import hashlib
import tempfile
import unittest
from pathlib import Path

from dia_source_checksum_assessment import OWNED_FILES, assess


class DiaChecksumAssessmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name) / "src" / "RecordSift.Infrastructure.Csv"
        self.directory.mkdir(parents=True)
        self.content = b"class C { }\r\n"
        for filename in OWNED_FILES:
            (self.directory / filename).write_bytes(self.content)

    def rows(self, contents=None, algorithm=3):
        digest = contents if contents is not None else hashlib.sha256(self.content).hexdigest()
        return [f"DOC|{name}|{algorithm}|{digest}" for name in OWNED_FILES] + ["COUNT|4|1"]

    def test_all_physical_crlf_bytes_match(self):
        self.assertEqual("PARTIALLY_VERIFIED", assess(self.rows(), self.tmp.name)["status"])

    def test_corrupt_source_digest_fails_closed(self):
        self.assertEqual("FAILED", assess(self.rows("0" * 64), self.tmp.name)["status"])

    def test_missing_dia_documents_is_inconclusive(self):
        self.assertEqual("INCONCLUSIVE", assess(["COUNT|0|1"], self.tmp.name)["status"])

    def test_unavailable_checksums_are_inconclusive(self):
        self.assertEqual("INCONCLUSIVE", assess(self.rows("", 0), self.tmp.name)["status"])

    def test_unknown_algorithm_is_not_assumed_sha(self):
        self.assertEqual("INCONCLUSIVE", assess(self.rows(algorithm=99), self.tmp.name)["status"])

    def test_duplicate_document_fails_closed(self):
        self.assertEqual("FAILED", assess(self.rows() + self.rows()[:1], self.tmp.name)["status"])

    def test_missing_count_fails_closed(self):
        self.assertEqual("FAILED", assess(self.rows()[:-1], self.tmp.name)["status"])

    def test_lf_only_digest_does_not_match_crlf_compiler_input(self):
        lf = hashlib.sha256(self.content.replace(b"\r\n", b"\n")).hexdigest()
        self.assertEqual("FAILED", assess(self.rows(lf), self.tmp.name)["status"])


if __name__ == "__main__":
    unittest.main()
