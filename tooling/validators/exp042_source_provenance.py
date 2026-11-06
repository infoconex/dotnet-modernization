#!/usr/bin/env python3
"""EXP-042: validate Csc diagnostic task inputs and a real target's output privately.

Trusted, local, ephemeral MSBuild transcript only. NO raw diagnostic log, source
paths, original file bytes or digest values are printed or uploaded.
"""
import argparse
import base64
import hashlib
import json
import ntpath
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from classic_pdb_document_checksums import VerificationError, normalized_key
from exp041_compiler_input_audit import read_capture, require

MAX_LOG_BYTES = 40 * 1024 * 1024
MAX_XML_BYTES = 60 * 1024 * 1024


def windows_identity(item, project):
    item = item.strip().strip('"')
    if not item or not item.casefold().endswith(".cs"):
        raise VerificationError("INVALID_CSC_SOURCE_ITEM")
    full = item if ntpath.isabs(item) else ntpath.join(str(project), item)
    return normalized_key(ntpath.normpath(full))


def declared_source_binding(path):
    if not path.is_file() or path.stat().st_size > MAX_XML_BYTES:
        raise VerificationError("PREPROCESSED_CSC_DECLARATION_UNAVAILABLE")
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        raise VerificationError("INVALID_PREPROCESSED_CSC_DECLARATION") from None
    tasks = []
    for target in tree.iter():
        if target.tag.rsplit("}", 1)[-1] != "Target" or target.get("Name") != "CoreCompile":
            continue
        for child in target.iter():
            if child.tag.rsplit("}", 1)[-1] == "Csc":
                tasks.append(child.get("Sources"))
    if len(tasks) != 1:
        return "INCONCLUSIVE_CSC_TASK_DEFINITION"
    if tasks[0] != "@(Compile)":
        raise VerificationError("EVALUATED_CSC_SOURCE_BINDING_CHANGED")
    return "CORECOMPILE_CSC_USES_COMPILE_ITEMS"


def csc_source_parameter(log):
    # Deliberately parse the *task parameter*, not arbitrary compiler path text.
    # Missing / unrecognized format is inconclusive, never a false PASS.
    spans = re.findall(r'Task "Csc"[^\n]*\n(.*?)Done executing task "Csc"',
                       log, flags=re.I | re.S)
    if len(spans) != 1:
        return None, "CSC_TASK_COUNT_NOT_UNIQUE"
    span = spans[0]
    marker = re.search(r'^\s*Task Parameter:\s*Sources\s*=([^\r\n]*)',
                       span, flags=re.I | re.M)
    if marker is None:
        return None, "CSC_SOURCES_PARAMETER_NOT_OBSERVED"
    items = []
    inline = marker.group(1).strip()
    if inline:
        items += [x.strip() for x in inline.split(";") if x.strip()]
    remainder = span[marker.end():]
    for row in remainder.splitlines():
        t = row.strip()
        if (re.match(r'^Task Parameter\s*:', t, re.I) or
            re.match(r'^Done executing task\b', t, re.I) or
            re.match(r'^Using ".*" task\b', t, re.I) or
            re.match(r'^Output Item\(s\)\s*:', t, re.I)):
            break
        if not t or re.match(r'^[A-Za-z][A-Za-z0-9_]*=', t):
            continue  # MSBuild item metadata, not an item identity.
        if t.casefold().strip('"').endswith(".cs"):
            items.extend(x.strip() for x in t.split(";") if x.strip())
    if not items or len(items) > 1024:
        return None, "CSC_SOURCE_PARAMETER_UNPARSABLE"
    return items, "CSC_TASK_SOURCES_OBSERVED"


