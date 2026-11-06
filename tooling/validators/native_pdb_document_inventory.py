#!/usr/bin/env python3
"""EXP-040: bounded, research-only DBI/C13 vs native source-stream provenance audit.

Input PDBs must be trusted, locally compiler-produced MSF7 symbols. No raw
document strings, paths, hashes, source bytes, PDBs or metadata are emitted.
This is a diagnostic inventory, NOT a replacement for checksum Gate C.
"""
import argparse
import json
import struct
import sys
from pathlib import Path

from classic_pdb_document_checksums import (
    PREFIX, VerificationError, normalized_key, parse_injected_source,
    read_private_manifest, source_key,
)
from native_windows_pdb_sourcelink import (
    read_msf, parse_named_streams, read_pe_codeview,
)

MAX_MODULES = 1024
MAX_REFERENCES = 65536
MAX_C13_SIZE = 16 * 1024 * 1024
C13_LINES = 0xF2
C13_FILECHKSMS = 0xF4
C13_HASHES = {0: 0, 1: 16, 2: 20, 3: 32}


def require(condition, category):
    if not condition:
        raise VerificationError(category)


def u16(buf, pos):
    require(pos >= 0 and pos + 2 <= len(buf), "TRUNCATED_NATIVE_DOCUMENT_STRUCTURE")
    return struct.unpack_from("<H", buf, pos)[0]


def u32(buf, pos):
    require(pos >= 0 and pos + 4 <= len(buf), "TRUNCATED_NATIVE_DOCUMENT_STRUCTURE")
    return struct.unpack_from("<I", buf, pos)[0]


def nul_string(data, pos):
    require(0 <= pos < len(data), "INVALID_NATIVE_STRING_OFFSET")
    end = data.find(b"\0", pos)
    require(end >= 0 and end - pos <= 8192, "INVALID_NATIVE_STRING_TERMINATION")
    try:
        return data[pos:end].decode("utf-8", "strict"), end + 1
    except UnicodeError:
        raise VerificationError("INVALID_NATIVE_STRING_ENCODING") from None


def to_source_key(name):
    # DBI names are document names; do not silently discard directories.
    require(bool(name) and len(name) <= 4096, "INVALID_NATIVE_DOCUMENT_IDENTITY")
    return source_key(name)


