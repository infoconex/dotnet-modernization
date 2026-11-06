"""EXP-042 privacy-preserving independent Csc-task and generator controls."""
import base64
import hashlib
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from exp042_source_provenance import (
    VerificationError, windows_identity, csc_source_parameter,
    compare_task_sources, producer_record, declared_source_binding,
    read_structured_csc_events,
)


class ProvenanceControls(unittest.TestCase):
    def test_windows_relative_source_identity(self):
        self.assertEqual(windows_identity(r"Properties\AssemblyInfo.cs",
                                          Path(r"C:\project")),
                         "c:/project/properties/assemblyinfo.cs")

    def test_task_sources_list_and_metadata(self):
        log=('Task "Csc" (TaskId:17):\n'
             '  Task Parameter:Sources=\n'
             '     Properties\\AssemblyInfo.cs\n'
             '       FullPath=C:\\private\\AssemblyInfo.cs\n'
             '     obj\\Release\\.NETFramework,Version=v4.8.AssemblyAttributes.cs\n'
             '  Task Parameter:References=System.dll\n'
             'Done executing task "Csc".\n')
        found,cat=csc_source_parameter(log)
        self.assertEqual(cat,"CSC_TASK_SOURCES_OBSERVED")
        self.assertEqual(len(found),2)
        self.assertTrue(any("AssemblyAttributes.cs" in x for x in found))

    def test_missing_or_multiple_csc_task_inconclusive(self):
        self.assertIsNone(csc_source_parameter('nothing')[0])
        a='Task "Csc"\nTask Parameter:Sources=a.cs\nDone executing task "Csc".\n'
        self.assertIsNone(csc_source_parameter(a+a)[0])

    def test_mismatch_duplicate_and_match(self):
        root=Path(r"C:\project")
        p=Path(r"C:\project\a.cs")
        records=[(p,b"a",str(p))]
        # On non-Windows Path cannot normalize Windows UNC paths but our
        # verifier explicitly uses ntpath for compiler identity resolution.
        status,count=compare_task_sources(["a.cs"],records,root)
        self.assertEqual((status,count),("MATCHED_INDEPENDENT_TASK_PARAMETER",1))
        with self.assertRaises(VerificationError):
            compare_task_sources(["a.cs","a.cs"],records,root)
        with self.assertRaises(VerificationError):
            compare_task_sources(["other.cs"],records,root)

    def test_exact_preprocessed_corecompile_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            x=Path(tmp)/"pp.xml"
            x.write_text('<Project><Target Name="CoreCompile">'
                         '<Csc Sources="@(Compile)" /></Target></Project>',encoding="utf-8")
            self.assertEqual(declared_source_binding(x),
                             "CORECOMPILE_CSC_USES_COMPILE_ITEMS")
            x.write_text('<Project><Target Name="CoreCompile">'
                         '<Csc Sources="@(Else)" /></Target></Project>',encoding="utf-8")
            with self.assertRaises(VerificationError):
                declared_source_binding(x)

    def test_target_observation_not_inferred_from_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            project=Path(r"C:\project")
            generated=Path(r"C:\project\obj\Release\generated.AssemblyAttributes.cs")
            data=b"generated\r\n"
            p=root/"producer"
            p.mkdir()
            (p/"producer-before.flag").write_bytes(b"PREPARED_ABSENT")
            (p/"producer-after.tsv").write_text(
                "PRODUCER\t"+base64.b64encode(str(generated).encode()).decode()
                +"\t"+hashlib.sha256(data).hexdigest()+"\n",encoding="ascii")
            res=producer_record(p,[(generated,data,str(generated))],project,"")
            self.assertEqual(res["producer_status"],"INCONCLUSIVE_TASK_EXECUTION_NOT_OBSERVED")
            log=('Target "GenerateTargetFrameworkMonikerAttribute" in file "X":\n'
                 '    Task "WriteLinesToFile"\n'
                 '    Done executing task "WriteLinesToFile".\n'
                 'Done building target "GenerateTargetFrameworkMonikerAttribute".')
            self.assertEqual(
                producer_record(p,[(generated,data,str(generated))],project,log)
                  ["producer_status"],"VERIFIED_TARGET_EXECUTION_AND_BYTES")
            with self.assertRaises(VerificationError):
                producer_record(p,[(generated,b"tampered",str(generated))],project,log)
            (p/"producer-before.flag").write_bytes(b"PREEXISTING")
            with self.assertRaises(VerificationError):
                producer_record(p,[(generated,data,str(generated))],project,log)


    def test_structured_event_exact_input_and_fail_closed_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private = root / "csc-structured-private.tsv"
            value = r"C:\project\src\A.cs"
            private.write_text("STATUS\tCSC_TASK_PARAMETER_EVENT\n"
                               "COUNT\t1\n" +
                               base64.b64encode(value.encode()).decode() + "\n",
                               encoding="ascii")
            found, category = read_structured_csc_events(private)
            self.assertEqual(found, [value])
            self.assertEqual(category, "STRUCTURED_CSC_TASK_INPUT_EVENT")
            status, count = compare_task_sources(
                found, [(Path(value), b"a", value)], Path(r"C:\project"))
            self.assertEqual((status, count),
                             ("MATCHED_INDEPENDENT_TASK_PARAMETER", 1))
            private.write_text("STATUS\tCSC_TASK_PARAMETER_EVENT\nCOUNT\t2\n"
                               + base64.b64encode(value.encode()).decode()+"\n",
                               encoding="ascii")
            with self.assertRaises(VerificationError):
                read_structured_csc_events(private)
            private.write_text("STATUS\tNO_UNIQUE_CSC_SOURCE_EVENT\n",
                               encoding="ascii")
            found, state = read_structured_csc_events(private)
            self.assertIsNone(found)
            self.assertEqual(state, "INCONCLUSIVE_NO_UNIQUE_CSC_EVENT")

if __name__=="__main__":
    unittest.main()
