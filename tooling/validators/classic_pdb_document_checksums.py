#!/usr/bin/env python3
"""Research-only, standard-library native Windows PDB document checksum verifier.

Requires the EXACT paired managed-document inventories captured privately by
two independently implemented readers, and explicit physical compiler-input
files supplied by the caller. Strict path normalization applies to FULL source
document keys; basename-only association is prohibited.

Trusted, build-produced symbols only. Outputs solely bounded categorical data,
never source bytes, raw source paths, URL mappings, native stream keys or hashes.
No adoption-policy decision is made by this tool.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import struct
import sys
import uuid

from native_windows_pdb_sourcelink import read_msf, parse_named_streams, read_pe_codeview

SHA1 = uuid.UUID("ff1816ec-aa5e-4d10-87f7-6f4963833460")
SHA256 = uuid.UUID("8829d00f-11b8-4213-878b-770e8597ac16")
ALGORITHMS = {SHA1: ("sha1", 20), SHA256: ("sha256", 32)}
PREFIX = "/src/files/"
MAX_DOCUMENTS = 1024
MAX_PRIVATE_MANIFEST = 128 * 1024
MAX_SOURCE = 16 * 1024 * 1024
MAX_SOURCE_RECORD = 2 * 1024 * 1024

class VerificationError(ValueError):
    """A failure category without unsafe input substrings."""


def normalized_key(key):
    """Normalize separators and case, not basename or relative path components."""
    if not isinstance(key, str) or not key or len(key) > 8192 or "\x00" in key:
        raise VerificationError("INVALID_DOCUMENT_KEY")
    return key.replace("\\", "/").casefold()


def source_key(url):
    if not url or len(url) > 4096 or "\x00" in url:
        raise VerificationError("INVALID_DOCUMENT_URL")
    return normalized_key(PREFIX + url)


def read_private_manifest(path):
    if not path.is_file() or path.stat().st_size > MAX_PRIVATE_MANIFEST:
        raise VerificationError("PRIVATE_MANIFEST_MISSING_OR_OVERSIZED")
    records = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        pair = line.split("\t")
        if len(pair) != 2:
            raise VerificationError("MALFORMED_PRIVATE_MANIFEST")
        name, encoded = pair
        if not name or name in records or len(records) >= MAX_DOCUMENTS:
            raise VerificationError("DUPLICATE_OR_OVERLIMIT_MANAGED_DOCUMENT")
        try:
            original_url = base64.b64decode(encoded, validate=True).decode("utf-8", "strict")
        except (ValueError, UnicodeError):
            raise VerificationError("INVALID_PRIVATE_URL_ENCODING") from None
        if not original_url or original_url.replace("\\", "/").split("/")[-1].casefold() != name.casefold():
            raise VerificationError("MANIFEST_BASENAME_DOES_NOT_MATCH_URL")
        records[name] = original_url
    if not records:
        raise VerificationError("EMPTY_MANAGED_DOCUMENT_INVENTORY")
    return records


def parse_injected_source(data):
    """Parse versioned Roslyn classic-PDB /SRC/FILES/ payload, fail closed.

    4 little-endian GUIDs + 2 signed lengths + checksum + optional source bytes.
    Returns None only for nonrecognized/empty *orphan* streams. For streams
    linked to documents a None is a fatal unsupported-format finding.
    """
    if data is None or len(data) < 72 or len(data) > MAX_SOURCE_RECORD:
        return None
    try:
        alg = uuid.UUID(bytes_le=data[48:64])
        digest_len, source_len = struct.unpack_from("<ii", data, 64)
    except (ValueError, struct.error):
        return None
    if alg not in ALGORITHMS:
        return None
    name, size = ALGORITHMS[alg]
    if digest_len != size or source_len < 0 or (72 + digest_len + source_len) != len(data):
        return None
    return {"algorithm": name, "digest": data[72:72+digest_len],
            "embedded_source_present": source_len > 0}


def native_sources(dll, pdb):
    """Read bounded MSF stream directory and structurally classify source streams."""
    try:
        streams = read_msf(pdb.read_bytes())
        guid, age, named = parse_named_streams(streams[1], len(streams))
        if read_pe_codeview(dll.read_bytes()) != (guid, age):
            raise VerificationError("PDB_PE_CODEVIEW_IDENTITY_MISMATCH")
    except (OSError, IndexError, KeyError, ValueError, struct.error) as exc:
        if isinstance(exc, VerificationError):
            raise
        raise VerificationError("INVALID_NATIVE_PDB_STRUCTURE_OR_PE") from None
    indexed = {}
    for raw_name, stream_id in named.items():
        if not raw_name.casefold().startswith(PREFIX):
            continue
        nk = normalized_key(raw_name)
        if nk in indexed:
            raise VerificationError("AMBIGUOUS_NORMALIZED_NATIVE_SOURCE_KEY")
        if stream_id < 0 or stream_id >= len(streams):
            raise VerificationError("NATIVE_STREAM_INDEX_OUT_OF_RANGE")
        indexed[nk] = parse_injected_source(streams[stream_id])
        if len(indexed) > MAX_DOCUMENTS:
            raise VerificationError("TOO_MANY_NATIVE_SOURCE_STREAMS")
    return indexed


def physical_files(paths):
    """Explicit trusted source list; never infer files from untrusted PDB URLs."""
    sources = {}
    for path in paths:
        if not path.is_file() or path.stat().st_size > MAX_SOURCE:
            raise VerificationError("EXPLICIT_SOURCE_MISSING_OR_OVERSIZED")
        name = path.name.casefold()
        if name in sources:
            raise VerificationError("COLLIDING_SOURCE_BASENAME_REQUIRES_EXPLICIT_IDENTITY_MAPPING")
        sources[name] = path
    if not sources:
        raise VerificationError("NO_EXPLICIT_PHYSICAL_SOURCES")
    return sources


def verify_coverage(native, reader_urls, sources, expected_names):
    """Return sanitized classifications or fail closed on any examined document.

    All reader documents must be checked. Native orphan streams are counted,
    not silently accepted or counted as managed documents.
    """
    if set(reader_urls) != {"DNLIB", "CECIL"}:
        raise VerificationError("REQUIRE_TWO_INDEPENDENT_READER_INVENTORIES")
    a, b = (reader_urls["DNLIB"], reader_urls["CECIL"])
    if len(a) != len(b):
        raise VerificationError("MANAGED_READER_DOCUMENT_COUNT_DISAGREEMENT")
    b_keys = {source_key(u) for u in b.values()}
    a_keys = [source_key(u) for u in a.values()]
    if len(set(a_keys)) != len(a_keys) or len(b_keys) != len(b):
        raise VerificationError("DUPLICATE_NORMALIZED_DOCUMENT_IDENTITY")
    if set(a_keys) != b_keys:
        raise VerificationError("INDEPENDENT_MANAGED_DOCUMENT_SET_DISAGREEMENT")
    if not {n.casefold() for n in expected_names}.issubset({n.casefold() for n in a}):
        raise VerificationError("REQUIRED_SELECTED_DOCUMENT_NOT_DISCOVERED")

    matched_native = set()
    seen_source = set()
    algorithms = {}
    missing_source = 0
    for display_name, url in a.items():
        name = display_name.casefold()
        key = source_key(url)
        if key not in native:
            raise VerificationError("MANAGED_DOCUMENT_WITHOUT_NATIVE_NAMED_STREAM")
        record = native[key]
        if record is None:
            raise VerificationError("UNSUPPORTED_OR_MALFORMED_DOCUMENT_SOURCE_STREAM")
        if name not in sources:
            missing_source += 1
            continue
        src = sources[name]
        digest = hashlib.new(record["algorithm"], src.read_bytes()).digest()
        if digest != record["digest"]:
            raise VerificationError("STRUCTURED_NATIVE_CHECKSUM_VS_PHYSICAL_SOURCE_MISMATCH")
        if name in seen_source:
            raise VerificationError("AMBIGUOUS_PHYSICAL_SOURCE_ASSOCIATION")
        seen_source.add(name)
        matched_native.add(key)
        algorithms[record["algorithm"]] = algorithms.get(record["algorithm"], 0) + 1

    if not {n.casefold() for n in expected_names}.issubset(seen_source):
        raise VerificationError("REQUIRED_SOURCE_NOT_CRYPTOGRAPHICALLY_VERIFIED")
    orphan_keys = set(native) - set(a_keys)
    orphan_invalid = sum(native[k] is None for k in orphan_keys)
    # A complete reader inventory is not proved by two readers that potentially
    # share discovery limitations. Extra native streams MUST be accounted for.
    complete = missing_source == 0 and not orphan_keys
    return {
        "managed_document_count": len(a_keys),
        "provided_physical_sources": len(sources),
        "source_hashes_matched": len(seen_source),
        "reader_document_sets_agree": True,
        "structured_digest_algorithm_counts": algorithms,
        "native_named_source_stream_count": len(native),
        "unmatched_native_source_streams": len(orphan_keys),
        "unmatched_native_unrecognized_records": orphan_invalid,
        "reader_documents_without_supplied_physical_source": missing_source,
        "inventory_completeness": "ALL_ENUMERATED_MANAGED_DOCS_AND_NATIVE_STREAMS"
                                  if complete else "INCOMPLETE_OR_UNCLASSIFIED_NATIVE_STREAMS",
        "native_source_record_verification": "VERIFIED_SELECTED_DOCUMENTS",
        "gate_c": "NOT_EVALUATED_FOR_POLICY_REPLACEMENT",
        "unproven": "Independence of complete native C13 document inventory, debugger operation, hostile-input safety, full app assembly scope",
    }


def run(args):
    readers = {
        "DNLIB": read_private_manifest(args.dnlib_urls),
        "CECIL": read_private_manifest(args.cecil_urls),
    }
    actual = native_sources(args.dll, args.pdb)
    provided = physical_files(args.source_file)
    return verify_coverage(actual, readers, provided, args.require_source_name)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dll", type=Path, required=True)
    p.add_argument("--pdb", type=Path, required=True)
    p.add_argument("--dnlib-urls", type=Path, required=True)
    p.add_argument("--cecil-urls", type=Path, required=True)
    p.add_argument("--source-file", type=Path, action="append", required=True)
    p.add_argument("--require-source-name", action="append", default=[])
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error("Refusing to overwrite existing output")
    try:
        result = run(args)
        report = {"experiment": "EXP-039",
                  "tool": "stdlib_trusted_native_windows_pdb_source_checksum_verifier",
                  "result": result,
                  "scope": "Limited to declared physical compiler-input files, two managed reader inventories and native named streams; no policy approval",
                  "privacy": "No source URLs, paths, PDB keys or digest hex in output"}
        args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print("EXP039 document verification:", result["source_hashes_matched"],
              "of", result["managed_document_count"],
              "managed docs; unmatched native named source streams:",
              result["unmatched_native_source_streams"],
              "inventory:", result["inventory_completeness"],
              "Gate C remains NOT EVALUATED for policy replacement")
    except (VerificationError, OSError, UnicodeError, ValueError) as ex:
        # Exception payload contains predefined categories ONLY, no external path strings.
        reason = str(ex) if isinstance(ex, VerificationError) else "UNCLASSIFIED_RESEARCH_VALIDATION_ERROR"
        print("EXP039 FAIL CLOSED:", reason, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
