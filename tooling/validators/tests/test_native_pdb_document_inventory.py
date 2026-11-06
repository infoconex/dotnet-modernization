"""Synthetic positive and negative DBI/C13/native inventory regression controls."""
import hashlib
import struct
import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from native_pdb_document_inventory import (
    audit, dbi_source_inventory, VerificationError,
)

NAME = r"C:\src\Owned.cs"
EXTRA = r"C:\generated\Extra.cs"


def source_record(source=b"owned"):
    alg = uuid.UUID("8829d00f-11b8-4213-878b-770e8597ac16")
    digest = hashlib.sha256(source).digest()
    return bytes(48) + alg.bytes_le + struct.pack("<ii", 32, 0) + digest


def subsection(kind, data):
    raw = struct.pack("<II", kind, len(data)) + data
    return raw + bytes((-len(raw)) % 4)


def fixture(file_names=(NAME,), with_c13=True):
    names = b"".join(x.encode("utf-8") + b"\0" for x in file_names)
    name_offset = {name: names.index(name.encode("utf-8")) for name in file_names}
    entries = b""
    positions = []
    for name in file_names:
        positions.append(len(entries))
        entry = struct.pack("<IBB", name_offset[name], 32, 3) + bytes(32)
        entries += entry + bytes((-len(entry)) % 4)
    c13 = b""
    if with_c13:
        c13 += subsection(0xF4, entries)
        line = struct.pack("<IHHI", 0, 1, 0, 8)
        line += struct.pack("<III", positions[0], 1, 20)
        line += struct.pack("<II", 0, 0)
        c13 += subsection(0xF2, line)
    mod = bytearray(64)
    struct.pack_into("<H", mod, 34, 5)
    struct.pack_into("<III", mod, 36, 4, 0, len(c13))
    struct.pack_into("<H", mod, 48, len(file_names))
    mod.extend(b"Module.obj\0Module.obj\0")
    mod.extend(bytes((-len(mod)) % 4))
    file_names_bytes = b"".join(x.encode("utf-8") + b"\0" for x in file_names)
    offsets = []
    i = 0
    for name in file_names:
        offsets.append(i)
        i += len(name.encode("utf-8")) + 1
    file_info = (struct.pack("<HH", 1, len(file_names)) +
                 struct.pack("<HH", 0, len(file_names)) +
                 struct.pack("<" + "I" * len(offsets), *offsets) +
                 file_names_bytes)
    file_info += bytes((-len(file_info)) % 4)
    dbi = bytearray(64)
    struct.pack_into("<I", dbi, 0, 0xFFFFFFFF)
    struct.pack_into("<I", dbi, 24, len(mod))
    struct.pack_into("<I", dbi, 36, len(file_info))
    dbi.extend(mod)
    dbi.extend(file_info)
    names_stream = struct.pack("<III", 0xEFFEEFFE, 1, len(names)) + names
    streams = [None, None, None, bytes(dbi), names_stream, b"\x04\0\0\0" + c13,
               None, source_record()]
    named = {"/names": 4, "/SRC/FILES/" + NAME: 7}
    for name in file_names[1:]:
        named["/SRC/FILES/" + name] = len(streams)
        streams.append(source_record(name.encode()))
    readers = {"DNLIB": {"Owned.cs": NAME}, "CECIL": {"Owned.cs": NAME}}
    return streams, named, readers


