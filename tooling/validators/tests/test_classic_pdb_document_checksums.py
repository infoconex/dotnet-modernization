"""EXP-039 standard-library synthetic positive and adversarial regression tests."""
import base64
import hashlib
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from classic_pdb_document_checksums import (
    VerificationError, normalized_key, source_key,
    read_private_manifest, parse_injected_source, physical_files, verify_coverage,
    SHA256, SHA1,
)


def encoded_stream(source, algorithm=SHA256):
    alg_name = "sha256" if algorithm == SHA256 else "sha1"
    digest = hashlib.new(alg_name, source).digest()
    return (
        bytes(48) + algorithm.bytes_le + struct.pack("<ii", len(digest), 0) + digest
    )


class NativeWindowsPdbChecksumTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)
        self.physical = self.root / "Owned.cs"
        self.physical.write_bytes(b"public sealed class Owned { }\r\n")
        self.url = r"C:\physical\Owned.cs"
        self.key = source_key(self.url)
        self.native = {self.key: parse_injected_source(encoded_stream(self.physical.read_bytes()))}
        self.readers = {"DNLIB": {"Owned.cs": self.url},
                        "CECIL": {"Owned.cs": self.url}}
        self.sources = {"owned.cs": self.physical}

    def validate(self, native=None, readers=None, sources=None, required=None):
        return verify_coverage(
            self.native if native is None else native,
            self.readers if readers is None else readers,
            self.sources if sources is None else sources,
            ["Owned.cs"] if required is None else required,
        )

    def test_full_key_positive(self):
        r = self.validate()
        self.assertEqual(r["source_hashes_matched"], 1)
        self.assertEqual(r["unmatched_native_source_streams"], 0)
        self.assertEqual(r["inventory_completeness"],
                         "ALL_ENUMERATED_MANAGED_DOCS_AND_NATIVE_STREAMS")
        self.assertEqual(r["gate_c"], "NOT_EVALUATED_FOR_POLICY_REPLACEMENT")

    def test_mapped_slashes_match_full_key(self):
        readers = {"DNLIB": {"Owned.cs": "C:/physical/Owned.cs"},
                   "CECIL": {"Owned.cs": "c:/physical/owned.cs"}}
        r = self.validate(readers=readers)
        self.assertEqual(r["source_hashes_matched"], 1)

    def test_wrong_directory_not_basename_match(self):
        readers = {"DNLIB": {"Owned.cs": "C:/wrong/Owned.cs"},
                   "CECIL": {"Owned.cs": "C:/wrong/Owned.cs"}}
        with self.assertRaisesRegex(VerificationError, "WITHOUT_NATIVE"):
            self.validate(readers=readers)

    def test_unclassified_native_stream_reported_not_accepted(self):
        native = dict(self.native)
        native[source_key("/extra/Other.cs")] = None
        r = self.validate(native=native)
        self.assertEqual(r["unmatched_native_source_streams"], 1)
        self.assertEqual(r["unmatched_native_unrecognized_records"], 1)
        self.assertEqual(r["inventory_completeness"],
                         "INCOMPLETE_OR_UNCLASSIFIED_NATIVE_STREAMS")

    def test_reader_document_inventory_mismatch_fails(self):
        r = {"DNLIB": {"Owned.cs": self.url},
             "CECIL": {"Owned.cs": "/other/Owned.cs"}}
        with self.assertRaisesRegex(VerificationError, "DOCUMENT_SET_DISAGREEMENT"):
            self.validate(readers=r)

    def test_missing_document_in_one_reader_fails(self):
        r = {"DNLIB": {"Owned.cs": self.url}, "CECIL": {}}
        with self.assertRaises(VerificationError):
            self.validate(readers=r)

    def test_missing_physical_source_is_incomplete(self):
        r = self.validate(sources={}, required=[])
        self.assertEqual(r["reader_documents_without_supplied_physical_source"], 1)
        self.assertEqual(r["inventory_completeness"],
                         "INCOMPLETE_OR_UNCLASSIFIED_NATIVE_STREAMS")

    def test_required_document_missing_fails(self):
        with self.assertRaisesRegex(VerificationError, "REQUIRED_SELECTED_DOCUMENT"):
            self.validate(required=["Missing.cs"])

    def test_mutated_physical_source_fails(self):
        self.physical.write_bytes(self.physical.read_bytes() + b"\x00")
        with self.assertRaisesRegex(VerificationError, "CHECKSUM_VS_PHYSICAL"):
            self.validate()

    def test_modified_native_digest_fails(self):
        native = {self.key: parse_injected_source(encoded_stream(b"wrong bytes"))}
        with self.assertRaisesRegex(VerificationError, "CHECKSUM_VS_PHYSICAL"):
            self.validate(native=native)

    def test_missing_native_key_fails(self):
        with self.assertRaisesRegex(VerificationError, "WITHOUT_NATIVE"):
            self.validate(native={})

    def test_unsupported_digest_record_fails(self):
        with self.assertRaisesRegex(VerificationError, "UNSUPPORTED_OR_MALFORMED"):
            self.validate(native={self.key: None})

    def test_different_hash_algorithm_sha1_supported(self):
        native = {self.key: parse_injected_source(
            encoded_stream(self.physical.read_bytes(), SHA1)
        )}
        self.assertEqual(self.validate(native=native)["structured_digest_algorithm_counts"],
                         {"sha1": 1})

    def test_source_stream_checksum_length_truncation(self):
        stream = encoded_stream(self.physical.read_bytes())
        self.assertIsNone(parse_injected_source(stream[:-1]))
        self.assertIsNone(parse_injected_source(stream[:64] + struct.pack("<ii", 50, 0) + stream[72:]))

    def test_unsupported_digest_algorithm(self):
        stream = encoded_stream(b"abc")
        bad = stream[:48] + uuid.uuid4().bytes_le + stream[64:]
        self.assertIsNone(parse_injected_source(bad))

    def test_negative_source_size_fails(self):
        stream = encoded_stream(b"abc")
        self.assertIsNone(parse_injected_source(stream[:68] + struct.pack("<i", -1) + stream[72:]))

    def test_case_only_native_mapping_collisions_prohibited_by_casefold_index(self):
        self.assertEqual(normalized_key("/SRC/FILES/C:/Owned.cs"),
                         normalized_key("/src/files/c:\\Owned.cs"))

    def test_physical_colliding_basenames_rejected(self):
        second = self.root / "second" / "Owned.cs"
        second.parent.mkdir()
        second.write_bytes(b"b")
        with self.assertRaisesRegex(VerificationError, "COLLIDING_SOURCE_BASENAME"):
            physical_files([self.physical, second])

    def test_private_reader_manifest_b64_and_no_paths_in_report(self):
        f = self.root / "private.txt"
        data = base64.b64encode(self.url.encode()).decode()
        f.write_text("Owned.cs\t" + data + "\n")
        self.assertEqual(read_private_manifest(f)["Owned.cs"], self.url)

    def test_private_reader_manifest_duplicate_basename_rejected(self):
        f = self.root / "private.txt"
        data = base64.b64encode(self.url.encode()).decode()
        f.write_text("Owned.cs\t" + data + "\nOwned.cs\t" + data + "\n")
        with self.assertRaisesRegex(VerificationError, "DUPLICATE"):
            read_private_manifest(f)

    def test_private_reader_manifest_bad_encoded_url_rejected(self):
        f = self.root / "private.txt"
        f.write_text("Owned.cs\t%%bad\n")
        with self.assertRaisesRegex(VerificationError, "ENCODING"):
            read_private_manifest(f)


if __name__ == "__main__":
    unittest.main()