def dbi_source_inventory(streams, named):
    """Return two independent native reference families, never guessed names.

    A C13 checksum record refers to a name in /names. A C13 line block refers
    to an offset into its module's FILECHKSMS subsection. The DBI File Info
    substream is a separate module-to-source inventory.
    """
    if len(streams) <= 3 or streams[3] is None:
        return {"status": "DBI_UNAVAILABLE", "dbi": set(), "c13": set(),
                "lines": set(), "modules": 0, "c13_records": 0,
                "line_references": 0}
    dbi = streams[3]
    require(len(dbi) >= 64 and u32(dbi, 0) == 0xFFFFFFFF,
            "INVALID_DBI_HEADER")
    sizes = [u32(dbi, i) for i in (24, 28, 32, 36, 40, 52, 48)]
    require(all(s <= MAX_C13_SIZE for s in sizes) and
            64 + sum(sizes) <= len(dbi), "INVALID_DBI_SUBSTREAM_BOUNDS")
    modules_raw = dbi[64:64 + sizes[0]]
    modules = []
    pos = 0
    while pos < len(modules_raw):
        require(len(modules) < MAX_MODULES and pos + 64 <= len(modules_raw),
                "INVALID_DBI_MODULE_INFO")
        sn = u16(modules_raw, pos + 34)
        sym, c11, c13 = (u32(modules_raw, pos + n) for n in (36, 40, 44))
        count = u16(modules_raw, pos + 48)
        require(not (c11 and c13) and sym + c11 + c13 <= MAX_C13_SIZE,
                "INVALID_DBI_MODULE_SIZE")
        p = pos + 64
        _, p = nul_string(modules_raw, p)
        _, p = nul_string(modules_raw, p)
        pos = (p + 3) & ~3
        require(pos <= len(modules_raw), "INVALID_DBI_MODULE_PADDING")
        modules.append((sn, sym, c11, c13, count))
    require(pos == len(modules_raw), "INVALID_DBI_MODULE_TRAILING")

    file_start = 64 + sizes[0] + sizes[1] + sizes[2]
    file_data = dbi[file_start:file_start + sizes[3]]
    dbi_keys = set()
    if file_data:
        require(len(file_data) >= 4, "INVALID_DBI_FILE_INFO")
        n = u16(file_data, 0)
        require(n == len(modules) and n <= MAX_MODULES,
                "DBI_MODULE_FILE_INFO_COUNT_MISMATCH")
        header = 4 + n * 4
        require(header <= len(file_data), "TRUNCATED_DBI_FILE_COUNTS")
        offsets = [u16(file_data, 4 + 2 * i) for i in range(n)]
        counts = [u16(file_data, 4 + 2 * n + 2 * i) for i in range(n)]
        total = sum(counts)
        require(total <= MAX_REFERENCES and header + total * 4 <= len(file_data),
                "INVALID_DBI_FILE_OFFSETS")
        names = file_data[header + total * 4:]
        # Module index offsets are counts, not byte offsets.
        for i, (start, count) in enumerate(zip(offsets, counts)):
            require(start + count <= total and modules[i][4] == count,
                    "INVALID_DBI_MODULE_FILE_REFERENCE")
            for j in range(start, start + count):
                name, _ = nul_string(names, u32(file_data, header + 4 * j))
                dbi_keys.add(to_source_key(name))

    c13_keys = set()
    line_keys = set()
    c13_count = 0
    line_count = 0
    need_names = any(c13 for _, _, _, c13, _ in modules)
    name_data = None
    if need_names:
        ids = [i for n, i in named.items() if n.casefold() == "/names"]
        require(len(ids) == 1 and streams[ids[0]] is not None,
                "C13_NAMES_STREAM_MISSING")
        raw = streams[ids[0]]
        require(len(raw) >= 12 and u32(raw, 0) == 0xEFFEEFFE and
                u32(raw, 4) == 1 and u32(raw, 8) <= len(raw) - 12,
                "INVALID_C13_NAMES_TABLE")
        name_data = raw[12:12 + u32(raw, 8)]

    for sn, sym, c11, c13, count in modules:
        if not c13:
            continue
        require(sn != 0xFFFF and sn < len(streams) and
                streams[sn] is not None, "INVALID_DBI_MODULE_STREAM_ID")
        stream = streams[sn]
        require(sym + c11 + c13 <= len(stream) and sym >= 4 and
                u32(stream, 0) == 4, "INVALID_DBI_MODULE_STREAM_LAYOUT")
        raw = stream[sym + c11:sym + c11 + c13]
        pos = 0
        checksum_offsets = {}
        line_offsets = []
        while pos < len(raw):
            require(pos + 8 <= len(raw), "TRUNCATED_C13_SUBSECTION")
            kind, length = u32(raw, pos), u32(raw, pos + 4)
            require(length <= len(raw) - pos - 8, "INVALID_C13_LENGTH")
            data = raw[pos + 8:pos + 8 + length]
            pos = (pos + 8 + length + 3) & ~3
            require(pos <= len(raw), "INVALID_C13_SUBSECTION_PADDING")
            if kind == C13_FILECHKSMS:
                offset = 0
                while offset < len(data):
                    require(offset + 6 <= len(data), "TRUNCATED_C13_CHECKSUM")
                    size, algorithm = data[offset + 4], data[offset + 5]
                    require(algorithm in C13_HASHES and
                            size == C13_HASHES[algorithm] and
                            offset + 6 + size <= len(data),
                            "UNSUPPORTED_OR_INVALID_C13_CHECKSUM")
                    name, _ = nul_string(name_data, u32(data, offset))
                    require(offset not in checksum_offsets,
                            "DUPLICATE_C13_CHECKSUM_OFFSET")
                    checksum_offsets[offset] = to_source_key(name)
                    c13_count += 1
                    require(c13_count <= MAX_REFERENCES, "TOO_MANY_C13_REFERENCES")
                    offset = (offset + 6 + size + 3) & ~3
                require(offset == len(data), "INVALID_C13_CHECKSUM_PADDING")
            elif kind == C13_LINES:
                require(len(data) >= 12, "TRUNCATED_C13_LINES")
                flags = u16(data, 6)
                require(not(flags & ~1), "UNSUPPORTED_C13_LINE_FLAGS")
                q = 12
                while q < len(data):
                    require(q + 12 <= len(data), "TRUNCATED_C13_LINE_BLOCK")
                    file_offset, nlines, size = (u32(data, q + x) for x in (0, 4, 8))
                    require(nlines <= MAX_REFERENCES and
                            size == nlines * (12 if flags & 1 else 8) and
                            q + 12 + size <= len(data), "INVALID_C13_LINE_BLOCK")
                    line_offsets.append(file_offset)
                    line_count += 1
                    require(line_count <= MAX_REFERENCES, "TOO_MANY_C13_LINE_BLOCKS")
                    q += 12 + size
                require(q == len(data), "INVALID_C13_LINE_TRAILING")
            # Unknown subsection kinds are not interpreted as document records.
        c13_keys.update(checksum_offsets.values())
        for offset in line_offsets:
            require(offset in checksum_offsets, "C13_LINE_WITHOUT_FILECHKSMS")
            line_keys.add(checksum_offsets[offset])

    return {"status": "DBI_PARSED", "dbi": dbi_keys, "c13": c13_keys,
            "lines": line_keys, "modules": len(modules),
            "c13_records": c13_count, "line_references": line_count}


