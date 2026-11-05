"""Conservative, scoped DIA checksum inventory assessment; not an ISymUnmanagedDocument reader."""
import argparse
import hashlib
import json
from pathlib import Path

OWNED_FILES = (
    "CharacterLimitedTextReader.cs",
    "CsvRecordReaderAdapter.cs",
    "CsvStreamImporterAdapter.cs",
    "MalformedCsvException.cs",
)
ALGORITHMS = {1: ("md5", 16), 2: ("sha1", 20), 3: ("sha256", 32)}

def assess(lines, root):
    records = {}
    counts = []
    errors = []
    for raw in lines:
        line = raw.strip().lstrip("\ufeff")
        if line.startswith("DOC|"):
            fields = line.split("|")
            if len(fields) != 4 or not fields[2].isdigit():
                errors.append("malformed DIA source-file row")
                continue
            name = fields[1]
            if name in records:
                errors.append("duplicate DIA source-file basename")
            records[name] = (int(fields[2]), fields[3].lower())
        elif line.startswith("COUNT|"):
            counts.append(line)
    if len(counts) != 1:
        errors.append("missing or duplicate DIA inventory count")
    results = []
    for name in OWNED_FILES:
        record = records.get(name)
        if record is None:
            results.append({"document": name, "result": "not-enumerated"})
            continue
        algorithm_id, actual = record
        if algorithm_id not in ALGORITHMS or not actual:
            results.append({"document": name, "result": "no-supported-checksum",
                            "algorithm_id": algorithm_id})
            continue
        hash_name, digest_bytes = ALGORITHMS[algorithm_id]
        if len(actual) != digest_bytes * 2 or any(x not in "0123456789abcdef" for x in actual):
            errors.append(f"invalid checksum encoding: {name}")
            continue
        candidates = list((Path(root) / "src" / "RecordSift.Infrastructure.Csv").rglob(name))
        if len(candidates) != 1:
            errors.append(f"ambiguous or missing physical source: {name}")
            continue
        expected = hashlib.new(hash_name, candidates[0].read_bytes()).hexdigest()
        match = actual == expected
        if not match:
            errors.append(f"physical source checksum mismatch: {name}")
        results.append({"document": name, "result": "matched" if match else "mismatch",
                        "algorithm": hash_name, "digest_length": digest_bytes})
    matched = sum(x["result"] == "matched" for x in results)
    status = "FAILED" if errors else ("PARTIALLY_VERIFIED" if matched == len(OWNED_FILES) else "INCONCLUSIVE")
    return {"status": status, "dia_source_file_rows": len(records),
            "owned_documents_matched": matched, "owned_documents_expected": len(OWNED_FILES),
            "documents": results, "errors": errors,
            "limitation": "DIA source-file table is not necessarily the complete managed ISymUnmanagedDocument inventory."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dia-output", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = assess(args.dia_output.read_text(encoding="utf-8-sig").splitlines(), args.source_root)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"DIA checksum classification: {result['status']} "
          f"({result['owned_documents_matched']}/{result['owned_documents_expected']} selected documents)")
    return 1 if result["status"] == "FAILED" else 0

if __name__ == "__main__":
    raise SystemExit(main())
