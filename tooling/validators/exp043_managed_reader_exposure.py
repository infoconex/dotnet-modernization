#!/usr/bin/env python3
"""EXP-043: compare two pinned managed-reader document inventories to native PDBs.

Read trusted, private ReaderProbe output and URL manifests only. Never emit
document names, URLs, PDBs, hashes, source bytes or reader raw stdout.
Managed APIs' missing digests do not override native physical-source proof.
"""
import argparse
import json
from pathlib import Path
import sys

from classic_pdb_document_checksums import VerificationError, read_private_manifest, source_key
from exp043_five_pdb_audit import COMPONENTS, SLUGS, source_pdb_inventory


def read_managed(reader_dir, component, reader):
    private = reader_dir / (component + "-" + reader + "-urls.private")
    stdout = reader_dir / (component + "-" + reader + "-stdout.private")
    if not stdout.is_file() or stdout.stat().st_size > 128 * 1024:
        raise VerificationError("PRIVATE_MANAGED_READER_OUTPUT_MISSING_OR_OVERSIZED")
    urls = read_private_manifest(private)
    lines = stdout.read_text(encoding="utf-8-sig").splitlines()
    seen = {}
    end = None
    for line in lines:
        cells = line.split("\t")
        if len(cells) == 2 and cells[0] == "MISSING":
            name = cells[1]
            if name in seen:
                raise VerificationError("DUPLICATE_MANAGED_READER_DOCUMENT")
            seen[name] = "MISSING"
        elif len(cells) == 4 and cells[0] == "DOC":
            name = cells[1]
            if name in seen or len(cells[3]) not in (40, 64) or not all(
                    x in "0123456789abcdef" for x in cells[3].lower()):
                raise VerificationError("INVALID_MANAGED_READER_CHECKSUM")
            seen[name] = "EXPOSED"
        elif len(cells) == 3 and cells[0] == "END":
            if end is not None:
                raise VerificationError("DUPLICATE_MANAGED_READER_END")
            try:
                end = tuple(int(x) for x in cells[1:])
            except ValueError:
                raise VerificationError("INVALID_MANAGED_READER_END_COUNT") from None
        else:
            raise VerificationError("UNRECOGNIZED_MANAGED_READER_PRIVATE_OUTPUT")
    if end != (sum(v == "EXPOSED" for v in seen.values()),
               sum(v == "MISSING" for v in seen.values())):
        raise VerificationError("MANAGED_READER_COUNT_DIVERGENCE")
    if set(seen) != set(urls):
        raise VerificationError("MANAGED_READER_DOCUMENT_URL_ASSOCIATION_INCOMPLETE")
    keys = [source_key(url) for url in urls.values()]
    if len(keys) != len(set(keys)):
        raise VerificationError("DUPLICATE_MANAGED_FULL_DOCUMENT_IDENTITY")
    return set(keys), {
        "managed_document_count": len(seen),
        "managed_document_checksum_exposed": sum(
            x == "EXPOSED" for x in seen.values()),
        "managed_document_checksum_missing": sum(
            x == "MISSING" for x in seen.values()),
    }


def classify_error(ex):
    return str(ex) if isinstance(ex, VerificationError) else "MANAGED_READER_AUDIT_FAILED_CLOSED"


def audit(app, reader_dir):
    results = []
    for component in COMPONENTS:
        name = "RecordSift." + component
        stem = app / "src" / name / "bin" / "Release" / name
        item = {"component": component, "status": "BLOCKED"}
        try:
            native, dbi = source_pdb_inventory(
                Path(str(stem) + ".dll"), Path(str(stem) + ".pdb"))
            if set(native) != dbi["dbi"] or set(native) != dbi["c13"]:
                raise VerificationError("MANAGED_PROBE_NATIVE_PDB_INVENTORY_UNTRUSTED")
            dn_keys, dn = read_managed(reader_dir, component, "DNLIB")
            ce_keys, ce = read_managed(reader_dir, component, "CECIL")
            item["native_source_documents"] = len(native)
            item["dnlib"] = dn
            item["cecil"] = ce
            item["reader_document_agreement"] = (
                "MATCHED" if dn_keys == ce_keys else "DISAGREES")
            item["reader_documents_subset_of_native"] = (
                dn_keys <= set(native) and ce_keys <= set(native))
            item["native_documents_not_exposed_by_both_readers"] = len(
                set(native) - (dn_keys & ce_keys))
            item["status"] = (
                "VERIFIED_READER_LIMITATION"
                if item["reader_document_agreement"] == "MATCHED"
                and item["reader_documents_subset_of_native"]
                else "INCOMPLETE"
            )
        except Exception as ex:
            item["failure_category"] = classify_error(ex)
        results.append(item)
    return {
        "experiment": "EXP-043",
        "phase": "two_pinned_managed_reader_exposure",
        "results": results,
        "all_five_readers_audited": all(
            x["status"] == "VERIFIED_READER_LIMITATION" for x in results),
        "managed_checksum_gate_c": "UNSATISFIED",
        "source_link_adoption": "HOLD",
        "privacy": "only native/managed counts, checksum exposure counts and fixed categories; source names, URLs, hashes, PDBs and private stdout never uploaded",
        "limitation": "dnlib and Cecil managed reader API exposure is not a complete native document inventory or authentic debugger operation",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--app-root", required=True, type=Path)
    p.add_argument("--reader-root", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    try:
        if a.output.exists():
            raise VerificationError("SANITIZED_READER_REPORT_ALREADY_EXISTS")
        result = audit(a.app_root, a.reader_root)
        a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
        print("EXP043 managed reader exposure:",
              ", ".join(x["component"] + "=" + x["status"] for x in result["results"]),
              "managed Gate C UNSATISFIED, Source Link HOLD")
        if not result["all_five_readers_audited"]:
            sys.exit(2)
    except Exception as ex:
        print("EXP043 reader FAIL CLOSED:", classify_error(ex), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