def audit(streams, named, readers):
    """Return only aggregate counts and three opaque orphan classifications."""
    require(set(readers) == {"DNLIB", "CECIL"},
            "REQUIRE_TWO_INDEPENDENT_READER_INVENTORIES")
    sets = []
    for urls in readers.values():
        keys = [source_key(u) for u in urls.values()]
        require(len(keys) == len(set(keys)), "DUPLICATE_MANAGED_DOCUMENT_KEY")
        sets.append(set(keys))
    require(sets[0] == sets[1], "MANAGED_READER_DOCUMENT_SET_DISAGREEMENT")
    managed = sets[0]
    keys = {}
    used_streams = set()
    for name, stream_id in named.items():
        if normalized_key(name).startswith(PREFIX):
            nk = normalized_key(name)
            require(nk not in keys and stream_id not in used_streams,
                    "DUPLICATE_NATIVE_SOURCE_IDENTITY_OR_STREAM")
            require(0 <= stream_id < len(streams), "INVALID_NATIVE_STREAM_ID")
            used_streams.add(stream_id)
            record = parse_injected_source(streams[stream_id])
            keys[nk] = record
    require(managed <= keys.keys(), "MANAGED_DOCUMENT_NATIVE_STREAM_MISSING")
    for key in managed:
        require(keys[key] is not None, "INVALID_MANAGED_SOURCE_RECORD")
    native = dbi_source_inventory(streams, named)
    dbi_keys = native["dbi"]
    c13_keys = native["c13"]
    lines = native["lines"]
    orphans = []
    for key in sorted(keys.keys() - managed):
        record = keys[key]
        orphans.append({
            "id": "unmatched-" + str(len(orphans) + 1),
            "record": "SUPPORTED_" + record["algorithm"].upper() if record
                      else "UNRECOGNIZED_OR_MALFORMED",
            "dbi_file_info_reference": key in dbi_keys,
            "c13_filechksms_reference": key in c13_keys,
            "c13_lines_reference": key in lines,
            "source_bytes_verified": False,
            "classification": (
                "REFERENCED_NATIVE_DOCUMENT_REQUIRES_ORIGINAL_INPUT"
                if key in dbi_keys or key in c13_keys or key in lines else
                "UNREFERENCED_BY_PARSED_DBI_C13_NOT_PROVED_IRRELEVANT"),
        })
    return {
        "experiment": "EXP-040",
        "scope": "frozen CSV candidate trusted local PDB only",
        "native_source_streams": len(keys),
        "managed_reader_document_count": len(managed),
        "managed_with_native_stream": len(managed & keys.keys()),
        "native_dbi_status": native["status"],
        "native_dbi_module_count": native["modules"],
        "native_dbi_file_info_documents": len(dbi_keys),
        "native_c13_checksum_records": native["c13_records"],
        "native_c13_checksum_documents": len(c13_keys),
        "native_c13_line_blocks": native["line_references"],
        "native_c13_line_documents": len(lines),
        "native_dbi_documents_without_named_stream": len(dbi_keys - keys.keys()),
        "native_c13_documents_without_named_stream": len(c13_keys - keys.keys()),
        "managed_documents_absent_from_dbi_file_info": len(managed - dbi_keys),
        "managed_documents_absent_from_c13_checksum": len(managed - c13_keys),
        "unmatched": orphans,
        "native_inventory_coverage": "UNRESOLVED_UNTIL_ALL_REFERENCE_FAMILIES_AND_BYTES_ARE_PROVEN",
        "gate_c": "UNSATISFIED",
        "source_link_adoption": "HOLD",
        "privacy": "counts, fixed categories and opaque IDs only; no source URLs, names, paths, record bytes or digest values",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("dll", "pdb", "dnlib-urls", "cecil-urls", "output"):
        parser.add_argument("--" + option, required=True, type=Path)
    args = parser.parse_args()
    require(not args.output.exists(), "EVIDENCE_FILE_ALREADY_EXISTS")
    try:
        streams = read_msf(args.pdb.read_bytes())
        guid, age, named = parse_named_streams(streams[1], len(streams))
        require(read_pe_codeview(args.dll.read_bytes()) == (guid, age),
                "NATIVE_PE_PDB_IDENTITY_MISMATCH")
        readers = {"DNLIB": read_private_manifest(args.dnlib_urls),
                   "CECIL": read_private_manifest(args.cecil_urls)}
        report = audit(streams, named, readers)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
        print("EXP040 classified", len(report["unmatched"]), "orphan streams;",
              "DBI:", report["native_dbi_status"],
              "Gate C UNSATISFIED")
    except (VerificationError, OSError, ValueError, IndexError, KeyError,
            UnicodeError, struct.error):
        # Never display exception text arising from raw source strings or PDB data.
        print("EXP040 FAIL CLOSED: native evidence invalid or unsupported",
              file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
