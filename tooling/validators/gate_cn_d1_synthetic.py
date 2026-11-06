#!/usr/bin/env python3
"""D1 synthetic-only Gate C-N domain contract probes.

NOT a live PDB reader, release gate, authority provider or production workflow.
No filesystem, network, compiler or package operations. All assertions use
explicit in-memory fixtures; caller-controlled records are NOT real signatures.
Trusted approval and sealed output are separate synthetic input ports.
"""
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Mapping


class Rejected(ValueError):
    """Sanitized, fixed-category D1 rejection without source/path disclosure."""

    def __init__(self, category):
        super().__init__(category)
        self.category = category


def require(condition, category):
    if not condition:
        raise Rejected(category)


def canonical_sha256(value):
    """Stable synthetic manifest identity, not a substitute for a signed approval."""
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")).hexdigest()


@dataclass(frozen=True)
class Approval:
    """Read-only record provided by an independent *synthetic* approval port."""

    manifest_sha256: str
    reviewer_identity: str
    expires_at: int
    revoked: bool


@dataclass(frozen=True)
class Candidate:
    """Synthetic compiled/installed artifact identity; no file access."""

    assembly_version: str
    sha256: str


@dataclass(frozen=True)
class CompilerEvent:
    """Synthetic witness of structured Csc input and completion."""

    run_identity: str
    task_identity: str
    compiler_sources: tuple
    compiler_options_sha256: str
    output_dll: str
    output_pdb: str
    completed: bool


@dataclass(frozen=True)
class CompiledOutput:
    """Synthetic independently sealed hashes and paired PE/native-PDB identity."""

    run_identity: str
    dll_sha256: str
    pdb_sha256: str
    pe_codeview_guid_age: str
    pdb_info_guid_age: str


_HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SAFE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,79}$")
_ALLOWED_ORIGINS = frozenset(("tracked", "moniker"))
_COMPONENT_FIELDS = frozenset((
    "assembly", "project", "target", "framework",
    "configuration", "platform", "sources",
))
_SOURCE_FIELDS = frozenset(("path", "origin", "sha256"))
_MANIFEST_FIELDS = frozenset(("schema", "application_commit", "components"))


def normalized_relative_path(value):
    require(type(value) is str and 0 < len(value) < 512
            and not value.startswith(("/", "\\")) and "\\" not in value
            and ":" not in value and "\x00" not in value
            and all(part not in ("", ".", "..") for part in value.split("/")),
            "D1_UNSAFE_RELATIVE_IDENTITY")
    return value.casefold()


def indexed_components(components):
    """Normalize an independently supplied complete set; reject alias collisions."""
    require(type(components) is list and 0 < len(components) <= 32,
            "D1_COMPONENT_SCHEMA_INVALID")
    result = {}
    for component in components:
        require(type(component) is dict
                and set(component) == _COMPONENT_FIELDS,
                "D1_COMPONENT_SCHEMA_INVALID")
        name = component["assembly"]
        require(type(name) is str and _SAFE_NAME.fullmatch(name),
                "D1_COMPONENT_SCHEMA_INVALID")
        key = name.casefold()
        require(key not in result, "D1_DUPLICATE_COMPONENT_IDENTITY")
        project = normalized_relative_path(component["project"])
        require(component["target"] == "CoreCompile"
                and component["framework"] == "net48"
                and component["configuration"] == "Release"
                and component["platform"] == "AnyCPU",
                "D1_UNSUPPORTED_SYNTHETIC_COMPILER_SCOPE")
        sources = component["sources"]
        require(type(sources) is list and 1 <= len(sources) <= 1024,
                "D1_SOURCE_SCHEMA_INVALID")
        normalized_sources = {}
        for source in sources:
            require(type(source) is dict and set(source) == _SOURCE_FIELDS
                    and type(source["origin"]) is str
                    and type(source["sha256"]) is str
                    and _HEX_SHA256.fullmatch(source["sha256"]),
                    "D1_SOURCE_SCHEMA_INVALID")
            identity = normalized_relative_path(source["path"])
            require(identity not in normalized_sources,
                    "D1_DUPLICATE_SOURCE_IDENTITY")
            # Keep origin with the identity set; unexpected origins cannot
            # silently turn into "tracked" or a generated moniker.
            normalized_sources[identity] = (
                source["origin"], source["sha256"])
        result[key] = (
            project, component["target"], component["framework"],
            component["configuration"], component["platform"],
            frozenset(normalized_sources.items()),
        )
    return result