def compare_task_sources(items, records, project, raw_log=None):
    if items is None:
        return "INCONCLUSIVE", 0
    observed = [windows_identity(s, project) for s in items]
    captured = [normalized_key(ntpath.normpath(str(p))) for p, _, _ in records]
    if len(set(observed)) != len(observed):
        raise VerificationError("DUPLICATE_CSC_TASK_SOURCE_IDENTITY")
    if len(set(captured)) != len(captured):
        raise VerificationError("DUPLICATE_CAPTURED_SOURCE_IDENTITY")
    if set(observed) != set(captured):
        overlap = len(set(observed) & set(captured))
        # Compare private raw task-section presence only as a diagnostic, never
        # as evidence of a true Csc source parameter match.
        in_task = 0
        in_parameter = 0
        if raw_log is not None:
            spans = re.findall(r'Task "Csc"[^\\n]*\\n(.*?)Done executing task "Csc"',
                               raw_log, flags=re.I | re.S)
            if len(spans) == 1:
                body = spans[0].replace("\\\\", "/").casefold()
                marker = re.search(r'Task Parameter:\\s*Sources\\s*=', body, re.I)
                param = body[marker.end():].split("task parameter:", 1)[0] if marker else ""
                for p, _, _ in records:
                    if normalized_key(ntpath.normpath(str(p))) in set(observed):
                        continue
                    relative = ntpath.relpath(str(p), str(project)).replace("\\\\", "/").casefold()
                    in_task += int(relative in body)
                    in_parameter += int(relative in param)
        # Aggregate counters only. No private path, basename, hash, URL, or log.
        raise VerificationError(
            "EFFECTIVE_CSC_SOURCES_VS_CAPTURE_MISMATCH"
            "_OBS%d_CAP%d_OVERLAP%d_TASKREL%d_PARAMREL%d" %
            (len(observed), len(captured), overlap, in_task, in_parameter))
    return "MATCHED_INDEPENDENT_TASK_PARAMETER", len(observed)


def producer_record(producer_root, records, project, log):
    prepared = producer_root / "producer-before.flag"
    manifest = producer_root / "producer-after.tsv"
    if not prepared.is_file() or prepared.read_bytes() != b"PREPARED_ABSENT":
        raise VerificationError("GENERATOR_PREPARE_NOT_PROVEN")
    if not manifest.is_file() or manifest.stat().st_size > 8192:
        raise VerificationError("GENERATOR_OUTPUT_IDENTITY_MISSING")
    parts = manifest.read_text(encoding="ascii").strip().split("\t")
    if len(parts) != 3 or parts[0] != "PRODUCER":
        raise VerificationError("INVALID_GENERATOR_OUTPUT_MANIFEST")
    try:
        path = base64.b64decode(parts[1], validate=True).decode("utf-8", "strict")
    except (ValueError, UnicodeError):
        raise VerificationError("INVALID_GENERATOR_OUTPUT_ENCODING") from None
    identity = windows_identity(path, project)
    allowed = normalized_key(ntpath.normpath(ntpath.join(str(project), "obj"))) + "/"
    if not identity.startswith(allowed):
        raise VerificationError("GENERATED_OUTPUT_OUTSIDE_PROJECT_OBJ")
    matching = [(p, raw) for p, raw, _ in records
                if normalized_key(ntpath.normpath(str(p))) == identity]
    if len(matching) != 1:
        raise VerificationError("TARGET_OUTPUT_NOT_ONE_OF_COMPILER_INPUTS")
    digest = hashlib.sha256(matching[0][1]).hexdigest()
    if parts[2] != digest:
        raise VerificationError("GENERATED_OUTPUT_BYTES_VS_COMPILER_INPUT_MISMATCH")
    target = re.search(
        r'Target "GenerateTargetFrameworkMonikerAttribute"[^\n]*\n(.*?)'
        r'Done building target "GenerateTargetFrameworkMonikerAttribute"',
        log, flags=re.I | re.S)
    observed = bool(target and re.search(r'Task "WriteLinesToFile"', target.group(1), re.I))
    # The additional target/executed-task observation is independently required
    # before claiming producer provenance, even when physical bytes matched.
    return {
        "output_matches_private_compiler_input": True,
        "output_previously_absent": True,
        "producer_target_name": "GenerateTargetFrameworkMonikerAttribute",
        "generator_task_executed": observed,
        "producer_status": ("VERIFIED_TARGET_EXECUTION_AND_BYTES" if observed
                            else "INCONCLUSIVE_TASK_EXECUTION_NOT_OBSERVED"),
    }


