#!/usr/bin/env python3
"""EXP-041: independently bind native PDB documents to private Csc-input snapshots.

For trusted, locally compiler-produced PDBs only. Source paths, original
bytes, complete digests and private manifest values are NEVER emitted.
Native PDB identities are never used as filesystem paths.
"""
import argparse
import base64
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys

from classic_pdb_document_checksums import (
    VerificationError, normalized_key, parse_injected_source, source_key,
)
from native_pdb_document_inventory import dbi_source_inventory
from native_windows_pdb_sourcelink import read_msf, parse_named_streams, read_pe_codeview

MAX_INPUTS = 1024
MAX_CAPTURE_BYTES = 16 * 1024 * 1024
MAX_MANIFEST = 512 * 1024


def require(ok, code):
    if not ok:
        raise VerificationError(code)


def decode(encoded):
    try:
        return base64.b64decode(encoded, validate=True).decode("utf-8", "strict")
    except (ValueError, UnicodeError):
        raise VerificationError("INVALID_PRIVATE_CAPTURE_ENCODING") from None


def parse_pathmap(value):
    if not value:
        return []
    # MSBuild may concatenate mapping fragments with commas or semicolons,
    # including leading/trailing empty separators. They are not mappings.
    # An empty interior segment is ambiguous and rejected.
    tokens = re.split(r"[,;]", value)
    while tokens and not tokens[0].strip():
        tokens.pop(0)
    while tokens and not tokens[-1].strip():
        tokens.pop()
    result = []
    for item in tokens:
        require(bool(item.strip()), "AMBIGUOUS_CAPTURE_PATHMAP_SEPARATOR")
        pair = item.rsplit("=", 1)
        require(len(pair) == 2 and all(pair), "INVALID_CAPTURE_PATHMAP_ENTRY")
        left, right = (x.strip().replace("\\", "/") for x in pair)
        require(left.startswith("/") or (len(left) > 2 and left[1] == ":"),
                "INVALID_CAPTURE_PATHMAP_ROOT")
        require(not any(left.casefold() == x[0].casefold() for x in result),
                "DUPLICATE_CAPTURE_PATHMAP_ROOT")
        result.append((left, right))
    return sorted(result, key=lambda x: len(x[0]), reverse=True)


def apply_pathmap(physical, mappings):
    value = physical.replace("\\", "/")
    for old, new in mappings:
        if (value.casefold() == old.casefold() or
                (value.casefold().startswith(old.casefold()) and
                 (old.endswith("/") or value[len(old):].startswith("/")))):
            suffix = value[len(old):].lstrip("/")
            return new.rstrip("/") + ("/" + suffix if suffix else "")
    return value


def read_capture(root):
    manifest = root / "input-manifest.tsv"
    require(manifest.is_file() and manifest.stat().st_size <= MAX_MANIFEST,
            "MISSING_OR_OVERSIZED_PRIVATE_CAPTURE")
    lines = manifest.read_text(encoding="ascii").splitlines()
    require(2 <= len(lines) <= MAX_INPUTS + 1, "INVALID_CAPTURE_ITEM_COUNT")
    header = lines[0].split("\t")
    require(len(header) == 2 and header[0] == "PATHMAP",
            "INVALID_CAPTURE_HEADER")
    mappings = parse_pathmap(decode(header[1]))
    records = []
    seen_files = set()
    for i, row in enumerate(lines[1:]):
        parts = row.split("\t")
        require(len(parts) == 3 and parts[0] == str(i),
                "DUPLICATE_OR_NONCONTIGUOUS_CAPTURE_IDENTIFIER")
        physical_name = decode(parts[1])
        physical = Path(physical_name)
        require(physical.is_absolute(), "CAPTURE_PATH_NOT_ABSOLUTE")
        key = normalized_key(str(physical))
        require(key not in seen_files, "DUPLICATE_CAPTURE_PHYSICAL_IDENTITY")
        seen_files.add(key)
        digest = parts[2].lower()
        require(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
                "INVALID_CAPTURE_DIGEST")
        data = root / ("input-%04d.bin" % i)
        require(data.is_file() and data.stat().st_size <= MAX_CAPTURE_BYTES,
                "CAPTURED_ORIGINAL_BYTES_MISSING_OR_OVERSIZED")
        raw = data.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest,
                "CAPTURE_MANIFEST_VS_SNAPSHOT_MISMATCH")
        # The post-Csc MSBuild task separately checks that source bytes remain
        # unchanged before/after compilation; this is not a replay from Git.
        records.append((physical, raw, apply_pathmap(str(physical), mappings)))
    return records, mappings


def classify_origin(path, repo):
    # Classification is based on independently supplied compiler source paths.
    # PDB source keys cannot cause arbitrary filesystem access.
    try:
        relative = path.resolve(strict=True).relative_to(repo.resolve(strict=True))
    except ValueError:
        return "external"
    except OSError:
        return "unknown"
    parts = [s.casefold() for s in relative.parts]
    if "obj" in parts:
        return "intermediate_location_producer_unverified"
    proc = subprocess.run(["git", "-C", str(repo), "ls-files", "--error-unmatch",
                           "--", relative.as_posix()], capture_output=True,
                          timeout=15, check=False)
    return "checked_in" if proc.returncode == 0 else "untracked_or_unknown"


