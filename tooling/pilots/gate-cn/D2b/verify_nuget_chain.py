#!/usr/bin/env python3
"""D2b: actual locally packaged NuGet restore & .NET Framework CLR identity.

ONE approved public disposable traditional net48 library, two defined variants,
ONE disposable SDK net48 PackageReference consumer. No internet package sources,
no real RecordSift assemblies, no release gate. All binary hashes stay private.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

VALIDATORS = Path(__file__).resolve().parents[3] / "validators"
sys.path.insert(0, str(VALIDATORS))
from native_windows_pdb_sourcelink import read_msf, parse_named_streams, read_pe_codeview

PACKAGE_ID = "D2b.Disposable"
PACKAGE_LOW = PACKAGE_ID.lower()
VERSION = "0.1.0"
ARCHIVE = PACKAGE_ID + "." + VERSION + ".nupkg"
LIB_MEMBER = "lib/net48/D2a.Probe.dll"

NUSPEC = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
 <metadata>
  <id>D2b.Disposable</id>
  <version>0.1.0</version>
  <authors>GateCNResearch</authors>
  <description>Disposable local-feed net48 identity evidence, never publish.</description>
  <dependencies><group targetFramework=".NETFramework4.8" /></dependencies>
 </metadata>
</package>
"""
CONTENT_TYPES = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml" />
 <Default Extension="nuspec" ContentType="application/octet" />
 <Default Extension="dll" ContentType="application/octet" />
</Types>
"""
PACKAGE_RELS = """<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Type="http://schemas.microsoft.com/packaging/2010/07/manifest"
 Id="R1" Target="/D2b.Disposable.nuspec" />
</Relationships>
"""


class Rejected(ValueError):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def require(condition, code):
    if not condition:
        raise Rejected(code)


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def real_pair(dll, pdb):
    try:
        data = read_msf(pdb.read_bytes())
        guid, age, _ = parse_named_streams(data[1], len(data))
        require(read_pe_codeview(dll.read_bytes()) == (guid, age),
                "D2B_REAL_PE_PDB_PAIR_MISMATCH")
    except Rejected:
        raise
    except (OSError, ValueError, IndexError, TypeError, OverflowError):
        raise Rejected("D2B_REAL_PE_PDB_UNAVAILABLE") from None


def make_nupkg(destination, dll_bytes):
    """Standards-format, disposable OPC ZIP/Nuspec NuGet package, not nuget.exe pack."""
    require(not destination.exists(), "D2B_REUSED_PACKAGE_DESTINATION")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "x", zipfile.ZIP_DEFLATED) as pkg:
        pkg.writestr("[Content_Types].xml", CONTENT_TYPES)
        pkg.writestr("_rels/.rels", PACKAGE_RELS)
        pkg.writestr(PACKAGE_ID + ".nuspec", NUSPEC)
        pkg.writestr(LIB_MEMBER, dll_bytes)
    with zipfile.ZipFile(destination, "r") as pkg:
        require(pkg.testzip() is None and pkg.namelist().count(LIB_MEMBER) == 1,
                "D2B_ARCHIVE_FORMAT_INVALID")
    return destination


def archive_member_sha(package):
    with zipfile.ZipFile(package, "r") as pkg:
        members = pkg.namelist()
        require(members.count(LIB_MEMBER) == 1 and
                members.count(PACKAGE_ID + ".nuspec") == 1,
                "D2B_ARCHIVE_CONTENT_UNEXPECTED")
        return hashlib.sha256(pkg.read(LIB_MEMBER)).hexdigest()


def verify_member(package, expected):
    require(archive_member_sha(package) == expected,
            "D2B_PACKAGE_DLL_HASH_MISMATCH")
    return True


def verify_archive(candidate, approved):
    require(file_sha(candidate) == approved, "D2B_PACKAGE_ARCHIVE_SHA_MISMATCH")
    return True


def cache_paths(root):
    cache = root / PACKAGE_LOW / VERSION
    return cache / (PACKAGE_LOW + "." + VERSION + ".nupkg"), cache / LIB_MEMBER


def verify_cache_archive(cache, approved):
    archive, _ = cache_paths(cache)
    require(archive.is_file(), "D2B_INSTALLED_NUPKG_MISSING")
    return verify_archive(archive, approved)


def verify_cache_dll(cache, approved):
    _, lib = cache_paths(cache)
    require(lib.is_file() and file_sha(lib) == approved,
            "D2B_RESTORED_DLL_HASH_MISMATCH")
    return True


def verify_copy_local(path, approved):
    require(path.is_file() and file_sha(path) == approved,
            "D2B_CONSUMER_COPY_HASH_MISMATCH")
    return True


def run_subprocess(argv, code, *, cwd=None, timeout=120):
    # Capture all external output privately. No raw console output or command
    # line, including NuGet config paths, passes to the public CI log.
    environment = os.environ.copy()
    environment["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1"
    environment["DOTNET_NOLOGO"] = "1"
    try:
        p = subprocess.run(argv, cwd=cwd, text=True, capture_output=True,
                           timeout=timeout, check=False, env=environment)
    except (OSError, subprocess.TimeoutExpired):
        raise Rejected(code) from None
    require(p.returncode == 0, code)
    return p.stdout.strip()


def consumer_root(private, label, template, feed):
    root = private / ("consumer-" + label)
    require(not root.exists(), "D2B_CONSUMER_ROOT_REUSED")
    shutil.copytree(template, root)
    cache = private / ("nuget-global-" + label)
    require(not cache.exists(), "D2B_NUGET_CACHE_NOT_FRESH")
    config = root / "NuGet.Config"
    # No inherited default feeds and no NuGet.org fallback. The absolute path
    # remains in ephemeral private config; never echoed to artifact/log.
    path = str(feed.resolve()).replace("&", "&amp;").replace('"', "&quot;")
    config.write_text("""<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources><clear /><add key="isolated" value="%s" /></packageSources>
  <disabledPackageSources><clear /></disabledPackageSources>
