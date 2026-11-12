import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compatibility
import package_payload


class PackagePayloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = self.root / 'baseline.nupkg'
        self.changed = self.root / 'candidate.nupkg'
        self.manifest = (b'<package><metadata><id>Demo</id><version>1.0.0</version>'
                         b'</metadata></package>')

    def package(self, path, dll=b'\x00\x01\x02', extra=None, timestamp=(2020, 1, 1, 0, 0, 0)):
        with zipfile.ZipFile(path, 'w') as archive:
            for name, data in [('demo.nuspec', self.manifest),
                               ('lib/net48/Demo.dll', dll)] + (extra or []):
                info = zipfile.ZipInfo(name, date_time=timestamp)
                archive.writestr(info, data)

    def test_same_package_is_identical(self):
        self.package(self.original)
        report = package_payload.compare_packages(self.original, self.original)
        self.assertEqual(report['overall'], 'identical_archive_and_entries')
        self.assertEqual(report['changed_member_count'], 0)
        self.assertTrue(report['member_path_sets_match'])
        self.assertEqual(len(report['baseline']['archive_sha256']), 64)

    def test_actual_member_bytes_detected_despite_unchanged_legacy_contract(self):
        self.package(self.original, b'\x00\x01\x02')
        self.package(self.changed, b'\x00\x01\x03')
        report = package_payload.compare_packages(self.original, self.changed)
        self.assertEqual(report['overall'], 'different_entries')
        self.assertEqual(len(report['entry_differences']), 1)
        self.assertEqual(report['entry_differences'][0]['path'], 'lib/net48/Demo.dll')
        self.assertEqual(report['entry_differences'][0]['kind'], 'bytes_changed')
        self.assertEqual(compatibility.package_contract(self.original),
                         compatibility.package_contract(self.changed))

    def test_container_metadata_only_does_not_imply_payload_change(self):
        self.package(self.original, timestamp=(2020, 1, 1, 0, 0, 0))
        self.package(self.changed, timestamp=(2021, 1, 1, 0, 0, 0))
        report = package_payload.compare_packages(self.original, self.changed)
        self.assertEqual(report['overall'], 'different_container_same_entries')
        self.assertEqual(report['changed_member_count'], 0)
        self.assertNotEqual(report['baseline']['archive_sha256'],
                            report['candidate']['archive_sha256'])

    def test_new_or_removed_member_detected(self):
        self.package(self.original)
        self.package(self.changed, extra=[('lib/net48/Other.dll', b'new')])
        report = package_payload.compare_packages(self.original, self.changed)
        self.assertEqual(report['overall'], 'different_entries')
        self.assertFalse(report['member_path_sets_match'])
        self.assertEqual(report['entry_differences'][0]['kind'], 'added')
        report_reverse = package_payload.compare_packages(self.changed, self.original)
        self.assertEqual(report_reverse['entry_differences'][0]['kind'], 'removed')

    def test_missing_required_package_is_incomplete(self):
        self.package(self.original)
        self.assertEqual(package_payload.compare_packages(self.original, self.changed)['overall'], 'incomplete')

    def test_malformed_zip_fails_closed(self):
        self.package(self.original)
        self.changed.write_bytes(b'not a zip file')
        self.assertEqual(package_payload.compare_packages(self.original, self.changed)['overall'], 'error')

    def test_rejects_path_traversal(self):
        self.package(self.original)
        self.package(self.changed, extra=[('../escaped.dll', b'x')])
        self.assertEqual(package_payload.compare_packages(self.original, self.changed)['overall'], 'error')

    def test_rejects_duplicate_case_folded_names(self):
        self.package(self.original)
        self.package(self.changed, extra=[('LIB/net48/demo.dll', b'x')])
        self.assertEqual(package_payload.compare_packages(self.original, self.changed)['overall'], 'error')

    def test_rejects_duplicate_exact_names(self):
        self.package(self.original)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            self.package(self.changed, extra=[('lib/net48/Demo.dll', b'x')])
        self.assertEqual(package_payload.compare_packages(self.original, self.changed)['overall'], 'error')

    def test_rejects_symlink(self):
        self.package(self.original)
        with zipfile.ZipFile(self.changed, 'w') as archive:
            archive.writestr('demo.nuspec', self.manifest)
            link = zipfile.ZipInfo('lib/net48/Demo.dll')
            link.create_system = 3
            link.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(link, b'other-location')
        self.assertEqual(package_payload.compare_packages(self.original, self.changed)['overall'], 'error')

    def test_rejects_missing_root_manifest(self):
        with zipfile.ZipFile(self.original, 'w') as archive:
            archive.writestr('lib/net48/Demo.dll', b'x')
        self.assertEqual(package_payload.compare_packages(self.original, self.original)['overall'], 'error')

    def test_rejects_expansion_limits(self):
        self.package(self.original)
        self.package(self.changed, dll=b'x' * 64)
        with mock.patch.object(package_payload, 'MAX_MEMBER_BYTES', 32):
            self.assertEqual(package_payload.compare_packages(self.original, self.changed)['overall'], 'error')

    def test_cli_exit_codes_and_report(self):
        self.package(self.original)
        self.package(self.changed, dll=b'\x00')
        output = self.root / 'report.json'
        cmd = [sys.executable, str(Path(package_payload.__file__)), '--baseline',
               str(self.original), '--candidate', str(self.changed), '--output', str(output)]
        first = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(first.returncode, 1, first.stderr)
        self.assertEqual(json.loads(output.read_text(encoding='utf-8'))['overall'], 'different_entries')
        second = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn('already exists', second.stderr)

    def test_cli_missing_package_is_incomplete_and_fails(self):
        self.package(self.original)
        output = self.root / 'missing.json'
        args = [sys.executable, str(Path(package_payload.__file__)), '--baseline',
                str(self.original), '--candidate', str(self.changed), '--output', str(output)]
        done = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(done.returncode, 1)
        self.assertEqual(json.loads(output.read_text(encoding='utf-8'))['overall'], 'incomplete')


if __name__ == '__main__':
    unittest.main()
