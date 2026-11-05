#!/usr/bin/env python3
"""Read-only, fail-closed inspection of pinned NuGet archives for EXP-036.

DOES NOT extract archives, load assemblies, execute package scripts, resolve
dependencies, or declare a package free of vulnerabilities.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import xml.etree.ElementTree as ET
import zipfile

PACKAGES = {
    "dnlib": {
        "version": "4.5.0",
        "assets": ("lib/net45/dnlib.dll",),
    },
    "Mono.Cecil": {
        "version": "0.11.6",
        "assets": ("lib/net40/Mono.Cecil.dll", "lib/net40/Mono.Cecil.Pdb.dll"),
    },
}
MAX_ARCHIVE_BYTES = 30 * 1024 * 1024
MAX_INFLATED_BYTES = 100 * 1024 * 1024
MAX_ENTRY_BYTES = 25 * 1024 * 1024
MAX_NUSPEC_BYTES = 256 * 1024


class InvalidPackage(ValueError):
    pass


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_entry(archive, info):
    digest = hashlib.sha256()
    with archive.open(info, "r") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_of(parent, name):
    node = parent.find("{*}" + name)
    return node.text.strip() if node is not None and node.text else None


def audit_package(path, package_id, *, max_archive_bytes=MAX_ARCHIVE_BYTES):
    expected = PACKAGES[package_id]
    path = Path(path)
    if not path.is_file() or path.stat().st_size > max_archive_bytes:
        raise InvalidPackage("missing or oversized package archive: " + package_id)
    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = archive.infolist()
            if len(infos) > 4096:
                raise InvalidPackage("too many archive entries")
            seen = set()
            files = {}
            total_size = 0
            for info in infos:
                name = info.filename.replace("\\", "/")
                p = PurePosixPath(name)
                if (not name or name.startswith("/") or ":" in name or
                        "." in p.parts or ".." in p.parts or "\x00" in name):
                    raise InvalidPackage("unsafe archive entry path")
                key = name.lower()
                if key in seen:
                    raise InvalidPackage("duplicate archive entry")
                seen.add(key)
                total_size += info.file_size
                if (info.file_size > MAX_ENTRY_BYTES or
                        total_size > MAX_INFLATED_BYTES or
                        info.flag_bits & 1):
                    raise InvalidPackage("oversized/encrypted archive contents")
                if not info.is_dir():
                    files[key] = info

            nuspecs = [info for key, info in files.items() if key.endswith(".nuspec")]
            if len(nuspecs) != 1 or nuspecs[0].file_size > MAX_NUSPEC_BYTES:
                raise InvalidPackage("expected exactly one small nuspec")
            xml = archive.read(nuspecs[0])
            root = ET.fromstring(xml)
            metadata = root.find("{*}metadata")
            if metadata is None:
                raise InvalidPackage("nuspec missing metadata")
            actual_id = text_of(metadata, "id")
            actual_version = text_of(metadata, "version")
            if actual_id != package_id or actual_version != expected["version"]:
                raise InvalidPackage("package id/version mismatch")
            for asset in expected["assets"]:
                if asset.lower() not in files:
                    raise InvalidPackage("missing expected managed reader asset: " + asset)
            # No package build/installation code may be executed. Flag even if present.
            dangerous = [name for name in files if name.endswith((".ps1", ".targets", ".props"))]
            if dangerous:
                raise InvalidPackage("unexpected installation/build scripts found")
            deps = []
            for group in metadata.findall(".//{*}dependencies/{*}group"):
                framework = group.attrib.get("targetFramework", "")
                for dep in group.findall("{*}dependency"):
                    deps.append({"framework": framework, "id": dep.attrib.get("id", ""),
                                 "version": dep.attrib.get("version", "")})
            for dep in metadata.findall("./{*}dependencies/{*}dependency"):
                deps.append({"framework": "", "id": dep.attrib.get("id", ""),
                             "version": dep.attrib.get("version", "")})
            assets = [{"path": asset,
                       "bytes": files[asset.lower()].file_size,
                       "sha256": sha256_entry(archive, files[asset.lower()])}
                      for asset in expected["assets"]]
            return {
                "package_id": actual_id,
                "version": actual_version,
                "archive_bytes": path.stat().st_size,
                "archive_sha256": sha256_file(path),
                "nuspec_sha256": hashlib.sha256(xml).hexdigest(),
                "authors": text_of(metadata, "authors"),
                "assets": assets,
                "declared_dependencies": deps,
                "entry_count": len(infos),
                "security_review": "PENDING; static archive preflight is not a vulnerability audit",
            }
    except (OSError, zipfile.BadZipFile, ET.ParseError, RuntimeError) as exc:
        raise InvalidPackage("archive could not be safely inspected") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dnlib", required=True, type=Path)
    parser.add_argument("--cecil", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = {
        "status": "ARCHIVE_METADATA_ONLY",
        "reader_execution": "NOT RUN",
        "managed_checksum_gate": "INCONCLUSIVE",
        "packages": [audit_package(args.dnlib, "dnlib"),
                     audit_package(args.cecil, "Mono.Cecil")],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Archive-only preflight passed; no PDB reader executed; security review pending.")


if __name__ == "__main__":
    try:
        main()
    except InvalidPackage as exc:
        print("EXP-036 PRE-FLIGHT BLOCKED: " + str(exc), file=sys.stderr)
        sys.exit(1)