def read_structured_csc_events(path):
    if not path.is_file() or path.stat().st_size > 128 * 1024:
        raise VerificationError("STRUCTURED_CSC_EVENT_FILE_MISSING_OR_OVERSIZED")
    try:
        rows = path.read_text(encoding="ascii").splitlines()
    except (UnicodeError, OSError):
        raise VerificationError("STRUCTURED_CSC_EVENT_FILE_INVALID") from None
    if len(rows) == 1 and rows[0] == "STATUS\tNO_UNIQUE_CSC_SOURCE_EVENT":
        return None, "INCONCLUSIVE_NO_UNIQUE_CSC_EVENT"
    if len(rows) < 3 or rows[0] != "STATUS\tCSC_TASK_PARAMETER_EVENT" or not rows[1].startswith("COUNT\t"):
        raise VerificationError("STRUCTURED_CSC_EVENT_HEADER_INVALID")
    try:
        count = int(rows[1].split("\t")[1])
    except (ValueError, IndexError):
        raise VerificationError("STRUCTURED_CSC_EVENT_COUNT_INVALID") from None
    if not 0 < count <= 1024 or len(rows) != count + 2:
        raise VerificationError("STRUCTURED_CSC_EVENT_COUNT_MISMATCH")
    items = []
    for row in rows[2:]:
        try:
            item = base64.b64decode(row, validate=True).decode("utf-8", "strict")
        except (UnicodeError, ValueError):
            raise VerificationError("STRUCTURED_CSC_EVENT_SOURCE_INVALID") from None
        if not item or len(item) > 8192:
            raise VerificationError("STRUCTURED_CSC_EVENT_SOURCE_INVALID")
        items.append(item)
    return items, "STRUCTURED_CSC_TASK_INPUT_EVENT"


def verify_provenance(records, preprocessed, log, producer_root, project,
                      structured_events=None):
    binding = declared_source_binding(preprocessed)
    producer = producer_record(producer_root, records, project, log)
    print("EXP042 producer corroboration:", producer["producer_status"])
    sources, category = csc_source_parameter(log)
    text_status = "INCONCLUSIVE"
    text_count = 0
    try:
        text_status, text_count = compare_task_sources(sources, records, project, log)
    except VerificationError as ex:
        if not str(ex).startswith("EFFECTIVE_CSC_SOURCES_VS_CAPTURE_MISMATCH"):
            raise
        text_status = "DIAGNOSTIC_TEXT_INCOMPLETE_OR_DISAGREES"
        text_count = len(sources) if sources else 0
    if structured_events is not None:
        event_sources, event_category = read_structured_csc_events(structured_events)
        status, count = compare_task_sources(event_sources, records, project)
    else:
        event_category = "NOT_CAPTURED"
        status, count = text_status, text_count
    return {
        "experiment": "EXP-042",
        "scope": "frozen CSV candidate only, private MSBuild diagnostic evidence",
        "evaluated_csc_source_binding": binding,
        "diagnostic_csc_parameter_observation": category,
        "diagnostic_text_evidence_status": text_status,
        "diagnostic_text_source_count": text_count,
        "structured_csc_task_parameter_evidence": event_category,
        "effective_csc_sources_verification": status,
        "effective_csc_source_count": count,
        "captured_compiler_source_count": len(records),
        "intermediate_producer": producer,
        "gate_c": "UNSATISFIED",
        "source_link_adoption": "HOLD",
        "privacy": "no original paths, private compiler command lines, raw sources or digests",
        "limitation": "task-parameter transcript only when exact and unambiguous; not a proof of compiler-server internals or virtual compiler documents",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("capture-dir", "producer-dir", "preprocessed", "private-log",
                 "project-dir", "output", "structured-events"):
        p.add_argument("--"+name, type=Path, required=True)
    args = p.parse_args()
    try:
        require(not args.output.exists(), "EVIDENCE_OUTPUT_ALREADY_EXISTS")
        require(args.private_log.is_file() and
                args.private_log.stat().st_size <= MAX_LOG_BYTES,
                "PRIVATE_DIAGNOSTIC_UNAVAILABLE_OR_OVERSIZED")
        records, _ = read_capture(args.capture_dir)
        log = args.private_log.read_text(encoding="utf-8-sig", errors="replace")
        result = verify_provenance(records, args.preprocessed, log,
                                   args.producer_dir, args.project_dir,
                                   args.structured_events)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n",
                               encoding="utf-8")
        print("EXP042 Csc parameter:", result["effective_csc_sources_verification"],
              "count:", result["effective_csc_source_count"],
              "producer:", result["intermediate_producer"]["producer_status"],
              "Gate C UNSATISFIED")
    except Exception as exc:
        # All runtime exceptions may contain sensitive private paths.
        category = str(exc) if isinstance(exc, VerificationError) else "PRIVATE_PROVENANCE_AUDIT_FAILED"
        print("EXP042 FAIL CLOSED:", category, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
