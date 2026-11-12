"""Offline synthetic archive controls; no real package execution."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("exp036", HERE / "nuget_reader_preflight.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class ArchiveControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pkg = Path(self.temp.name) / "fixture.nupkg"

    def write(self, package_id="dnlib", version="4.5.0", *, asset=True,
              extra_name=None, extra_bytes=b"test"):
        ns = '<?xml version="1.0"?><package><metadata><id>' + package_id
        ns += '</id><version>' + version + '</version><authors>fixture</authors>'
        ns += '<dependencies /></metadata></package>'
        with zipfile.ZipFile(self.pkg, "w") as z:
            z.writestr(package_id + ".nuspec", ns)
            if asset:
                z.writestr("lib/net45/dnlib.dll", b"fixture managed DLL")
            if extra_name:
                z.writestr(extra_name, extra_bytes)

    def test_good_mock(self):
        self.write()
        out = audit.audit_package(self.pkg, "dnlib")
        self.assertEqual(out["version"], "4.5.0")
        self.assertEqual(len(out["assets"]), 1)
        self.assertEqual(out["security_review"].split(";")[0], "PENDING")

    def test_reject_typosquat_identity(self):
        self.write(package_id="dnlib.net")
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "dnlib")

    def test_reject_wrong_version(self):
        self.write(version="4.0.0")
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "dnlib")

    def test_reject_missing_managed_asset(self):
        self.write(asset=False)
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "dnlib")

    def test_reject_traversal(self):
        self.write(extra_name="../escape.txt")
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "dnlib")

    def test_reject_install_scripts(self):
        self.write(extra_name="tools/install.ps1")
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "dnlib")

    def test_reject_duplicate_paths(self):
        self.write(extra_name="LIB/NET45/DNLIB.DLL")
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "dnlib")

    def test_reject_oversized_archive(self):
        self.write()
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "dnlib", max_archive_bytes=1)

    def test_cecil_requires_two_assets(self):
        self.write(package_id="Mono.Cecil", version="0.11.6")
        with self.assertRaises(audit.InvalidPackage):
            audit.audit_package(self.pkg, "Mono.Cecil")


if __name__ == "__main__":
    unittest.main()