class NativeInventoryTests(unittest.TestCase):
    def test_structured_dbi_c13_and_lines_agree(self):
        streams, named, readers = fixture()
        r = audit(streams, named, readers)
        self.assertEqual(r["native_dbi_status"], "DBI_PARSED")
        self.assertEqual(r["native_dbi_file_info_documents"], 1)
        self.assertEqual(r["native_c13_checksum_records"], 1)
        self.assertEqual(r["native_c13_line_blocks"], 1)
        self.assertEqual(r["native_c13_line_documents"], 1)
        self.assertEqual(r["unmatched"], [])
        self.assertEqual(r["gate_c"], "UNSATISFIED")

    def test_unmatched_native_document_referenced_by_dbi_and_c13(self):
        streams, named, readers = fixture((NAME, EXTRA))
        r = audit(streams, named, readers)
        self.assertEqual(len(r["unmatched"]), 1)
        x = r["unmatched"][0]
        self.assertTrue(x["dbi_file_info_reference"])
        self.assertTrue(x["c13_filechksms_reference"])
        self.assertFalse(x["c13_lines_reference"])
        self.assertFalse(x["source_bytes_verified"])
        self.assertEqual(x["classification"],
                         "REFERENCED_NATIVE_DOCUMENT_REQUIRES_ORIGINAL_INPUT")

    def test_unreferenced_native_named_stream_stays_unclassified(self):
        streams, named, readers = fixture()
        named["/SRC/FILES/" + EXTRA] = 8
        streams.append(source_record())
        r = audit(streams, named, readers)
        self.assertEqual(len(r["unmatched"]), 1)
        self.assertEqual(r["unmatched"][0]["classification"],
                         "UNREFERENCED_BY_PARSED_DBI_C13_NOT_PROVED_IRRELEVANT")

    def test_unrecognized_orphan_payload_is_not_silently_accepted(self):
        streams, named, readers = fixture()
        named["/SRC/FILES/" + EXTRA] = 8
        streams.append(b"unrecognized")
        self.assertEqual(audit(streams, named, readers)["unmatched"][0]["record"],
                         "UNRECOGNIZED_OR_MALFORMED")

    def test_incorrect_native_source_record_fails(self):
        streams, named, readers = fixture()
        streams[7] = b"invalid"
        with self.assertRaisesRegex(VerificationError, "INVALID_MANAGED_SOURCE_RECORD"):
            audit(streams, named, readers)

    def test_duplicate_normalized_native_path_rejected(self):
        streams, named, readers = fixture()
        named["/src/files/c:/src/owned.cs"] = 8
        streams.append(source_record())
        with self.assertRaisesRegex(VerificationError, "DUPLICATE_NATIVE"):
            audit(streams, named, readers)

    def test_duplicate_stream_id_rejected(self):
        streams, named, readers = fixture()
        named["/SRC/FILES/" + EXTRA] = 7
        with self.assertRaisesRegex(VerificationError, "DUPLICATE_NATIVE"):
            audit(streams, named, readers)

    def test_reader_document_disagreement_rejected(self):
        streams, named, readers = fixture()
        readers["CECIL"]["Owned.cs"] = EXTRA
        with self.assertRaisesRegex(VerificationError, "DISAGREEMENT"):
            audit(streams, named, readers)

    def test_invalid_module_stream_id_rejected(self):
        streams, named, readers = fixture()
        raw = bytearray(streams[3])
        struct.pack_into("<H", raw, 64 + 34, 999)
        streams[3] = bytes(raw)
        with self.assertRaisesRegex(VerificationError, "MODULE_STREAM_ID"):
            audit(streams, named, readers)

    def test_missing_filechksms_line_reference_rejected(self):
        streams, named, readers = fixture()
        mod = bytearray(streams[5])
        # The first C13 subsection's kind becomes unknown, leaving a line
        # block whose checksum offset no longer resolves.
        struct.pack_into("<I", mod, 4, 0xFA)
        streams[5] = bytes(mod)
        with self.assertRaisesRegex(VerificationError, "LINE_WITHOUT_FILECHKSMS"):
            audit(streams, named, readers)

    def test_c13_line_block_size_excluding_header_fails_closed(self):
        streams, named, readers = fixture()
        raw = bytearray(streams[5])
        # Module signature 4, checksum subsection header 8 + 40 payload,
        # line subsection header 8, line header 12, then fragment header.
        line_fragment_block_size = 4 + 48 + 8 + 12 + 8
        struct.pack_into("<I", raw, line_fragment_block_size, 8)
        streams[5] = bytes(raw)
        with self.assertRaisesRegex(VerificationError, "INVALID_C13_LINE_BLOCK"):
            audit(streams, named, readers)

    def test_unsupported_c13_checksum_algorithm_rejected(self):
        streams, named, readers = fixture()
        mod = bytearray(streams[5])
        # Signature 4, subsection header 8, name-offset 4, size 1, kind 1.
        mod[4 + 8 + 5] = 99
        streams[5] = bytes(mod)
        with self.assertRaisesRegex(VerificationError, "UNSUPPORTED_OR_INVALID_C13"):
            audit(streams, named, readers)

    def test_wrong_c13_name_offset_rejected(self):
        streams, named, readers = fixture()
        mod = bytearray(streams[5])
        struct.pack_into("<I", mod, 4 + 8, 999999)
        streams[5] = bytes(mod)
        with self.assertRaisesRegex(VerificationError, "INVALID_NATIVE_STRING_OFFSET"):
            audit(streams, named, readers)

    def test_missing_names_table_rejected_when_c13_required(self):
        streams, named, readers = fixture()
        named.pop("/names")
        with self.assertRaisesRegex(VerificationError, "C13_NAMES_STREAM_MISSING"):
            audit(streams, named, readers)

    def test_truncated_dbi_rejected(self):
        streams, named, readers = fixture()
        streams[3] = streams[3][:60]
        with self.assertRaisesRegex(VerificationError, "INVALID_DBI_HEADER"):
            audit(streams, named, readers)

    def test_incorrect_module_file_count_rejected(self):
        streams, named, readers = fixture()
        raw = bytearray(streams[3])
        struct.pack_into("<H", raw, 64 + 48, 9)
        streams[3] = bytes(raw)
        with self.assertRaisesRegex(VerificationError, "INVALID_DBI_MODULE_FILE_REFERENCE"):
            audit(streams, named, readers)

    def test_absent_dbi_does_not_imply_absent_documents(self):
        streams, named, readers = fixture()
        streams[3] = None
        result = audit(streams, named, readers)
        self.assertEqual(result["native_dbi_status"], "DBI_UNAVAILABLE")
        self.assertEqual(result["managed_documents_absent_from_dbi_file_info"], 1)
        self.assertEqual(result["native_inventory_coverage"],
                         "UNRESOLVED_UNTIL_ALL_REFERENCE_FAMILIES_AND_BYTES_ARE_PROVEN")

    def test_no_c13_not_assumed_complete(self):
        streams, named, readers = fixture(with_c13=False)
        result = audit(streams, named, readers)
        self.assertEqual(result["native_c13_checksum_records"], 0)
        self.assertEqual(result["native_inventory_coverage"],
                         "UNRESOLVED_UNTIL_ALL_REFERENCE_FAMILIES_AND_BYTES_ARE_PROVEN")


if __name__ == "__main__":
    unittest.main()
