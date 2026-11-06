"""EXP-043 independent managed-reader exposure, privacy and native-universe controls."""
import base64
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp043_managed_reader_exposure import read_managed, audit, VerificationError
from exp043_five_pdb_audit import COMPONENTS


def write_reader(root, component, reader, entries):
    manifest = []
    rows = []
    matched = missing = 0
    for name, full, digest in entries:
        manifest.append(name+"\t"+base64.b64encode(full.encode()).decode())
        if digest is None:
            rows.append("MISSING\t"+name)
            missing += 1
        else:
            rows.append("DOC\t"+name+"\t8829d00f-11b8-4213-878b-770e8597ac16\t"+digest)
            matched += 1
    rows.append(f"END\t{matched}\t{missing}")
    prefix = root/(component+"-"+reader)
    (Path(str(prefix)+"-urls.private")).write_text("\n".join(manifest)+"\n",encoding="utf-8")
    (Path(str(prefix)+"-stdout.private")).write_text("\n".join(rows)+"\n",encoding="utf-8")


class ManagedReaderExposureTests(unittest.TestCase):
    def test_reader_parsing_exposes_only_counts_and_full_normalized_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            doc="C:/very/private/Class.cs"
            write_reader(root,"Domain","DNLIB",[("Class.cs",doc,None)])
            keys,stat=read_managed(root,"Domain","DNLIB")
            self.assertEqual(keys,{"/src/files/"+doc.casefold()})
            self.assertEqual(stat,{"managed_document_count":1,
                    "managed_document_checksum_exposed":0,
                    "managed_document_checksum_missing":1})
            self.assertNotIn(doc,str(stat))

    def test_duplicate_document_or_malformed_missing_end_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            source="C:/private/A.cs"
            write_reader(root,"Domain","CECIL",[("A.cs",source,None)])
            p=root/"Domain-CECIL-stdout.private"
            p.write_text("MISSING\tA.cs\nMISSING\tA.cs\nEND\t0\t2\n",encoding="utf-8")
            with self.assertRaises(VerificationError):
                read_managed(root,"Domain","CECIL")
            write_reader(root,"Domain","CECIL",[("A.cs",source,None)])
            p.write_text("MISSING\tA.cs\nEND\t0\t2\n",encoding="utf-8")
            with self.assertRaises(VerificationError):
                read_managed(root,"Domain","CECIL")

    def test_all_five_reader_consensus_and_unexposed_native_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            input_root=root/"private-readers"
            input_root.mkdir()
            for component in COMPONENTS:
                for reader in ("DNLIB","CECIL"):
                    write_reader(input_root,component,reader,
                                 [("A.cs","C:/private/A.cs",None)])
            native={"/src/files/c:/private/a.cs":{},
                    "/src/files/c:/private/generated.cs":{}}
            dbi={"dbi":set(native),"c13":set(native)}
            with mock.patch("exp043_managed_reader_exposure.source_pdb_inventory",
                            return_value=(native,dbi)):
                result=audit(root/"app",input_root)
                self.assertTrue(result["all_five_readers_audited"])
                self.assertEqual(len(result["results"]),5)
                self.assertTrue(all(x["native_documents_not_exposed_by_both_readers"]==1
                                    for x in result["results"]))
                self.assertNotIn("private",str(result["results"]).lower().replace(
                    "private", ""))  # No source/path payload permitted.
                bad={**dbi,"c13":set()}
                with mock.patch("exp043_managed_reader_exposure.source_pdb_inventory",
                                return_value=(native,bad)):
                    mismatch=audit(root/"app",input_root)
                    self.assertFalse(mismatch["all_five_readers_audited"])
                    self.assertTrue(all(x["status"]=="BLOCKED" for x in mismatch["results"]))

    def test_non_verification_exception_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("exp043_managed_reader_exposure.source_pdb_inventory",
                            side_effect=OSError(tmp+"/private-source.cs")):
                result=audit(Path(tmp),Path(tmp))
                self.assertFalse(result["all_five_readers_audited"])
                self.assertNotIn(tmp,str(result))
                self.assertTrue(all(x["failure_category"]==
                    "MANAGED_READER_AUDIT_FAILED_CLOSED" for x in result["results"]))


if __name__=="__main__":
    unittest.main()
