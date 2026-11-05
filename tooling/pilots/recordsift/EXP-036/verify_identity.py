#!/usr/bin/env python3
"""Structural MSF7 PDB vs compiled PE identity, without source-link assumptions."""
import argparse
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(root / "tooling" / "validators"))
from native_windows_pdb_sourcelink import read_msf, parse_named_streams, read_pe_codeview


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dll", required=True, type=Path)
    parser.add_argument("--pdb", required=True, type=Path)
    args = parser.parse_args()
    streams = read_msf(args.pdb.read_bytes())
    guid, age, _ = parse_named_streams(streams[1], len(streams))
    if (guid, age) != read_pe_codeview(args.dll.read_bytes()):
        raise SystemExit("PE/PDB CodeView identity mismatch")
    print("Verified independently: native MSF7 Windows PDB, PE RSDS GUID/age match")


if __name__ == "__main__":
    main()
