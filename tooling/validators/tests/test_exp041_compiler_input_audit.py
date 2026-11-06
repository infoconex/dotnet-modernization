"""EXP-041 independent private input and fail-closed mapping controls."""
import base64
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp041_compiler_input_audit import (
    VerificationError, parse_pathmap, apply_pathmap, read_capture, verify,
)


def record(data):
    return {"algorithm": "sha256", "digest": hashlib.sha256(data).digest()}


class CompilerInputsTests(unittest.TestCase):
    def test_full_pathmap_not_basename(self):
        mapping = parse_pathmap(r"C:\source=/_/,C:\source\other=/second")
        self.assertEqual(apply_pathmap(r"C:\source\src\A.cs", mapping),
                         "/_/src/A.cs")
        self.assertEqual(apply_pathmap(r"C:\source\other\A.cs", mapping),
                         "/second/A.cs")
        self.assertNotEqual(apply_pathmap(r"C:\different\A.cs", mapping), "/_/A.cs")

    def test_duplicate_mapping_rejected(self):
        with self.assertRaises(VerificationError):
            parse_pathmap(r"C:\src=/_/,c:\src=/other")

    def test_malformed_mapping_rejected(self):
        with self.assertRaises(VerificationError):
            parse_pathmap("not-a-pathmap")

    def test_private_capture_preserves_raw_bom_crlf_and_detects_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            physical = root / "a.cs"
            data = b"\xef\xbb\xbfclass A {}\r\n"
            physical.write_bytes(data)
            (root / "input-0000.bin").write_bytes(data)
            manifest = "PATHMAP\t" + base64.b64encode(b"").decode() + "\n"
            manifest += "0\t" + base64.b64encode(str(physical).encode()).decode()
            manifest += "\t" + hashlib.sha256(data).hexdigest() + "\n"
            (root / "input-manifest.tsv").write_text(manifest, encoding="ascii")
            rows, _ = read_capture(root)
            self.assertEqual(rows[0][1], data)
            (root / "input-0000.bin").write_bytes(b"changed")
            with self.assertRaises(VerificationError):
                read_capture(root)

    def test_all_native_inputs_and_origin_categorization(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / "sample.cs"
            p.write_bytes(b"one\r\n")
            n = "/src/files/" + str(p).replace("\\", "/").casefold()
            dbi = {"status":"DBI_PARSED", "dbi":{n}, "c13":{n},
                   "lines":set(), "c13_algorithm_counts":{"NONE":1}}
            result = verify({n: record(b"one\r\n")}, dbi, [(p, b"one\r\n", str(p))], root)
            self.assertEqual(result["original_input_sha256_or_sha1_matches"], 1)
            self.assertEqual(result["gate_c"], "UNSATISFIED")

    def test_missing_input_is_incomplete_not_passed(self):
        with tempfile.TemporaryDirectory() as d:
            n = "/src/files/a"
            dbi = {"status":"DBI_PARSED", "dbi":{n}, "c13":{n},
                   "lines":set(), "c13_algorithm_counts":{"NONE":1}}
            result = verify({n: record(b"abc")}, dbi, [], Path(d))
            self.assertEqual(result["native_inventory"], "INCOMPLETE")

    def test_stale_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a"
            p.write_bytes(b"wrong")
            n = "/src/files/" + str(p).casefold()
            dbi = {"status":"DBI_PARSED", "dbi":{n}, "c13":{n},
                   "lines":set(), "c13_algorithm_counts":{"NONE":1}}
            with self.assertRaises(VerificationError):
                verify({n: record(b"right")}, dbi, [(p, b"wrong", str(p))], Path(d))

    def test_same_basename_different_paths_is_independent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            a, b = root/"one"/"A.cs", root/"two"/"A.cs"
            a.parent.mkdir()
            b.parent.mkdir()
            a.write_bytes(b"a")
            b.write_bytes(b"b")
            na = "/src/files/"+str(a).casefold()
            nb = "/src/files/"+str(b).casefold()
            dbi = {"status":"DBI_PARSED", "dbi":{na,nb}, "c13":{na,nb},
                   "lines":set(), "c13_algorithm_counts":{"NONE":2}}
            result = verify({na:record(b"a"),nb:record(b"b")}, dbi,
                            [(a,b"a",str(a)),(b,b"b",str(b))], root)
            self.assertEqual(result["original_input_sha256_or_sha1_matches"],2)

    def test_unmatched_compiler_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a"
            p.write_bytes(b"a")
            with self.assertRaises(VerificationError):
                verify({}, {"status":"DBI_PARSED", "dbi":set(), "c13":set(),
                            "lines":set(), "c13_algorithm_counts":{}},
                       [(p,b"a",str(p))], Path(d))

    def test_wrong_dbi_and_algorithm_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            n = "/src/files/a"
            d0 = {"status":"DBI_PARSED", "dbi":set(), "c13":{n},
                  "lines":set(), "c13_algorithm_counts":{}}
            with self.assertRaises(VerificationError):
                verify({n:record(b"a")},d0,[],Path(d))
            d0["dbi"] = {n}
            with self.assertRaises(VerificationError):
                verify({n:{"algorithm":"md5","digest":b"0"}},d0,[],Path(d))

    def test_duplicate_mapped_identifiers_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p, q = Path(d)/"a.cs", Path(d)/"b.cs"
            key = "/src/files/" + str(p).casefold()
            dbi = {"status":"DBI_PARSED", "dbi":{key}, "c13":{key},
                   "lines":set(), "c13_algorithm_counts":{}}
            with self.assertRaises(VerificationError):
                verify({key:record(b"x")},dbi,
                       [(p,b"x",str(p)),(q,b"x",str(p))],Path(d))


if __name__ == "__main__":
    unittest.main()