def verify(native, dbi, records, repo):
    require(dbi["status"] == "DBI_PARSED", "DBI_NOT_PROVEN")
    native_keys = set(native)
    require(bool(native_keys), "EMPTY_NATIVE_DOCUMENT_INVENTORY")
    require(native_keys == dbi["dbi"] == dbi["c13"],
            "NATIVE_DBI_C13_UNIVERSE_DISAGREES")
    require(dbi["lines"] <= native_keys, "UNREFERENCED_C13_LINE_DOCUMENT")
    require(all(v is not None for v in native.values()),
            "NATIVE_RECORD_ALGORITHM_UNSUPPORTED")
    seen = {}
    origins = {}
    for physical, raw, mapped in records:
        key = source_key(mapped)
        require(key not in seen, "DUPLICATE_MAPPED_COMPILER_INPUT_IDENTITY")
        seen[key] = (raw, physical)
    matches = 0
    missing = 0
    origin_counts = {}
    for key in sorted(native_keys):
        algorithm = native[key]["algorithm"]
        require(algorithm in ("sha1", "sha256"), "NATIVE_ALGORITHM_MISMATCH")
        if key not in seen:
            missing += 1
            continue
        data, physical = seen[key]
        require(hashlib.new(algorithm, data).digest() == native[key]["digest"],
                "ORIGINAL_COMPILER_INPUT_HASH_MISMATCH")
        matches += 1
        origin = classify_origin(physical, repo)
        origins[key] = origin
        origin_counts[origin] = origin_counts.get(origin, 0) + 1
    unassociated = set(seen) - native_keys
    require(not unassociated, "COMPILER_INPUT_WITHOUT_NATIVE_RECORD")
    # The current managed-reader limit is four, not a policy redefinition.
    complete = missing == 0 and matches == len(native_keys)
    # C13 non-line-referenced identities are an independent family. EXP-040
    # established these three are also absent from both managed reader lists;
    # this standalone verifier does NOT rediscover the reader universe.
    no_line = sorted(native_keys - dbi["lines"])
    no_line_evidence = [
        {"id": "native-no-line-" + str(i + 1),
         "physical_bytes_authenticated": key in origins,
         "origin_evidence": origins.get(key, "original_compiler_input_unavailable")}
        for i, key in enumerate(no_line)
    ]
    return {
        "experiment": "EXP-041", "native_source_documents": len(native_keys),
        "captured_compiler_inputs": len(records),
        "original_input_sha256_or_sha1_matches": matches,
        "native_documents_without_captured_input": missing,
        "origin_categories": origin_counts,
        "native_line_referenced_documents": len(dbi["lines"]),
        "native_documents_without_line_references": no_line_evidence,
        "c13_checksum_algorithms": dbi["c13_algorithm_counts"],
        "native_inventory": "COVERED_BY_CAPTURE" if complete else "INCOMPLETE",
        "original_compiler_input_bytes": "MATCHED_ALL_NATIVE_DOCUMENTS" if complete else "INCOMPLETE",
        "gate_c": "UNSATISFIED", "source_link_adoption": "HOLD",
        "scope": "frozen CSV only; original physical bytes snapshotted at pre-CoreCompile and checked post-CoreCompile",
        "not_proven": "effective compiler argv completeness, other four production PDBs, existing managed checksum Gate C, IDE installation or live debugger",
        "privacy": "aggregate counts and fixed categories only; no source names, paths, PDB keys or digests",
    }


def run(args):
    records, _ = read_capture(args.capture_dir)
    streams = read_msf(args.pdb.read_bytes())
    guid, age, named = parse_named_streams(streams[1], len(streams))
    require(read_pe_codeview(args.dll.read_bytes()) == (guid, age),
            "NATIVE_PE_PDB_IDENTITY_MISMATCH")
    native = {}
    for name, stream_id in named.items():
        if normalized_key(name).startswith("/src/files/"):
            key = normalized_key(name)
            require(key not in native, "DUPLICATE_NATIVE_SOURCE_IDENTITY")
            require(0 <= stream_id < len(streams), "NATIVE_STREAM_ID_OUT_OF_RANGE")
            native[key] = parse_injected_source(streams[stream_id])
    require(0 < len(native) <= MAX_INPUTS, "INVALID_NATIVE_DOCUMENT_COUNT")
    dbi = dbi_source_inventory(streams, named)
    return verify(native, dbi, records, args.app_root)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ("dll", "pdb", "capture-dir", "app-root", "output"):
        p.add_argument("--" + arg, required=True, type=Path)
    args = p.parse_args()
    try:
        require(not args.output.exists(), "EVIDENCE_OUTPUT_ALREADY_PRESENT")
        result = run(args)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
        print("EXP041 captured", result["captured_compiler_inputs"], "compiler inputs;",
              result["original_input_sha256_or_sha1_matches"], "native bytes verified;",
              "missing", result["native_documents_without_captured_input"],
              "Gate C UNSATISFIED; Source Link HOLD")
    except Exception as ex:
        # Even filesystem exceptions may contain private paths. Do not print them.
        category = str(ex) if isinstance(ex, VerificationError) else "CAPTURE_AUDIT_FAILED_CLOSED"
        print("EXP041 FAIL CLOSED:", category, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