</configuration>
""" % path, encoding="utf-8")
    return root, cache, config


def actual_restore(root, cache, config):
    project = root / "D2b.Consumer.csproj"
    run_subprocess(["dotnet", "restore", str(project),
                    "--configfile", str(config), "--packages", str(cache),
                    "--force", "--no-cache", "-p:NuGetAudit=false",
                    "-p:RestoreIgnoreFailedSources=false", "--verbosity", "quiet"],
                   "D2B_REAL_NUGET_RESTORE_FAILED", cwd=root)
    archive, lib = cache_paths(cache)
    require(archive.is_file() and lib.is_file(),
            "D2B_REAL_NUGET_PACKAGE_CACHE_MISSING")
    # Verify actual NuGet assets references approved package ID/version.
    assets = json.loads((root / "obj" / "project.assets.json").read_text(
        encoding="utf-8"))
    require(PACKAGE_ID + "/" + VERSION in assets.get("libraries", {}),
            "D2B_NUGET_ASSETS_IDENTITY_MISSING")
    return archive, lib


def build_consumer(root):
    project = root / "D2b.Consumer.csproj"
    run_subprocess(["dotnet", "build", str(project), "-c", "Release",
                    "--no-restore", "--nologo", "--verbosity", "quiet"],
                   "D2B_REAL_NUGET_CONSUMER_BUILD_FAILED", cwd=root)
    output = root / "bin" / "Release" / "net48"
    consumer = output / "D2b.Consumer.dll"
    dll = output / "D2a.Probe.dll"
    require(consumer.is_file() and dll.is_file(),
            "D2B_REAL_NUGET_COPY_LOCAL_MISSING")
    return consumer, dll


def loaded(runtime, consumer):
    p = run_subprocess(["powershell.exe", "-NoProfile", "-NonInteractive",
                        "-ExecutionPolicy", "Bypass", "-File", str(runtime),
                        "-ConsumerPath", str(consumer)],
                       "D2B_ACTUAL_CLR_CONSUMER_FAILED", timeout=40)
    try:
        result = json.loads(p)
        location = Path(result["loaded_location"]).resolve()
        require(location.is_file(), "D2B_CLR_LOADED_MODULE_MISSING")
        require(len(result["module_mvid"]) == 36 and
                isinstance(result["method_value"], int),
                "D2B_CLR_OBSERVATION_INVALID")
        require(location.name.casefold() == "d2a.probe.dll",
                "D2B_CLR_WRONG_ASSEMBLY_LOADED")
        result["observed_sha256"] = file_sha(location)
        return result
    except (KeyError, ValueError, TypeError):
        raise Rejected("D2B_CLR_OBSERVATION_INVALID") from None


def verify_loaded(result, approved, expected_value):
    require(result["observed_sha256"] == approved and
            result["method_value"] == expected_value,
            "D2B_CLR_LOADED_DLL_HASH_MISMATCH")
    return True


def negative(name, expected, callback, results):
    try:
        callback()
    except Rejected as e:
        require(e.code == expected, "D2B_WRONG_NEGATIVE_FAILURE_STAGE")
        results.append({
            "id": name,
            "status": "PASS",
            "expected": expected,
            "observed": e.code,
            "paired_positive": "PASS",
        })
        return
    raise Rejected("D2B_NEGATIVE_WAS_ACCEPTED")


def run(root, template, runtime):
    a, b = root / "variant-a", root / "variant-b"
    dll_a, pdb_a = a / "D2a.Probe.dll", a / "D2a.Probe.pdb"
    dll_b, pdb_b = b / "D2a.Probe.dll", b / "D2a.Probe.pdb"
    require(all(p.is_file() for p in (dll_a, pdb_a, dll_b, pdb_b)),
            "D2B_ACTUAL_COMPILER_OUTPUT_MISSING")
    real_pair(dll_a, pdb_a)
    real_pair(dll_b, pdb_b)
    approved_sha, alternate_sha = file_sha(dll_a), file_sha(dll_b)
    require(approved_sha != alternate_sha, "D2B_COMPILER_VARIANTS_SAME_DLL")

    feed_a, feed_b = root / "local-feed-a", root / "local-feed-b"
    pkg_a = make_nupkg(feed_a / ARCHIVE, dll_a.read_bytes())
    pkg_b = make_nupkg(feed_b / ARCHIVE, dll_b.read_bytes())
    mixed = make_nupkg(root / "mixed-feed" / ARCHIVE, dll_b.read_bytes())
    require(file_sha(pkg_a) != file_sha(pkg_b),
            "D2B_PACKAGES_NOT_DISTINCT")
    approved_archive_sha = file_sha(pkg_a)
    assert verify_archive(pkg_a, approved_archive_sha)
    assert verify_member(pkg_a, approved_sha)
    assert verify_member(pkg_b, alternate_sha)

    results = []
    negative("D2b-N01", "D2B_PACKAGE_DLL_HASH_MISMATCH",
             lambda: verify_member(mixed, approved_sha), results)

    consumer_a, cache_a, config_a = consumer_root(
        root, "a", template, feed_a)
    consumer_b, cache_b, config_b = consumer_root(
        root, "b", template, feed_b)

    restored_a_archive, restored_a_lib = actual_restore(
        consumer_a, cache_a, config_a)
    assert verify_cache_archive(cache_a, approved_archive_sha)
    assert verify_cache_dll(cache_a, approved_sha)
    require(file_sha(restored_a_archive) == approved_archive_sha,
            "D2B_APPROVED_ARCHIVE_CUSTODY_MISMATCH")

    # Actual separate NuGet restore from alternate feed with same ID/version,
    # clean alternate cache: source selection is not mocked.
    restored_b_archive, restored_b_lib = actual_restore(
        consumer_b, cache_b, config_b)
    assert verify_cache_archive(cache_b, file_sha(pkg_b))
    assert verify_cache_dll(cache_b, alternate_sha)
    negative("D2b-N02", "D2B_PACKAGE_ARCHIVE_SHA_MISMATCH",
             lambda: verify_archive(restored_b_archive, approved_archive_sha),
             results)

    # N03 changes one physically installed NuGet global-packages DLL file.
    # Restore original A bytes immediately after the intended rejection.
    restored_a_lib.write_bytes(dll_b.read_bytes())
    try:
        negative("D2b-N03", "D2B_RESTORED_DLL_HASH_MISMATCH",
                 lambda: verify_cache_dll(cache_a, approved_sha), results)
    finally:
        restored_a_lib.write_bytes(dll_a.read_bytes())
    assert verify_cache_dll(cache_a, approved_sha)

    compiled_a, copied_a = build_consumer(consumer_a)
    compiled_b, copied_b = build_consumer(consumer_b)
    assert verify_copy_local(copied_a, approved_sha)
    assert verify_copy_local(copied_b, alternate_sha)

    # N04: replace physical CopyLocal after genuine NuGet restore/build.
    copied_a.write_bytes(dll_b.read_bytes())
    try:
        negative("D2b-N04", "D2B_CONSUMER_COPY_HASH_MISMATCH",
                 lambda: verify_copy_local(copied_a, approved_sha), results)
    finally:
        copied_a.write_bytes(dll_a.read_bytes())
    assert verify_copy_local(copied_a, approved_sha)

    # The host invokes actual compiled SDK PackageReference consumer class,
    # which calls the package library, then reports its actually loaded module.
    loaded_a = loaded(runtime, compiled_a)
    loaded_b = loaded(runtime, compiled_b)
    require(loaded_a["loaded_location"].casefold() ==
            str(copied_a.resolve()).casefold(),
            "D2B_CLR_LOCATION_NOT_CONSUMER_COPY")
    require(loaded_b["loaded_location"].casefold() ==
            str(copied_b.resolve()).casefold(),
            "D2B_CLR_LOCATION_NOT_CONSUMER_COPY")
    assert verify_loaded(loaded_a, approved_sha, 101)
    assert verify_loaded(loaded_b, alternate_sha, 202)
    negative("D2b-N05", "D2B_CLR_LOADED_DLL_HASH_MISMATCH",
             lambda: verify_loaded(loaded_b, approved_sha, 101), results)

    require(len(results) == 5 and
            [x["id"] for x in results] ==
            ["D2b-N01", "D2b-N02", "D2b-N03", "D2b-N04", "D2b-N05"],
            "D2B_WRONG_PREREGISTERED_TEST_UNIVERSE")
    return {
        "experiment": "D2b",
        "verdict": "LOCAL_REAL_NUGET_AND_CLR_RESEARCH_VERIFIED_ONLY",
        "scope": "one disposable traditional net48 library and SDK net48 consumer",
        "two_real_compiler_variants": "VERIFIED_DISTINCT",
        "two_local_nuget_package_archives": "VERIFIED_DIFFERENT",
        "two_actual_local_feed_restores": "VERIFIED_ISOLATED",
        "two_real_netfx_consumer_loads": "VERIFIED",
        "negative_controls": results,
        "privacy": "no source data, physical paths, raw logs or artifact hashes",
        "limit": "runner-local post-exit CLR module hash, no production/independent manifest authority",
        "original_gate_c": "UNSATISFIED",
        "native_gate_cn_release": "NOT_AUTHORIZED",
        "source_link_production": "HOLD",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--private-root", required=True, type=Path)
    p.add_argument("--consumer-template", required=True, type=Path)
    p.add_argument("--netfx-loader", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    try:
        require(not a.output.exists(), "D2B_REPORT_REUSED")
        report = run(a.private_root, a.consumer_template, a.netfx_loader)
        a.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                            encoding="ascii")
        print("D2b research: two real local NuGet installs, two real CLR consumers, 5/5 candidate identity negatives PASS")
        print("Gate C UNSATISFIED; C-N release NOT_AUTHORIZED; production Source Link HOLD")
    except Rejected as e:
        print("D2b FAIL CLOSED OR INCONCLUSIVE: " + e.code, file=sys.stderr)
        raise SystemExit(2)
    except Exception:
        # Never surface raw external tool output/path/hash.
        print("D2b FAIL CLOSED OR INCONCLUSIVE: PRIVATE_RESEARCH_RUNNER_ERROR",
              file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
