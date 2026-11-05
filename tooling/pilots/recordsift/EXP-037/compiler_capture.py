#!/usr/bin/env python3
"""Sanitize private MSBuild diagnostic evidence without retaining paths or command lines.

Never copy the source log into a repository or uploaded Actions artifact. A switch
not observed in a diagnostic transcript is UNKNOWN, not proven absent.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

TASK_START = re.compile(r'\bTask "Csc"(?:\s|\()', re.I)
TASK_END = re.compile(r'\bDone executing task "Csc"', re.I)
SWITCHES = (
    "debug", "pdb", "checksumalgorithm", "deterministic", "pathmap",
    "sourcelink", "nostdlib", "langversion", "optimize", "shared", "define",
    "target", "out", "reference", "features",
)
SWITCH_RE = re.compile(
    r'(?<![A-Za-z0-9])/(%s)(?:(:)([^\s"\x27]+)|([+-]))?' % "|".join(SWITCHES),
    re.I,
)
COMPILER_PATH = re.compile(r'([A-Za-z]:\\[^"\r\n]*?\\(?:csc|VBCSCompiler)\.exe)', re.I)
VALID_VALUES = {
    "debug": {"pdbonly", "portable", "embedded", "full", "-"},
    "checksumalgorithm": {"sha1", "sha256"},
    "langversion": {"7.3", "default", "latest"},
}
# Exact flag values are constrained to harmless allowlists. All other argument
# values, including source paths, are deliberately discarded.
def parse(log):
    spans = []
    current = []
    for row in log.splitlines():
        if TASK_START.search(row):
            if current:
                spans.append(current)
            current = [row]
        elif current:
            current.append(row)
            if TASK_END.search(row):
                spans.append(current)
                current = []
    if current:
        spans.append(current)
    switches = {key: set() for key in SWITCHES}
    tool_identity = set()
    captured_argv_lines = 0
    for span in spans:
        for line in span:
            stripped = line.strip()
            # Restrict to compiler command lines, not arbitrary Task Parameter paths.
            if not (re.search(r'(?i)\\csc\.exe\b|\bCommandLineArguments\b|\bCommand Line\b|\bcsc\.exe\b', line)
                    or (line.count(' /') >= 3 and '/debug' in line.lower())):
                continue
            found = list(SWITCH_RE.finditer(line))
            if not found:
                continue
            captured_argv_lines += 1
            if re.search(r'(?i)\\csc\.exe\b|\bcsc\.exe\b', line):
                tool_identity.add("csc.exe_command_line_mentioned")
            for match in found:
                name = match.group(1).lower()
                value = match.group(3) or match.group(4) or "BARE"
                if name in VALID_VALUES:
                    safe = value.lower()
                    switches[name].add(safe if safe in VALID_VALUES[name] else "PRESENT_UNCLASSIFIED")
                elif name in ("deterministic", "optimize"):
                    switches[name].add(value if value in ("+", "-") else "PRESENT")
                else:
                    switches[name].add("PRESENT")
    text = "\n".join("\n".join(s) for s in spans)
    markers = {
        "csc_task_count": len(spans),
        "candidate_command_line_evidence_lines": captured_argv_lines,
        "csc_executable_name_in_command_line": bool(tool_identity),
        "compiler_server_mentioned_within_csc_task": "VBCSCompiler" in text,
        "shared_compilation_task_property_mentioned": "UseSharedCompilation" in text,
    }
    # NEVER interpret missing switches as absent; an MSBuild task may invoke
    # Roslyn's compiler server or omit normalized arguments from its log.
    return {
        "experiment": "EXP-037",
        "evidence_scope": "ephemeral private MSBuild candidate diagnostic log",
        "compiler_switches_observed": {k: sorted(v) for k, v in switches.items()},
        "capture_markers": markers,
        "confidence": "OBSERVED_ONLY_NOT_A_COMPLETE_EFFECTIVE_COMPILER_INVOCATION",
        "unobserved_switch_policy": "UNKNOWN_NOT_PROVEN_ABSENT",
        "private_values_excluded": "source paths, output paths, reference lists, response file contents, host environment",
    }

def self_test():
    specimen = (
        'Task "Csc" (TaskId:42):\n'
        '  C:\\Private User\\VS\\csc.exe /noconfig /debug:pdbonly /deterministic+ '
        '/checksumalgorithm:SHA256 /pathmap:C:\\Private User\\source=/_/ '
        '/sourcelink:C:\\Private User\\secret.json /langversion:7.3 '
        '/out:C:\\Private User\\secret.dll /reference:C:\\Private User\\secret.dll\n'
        'Done executing task "Csc".\n'
    )
    s = json.dumps(parse(specimen))
    assert "Private User" not in s
    assert parse(specimen)["compiler_switches_observed"]["checksumalgorithm"] == ["sha256"]
    assert parse(specimen)["compiler_switches_observed"]["pathmap"] == ["PRESENT"]
    assert parse("task \"Other\"")["capture_markers"]["csc_task_count"] == 0
    assert parse("Task \"Csc\"\nDone executing task \"Csc\"")[
        "compiler_switches_observed"]["checksumalgorithm"] == []
    print("EXP-037 sanitized compiler log synthetic positive/negative controls PASS")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--private-log", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    if args.private_log is None or args.output is None:
        ap.error("--private-log and --output required")
    if args.output.exists():
        ap.error("Refusing to overwrite result")
    size = args.private_log.stat().st_size
    if size > 30 * 1024 * 1024:
        ap.error("Private diagnostic log exceeds size limit")
    result = parse(args.private_log.read_text(encoding="utf-8-sig", errors="replace"))
    if result["capture_markers"]["csc_task_count"] == 0:
        raise SystemExit("No candidate Csc task located; compiler invocation evidence unavailable")
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("EXP-037: candidate compiler diagnostic evidence sanitized")
    print("Csc tasks:", result["capture_markers"]["csc_task_count"])
    print("Command-line evidence lines:", result["capture_markers"]["candidate_command_line_evidence_lines"])
    print("Switch categories:", {k:v for k,v in result["compiler_switches_observed"].items() if v})

if __name__ == "__main__":
    main()