def authorize_scope(manifest, observed_components, approved_record,
                    *, build_identity, current_time):
    """Validate an exact *synthetic* trusted-approval vs observed compilation set.

    approved_record is a read-only caller-injected port used only in D1.
    It does not prove signature, real separation of duties or custody.
    """
    require(type(manifest) is dict and set(manifest) == _MANIFEST_FIELDS
            and manifest["schema"] == "gate-cn-d1-synthetic-v1"
            and type(manifest["application_commit"]) is str
            and re.fullmatch(r"[0-9a-f]{40}", manifest["application_commit"]),
            "D1_MANIFEST_SCHEMA_INVALID")
    require(isinstance(approved_record, Approval)
            and _HEX_SHA256.fullmatch(approved_record.manifest_sha256),
            "D1_MANIFEST_APPROVAL_MISSING")
    require(canonical_sha256(manifest) == approved_record.manifest_sha256,
            "D1_MANIFEST_APPROVAL_MISMATCH")
    require(type(build_identity) is str and bool(build_identity)
            and type(approved_record.reviewer_identity) is str
            and bool(approved_record.reviewer_identity)
            and build_identity != approved_record.reviewer_identity,
            "D1_APPROVAL_NOT_INDEPENDENT")
    require(approved_record.revoked is False
            and type(approved_record.expires_at) is int
            and type(current_time) is int
            and current_time < approved_record.expires_at,
            "D1_APPROVAL_EXPIRED_OR_REVOKED")
    expected = indexed_components(manifest["components"])
    actual = indexed_components(observed_components)
    require(set(expected) == set(actual), "D1_COMPONENT_UNIVERSE_MISMATCH")
    for assembly in expected:
        # Separate compiler source sets from project/target/config differences.
        require(expected[assembly][:5] == actual[assembly][:5],
                "D1_PROJECT_TARGET_SCOPE_MISMATCH")
        require(expected[assembly][5] == actual[assembly][5],
                "D1_COMPILER_SOURCE_SET_MISMATCH")
    return True


def verify_candidate_bindings(candidates: Mapping, required_by_suite: Mapping,
                              actual_suite_files: Mapping,
                              approved_package: Candidate,
                              installed_package: Candidate):
    """Synthetic mandatory copy-local and installed archive hash comparisons."""
    require(bool(candidates) and bool(required_by_suite)
            and set(required_by_suite) == set(actual_suite_files),
            "D1_SUITE_UNIVERSE_MISMATCH")
    for suite, required_assemblies in required_by_suite.items():
        require(bool(required_assemblies) and len(set(required_assemblies))
                == len(required_assemblies), "D1_SUITE_REQUIREMENTS_INVALID")
        local = actual_suite_files[suite]
        require(isinstance(local, dict), "D1_SUITE_REQUIREMENTS_INVALID")
        for assembly in required_assemblies:
            require(assembly in candidates and assembly in local,
                    "D1_MANDATORY_COPY_LOCAL_MISSING")
            candidate = candidates[assembly]
            installed = local[assembly]
            require(isinstance(candidate, Candidate)
                    and isinstance(installed, Candidate),
                    "D1_CANDIDATE_IDENTITY_INVALID")
            require(candidate.assembly_version == installed.assembly_version
                    and candidate.sha256 == installed.sha256,
                    "D1_CANDIDATE_COPY_LOCAL_HASH_MISMATCH")
        require(set(local) == set(required_assemblies),
                "D1_UNEXPECTED_SUITE_COPY_LOCAL")
    require(isinstance(approved_package, Candidate)
            and isinstance(installed_package, Candidate),
            "D1_PACKAGE_IDENTITY_INVALID")
    require(approved_package == installed_package,
            "D1_PACKAGE_ARCHIVE_IDENTITY_MISMATCH")
    return True


def verify_compiler_output(events, actual_output: CompiledOutput,
                           sealed_output: CompiledOutput, *,
                           output_root_was_empty, required_run_identity):
    """Synthetic unique task, fresh output root, and sealed output byte identity.

    A passing test proves only this in-memory model, never genuine Csc causation.
    """
    require(output_root_was_empty is True,
            "D1_OUTPUT_ROOT_NOT_FRESH")
    require(len(events) == 1 and isinstance(events[0], CompilerEvent),
            "D1_CSC_EVENT_MISSING_OR_AMBIGUOUS")
    event = events[0]
    require(event.completed is True
            and event.run_identity == required_run_identity
            and bool(event.task_identity)
            and event.output_dll.endswith(".dll")
            and event.output_pdb.endswith(".pdb")
            and bool(event.compiler_sources)
            and len(event.compiler_sources) == len(set(event.compiler_sources))
            and _HEX_SHA256.fullmatch(event.compiler_options_sha256),
            "D1_CSC_EVENT_NOT_ATTESTED")
    require(isinstance(sealed_output, CompiledOutput)
            and isinstance(actual_output, CompiledOutput)
            and event.run_identity == sealed_output.run_identity
            and event.run_identity == actual_output.run_identity,
            "D1_OUTPUT_INVOCATION_MISMATCH")
    require(actual_output.pe_codeview_guid_age
            == actual_output.pdb_info_guid_age
            and bool(actual_output.pe_codeview_guid_age),
            "D1_PE_PDB_PAIR_MISMATCH")
    require(_HEX_SHA256.fullmatch(actual_output.dll_sha256)
            and _HEX_SHA256.fullmatch(actual_output.pdb_sha256)
            and actual_output.dll_sha256 == sealed_output.dll_sha256
            and actual_output.pdb_sha256 == sealed_output.pdb_sha256
            and actual_output.pe_codeview_guid_age
                == sealed_output.pe_codeview_guid_age
            and actual_output.pdb_info_guid_age
                == sealed_output.pdb_info_guid_age,
            "D1_COMPILER_OUTPUT_HASH_MISMATCH")
    return True
