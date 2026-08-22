#!/usr/bin/env python3
"""Fail-closed checks for ActionGate independent-source provenance controls."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SPDX_TOKEN = re.compile(r"^[A-Za-z0-9.+():\-\s]+$")
PLACEHOLDER = re.compile(r"(?:<[^>]+>|TODO|TBD|CHANGEME|EXAMPLE(?:\.COM)?|0{40}|0{64})", re.I)

REQUIRED_PATHS = (
    ".provenance/upstreams.lock.json",
    ".provenance/imported-paths.json",
    ".provenance/patch-lineage.json",
    ".provenance/policy.json",
    ".provenance/local-handoff-queue.json",
    ".provenance/schemas/upstreams-lock.schema.json",
    ".provenance/schemas/imported-paths.schema.json",
    ".provenance/schemas/patch-lineage.schema.json",
    ".provenance/schemas/clean-room-session-receipt.schema.json",
    ".provenance/schemas/independent-provenance-review-receipt.schema.json",
    ".provenance/schemas/outside-project-review-receipt.schema.json",
    ".provenance/schemas/release-admission.schema.json",
    "docs/provenance/README.md",
    "docs/provenance/AGENTS.md",
    "docs/provenance/UPSTREAM_BASELINE.md",
    "docs/provenance/SOURCE_BOUNDARY.md",
    "docs/provenance/PATCH_LINEAGE.md",
    "docs/provenance/LICENSE_OBLIGATIONS.md",
    "docs/handoff/PROVENANCE_LOCAL_HANDOFF.md",
    "LICENSES/README.md",
    "sbom/README.md",
    "CONTRIBUTING.md",
    ".github/PULL_REQUEST_TEMPLATE/provenance.md",
)

SCHEMA_PATHS = tuple(path for path in REQUIRED_PATHS if path.endswith(".schema.json"))

ALLOWED_RELATIONSHIPS = {
    "DERIVED_SOURCE",
    "DEPENDENCY",
    "REFERENCE_IMPLEMENTATION",
    "SPECIFICATION_ONLY",
    "BUILD_TOOLING",
}
ALLOWED_IMPORT_MODES = {
    "UNCHANGED_IMPORT",
    "MODIFIED_DERIVATIVE",
    "GENERATED_FROM_PUBLIC_SPEC",
}
ALLOWED_AUTHORSHIP = {
    "ORIGINAL_PATCH",
    "DERIVED_PATCH",
    "MECHANICAL_TRANSFORM",
    "UNCHANGED_IMPORT",
    "GENERATED_FROM_PUBLIC_SPEC",
}
COPY_RELATIONSHIPS = {"DERIVED_SOURCE", "DEPENDENCY"}
REQUIRED_FORBIDDEN_SOURCE_CLASSES = {
    "EMPLOYER_SOURCE",
    "EMPLOYER_PRIVATE_DOCUMENT",
    "EMPLOYER_PROTOCOL",
    "EMPLOYER_TEST_VECTOR",
    "CUSTOMER_DATA",
    "EMPLOYER_CREDENTIAL",
    "EMPLOYER_BUILD_ARTIFACT",
    "NON_PUBLIC_REMEMBERED_IMPLEMENTATION",
}
REQUIRED_RELEASE_REQUIREMENTS = {
    "UPSTREAM_LICENSE_VERIFIED",
    "BASELINE_SHA_TREE_PINNED",
    "IMPORT_PATHS_CLASSIFIED",
    "CLEAN_ROOM_SESSION_RECEIPTS_PRESENT",
    "NOTICE_AND_SBOM_VERIFIED",
    "INDEPENDENT_PROVENANCE_REVIEWED",
    "HUMAN_LEGAL_ADMITTED",
}

LOCK_KEYS = {
    "schema", "repository", "state", "source_policy",
    "no_source_imports_admitted", "legal_admission", "release_state", "upstreams",
}
UPSTREAM_KEYS = {
    "id", "name", "repository", "commit", "tree", "tag",
    "license_spdx", "license_sha256", "relationship",
    "imported_paths", "excluded_paths", "observed_at",
}
IMPORT_ROOT_KEYS = {"schema", "repository", "state", "mappings"}
IMPORT_KEYS = {"upstream_id", "source_path", "target_path", "source_blob", "import_mode"}
LINEAGE_ROOT_KEYS = {"schema", "repository", "state", "records"}
LINEAGE_KEYS = {
    "change_id", "target_path", "authorship", "upstream_id",
    "source_path", "upstream_blob", "receipt",
}

PRODUCT_SOURCE_PREFIXES = (
    "packages/",
    "src/",
    "contracts/",
    "sdk-",
    "vendor/",
    "third_party/",
    "examples/",
)
DEPENDENCY_FILES = {
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "pyproject.toml", "poetry.lock", "requirements.txt",
    "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts",
    "Package.swift", "Cargo.toml", "Cargo.lock", "go.mod", "go.sum",
}

QUEUE_ITEM_KEYS = {
    "id", "state", "objective", "entry", "required_inputs",
    "commands_after_binding", "parameter_law", "runtime_lane",
    "receipt", "public_receipt", "exit", "next", "human_owned",
}
QUEUE_STATES = {
    "ACTIVE_INPUT_COLLECTION",
    "BLOCKED_BY_PV_LH_001",
    "BLOCKED_BY_PV_LH_002",
    "BLOCKED_BY_PV_LH_003_AND_PV_LH_004",
    "HUMAN_ADMIT_REQUIRED",
}
REQUIRED_INDEPENDENT_FALSIFIERS = {
    "placeholder_repository",
    "malformed_commit_tree",
    "unknown_license",
    "unmapped_import",
    "missing_source_blob",
    "private_url_leak",
    "false_release_escalation",
    "missing_dco",
    "same_context_independence",
    "fabricated_sbom",
    "stale_subject_binding",
    "wrong_event_checkout",
    "employer_nonoverlap_overclaim",
    "queue_placeholder_execution",
}
RELEASE_SUCCESSOR_ALLOWED_PATHS = {
    ".provenance/upstreams.lock.json",
    ".provenance/receipts/independent-provenance-review.json",
    ".provenance/receipts/outside-project-review-redacted.json",
    ".provenance/receipts/release-admission.json",
    "sbom/actiongate.spdx.json",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def strict_keys(value: dict[str, Any], expected: set[str], label: str) -> list[str]:
    errors: list[str] = []
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing:
        errors.append(f"{label} missing keys: {sorted(missing)}")
    if unknown:
        errors.append(f"{label} has unknown keys: {sorted(unknown)}")
    return errors


def valid_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def relative_path_is_safe(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if "\\" in value or "\x00" in value or any(ord(ch) < 32 for ch in value):
        return False
    if value.startswith("/") or value.endswith("/") or "//" in value or ":" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return False
    if any(char in value for char in "*?[]{}"):
        return False
    return True


def overlapping_paths(paths: Iterable[str]) -> list[tuple[str, str]]:
    normalized = [path.strip("/") for path in paths]
    conflicts: list[tuple[str, str]] = []
    seen: set[str] = set()
    for path in normalized:
        if path in seen:
            conflicts.append((path, path))
        seen.add(path)
    unique = sorted(seen)
    for index, left in enumerate(unique):
        for right in unique[index + 1:]:
            if right.startswith(left + "/"):
                conflicts.append((left, right))
    return conflicts


def public_https_url_is_sane(value: Any) -> bool:
    if not isinstance(value, str) or PLACEHOLDER.search(value):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if parsed.scheme != "https" or not parsed.hostname:
        return False
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        return False
    host = parsed.hostname.rstrip(".").lower()
    if host in {"localhost"} or host.endswith((".internal", ".local", ".lan", ".home", ".test", ".invalid", ".example")):
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return True
    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_multicast
        or address.is_unspecified
    )


def validate_schema_documents(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in SCHEMA_PATHS:
        path = root / relative
        try:
            schema = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{relative} is not valid object JSON: {exc}")
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{relative} is not Draft 2020-12")
        if schema.get("type") != "object":
            errors.append(f"{relative} root type must be object")
        if schema.get("additionalProperties") is not False:
            errors.append(f"{relative} must fail closed on unknown root fields")
    return errors


def validate_lock(lock: dict[str, Any]) -> list[str]:
    errors = strict_keys(lock, LOCK_KEYS, "upstream lock")
    if lock.get("schema") != "actiongate-upstream-lock/v1":
        errors.append("upstream lock schema mismatch")
    if lock.get("repository") != "ed3c/ActionGate":
        errors.append("upstream lock repository mismatch")
    if lock.get("source_policy") != "PUBLIC_ENUMERATED_ONLY":
        errors.append("source policy must be PUBLIC_ENUMERATED_ONLY")

    state = lock.get("state")
    upstreams = lock.get("upstreams")
    if not isinstance(upstreams, list):
        return errors + ["upstreams must be an array"]

    if state == "UPSTREAM_SELECTION_REQUIRED":
        if upstreams:
            errors.append("selection-required state must have zero upstreams")
        if lock.get("no_source_imports_admitted") is not True:
            errors.append("selection-required state must forbid source imports")
        if lock.get("legal_admission") != "HUMAN_ADMIT_REQUIRED":
            errors.append("selection-required state cannot claim legal admission")
        if lock.get("release_state") != "BLOCKED":
            errors.append("selection-required state must block release")
    elif state == "UPSTREAMS_ADMITTED":
        if not upstreams:
            errors.append("admitted state requires at least one upstream")
        if lock.get("no_source_imports_admitted") not in {True, False}:
            errors.append("no_source_imports_admitted must be boolean")
    else:
        errors.append(f"unsupported upstream state: {state!r}")

    seen: set[str] = set()
    for index, item in enumerate(upstreams):
        prefix = f"upstreams[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        errors.extend(strict_keys(item, UPSTREAM_KEYS, prefix))

        upstream_id = item.get("id")
        if not isinstance(upstream_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,63}", upstream_id):
            errors.append(f"{prefix}.id is invalid")
        elif upstream_id in seen:
            errors.append(f"duplicate upstream id: {upstream_id}")
        else:
            seen.add(upstream_id)

        name = item.get("name")
        if not isinstance(name, str) or not name.strip() or len(name) > 200:
            errors.append(f"{prefix}.name is invalid")

        repository = item.get("repository")
        if not public_https_url_is_sane(repository):
            errors.append(f"{prefix}.repository is not a sane public HTTPS locator")

        for field, pattern in (("commit", HEX40), ("tree", HEX40), ("license_sha256", HEX64)):
            value = item.get(field)
            if not isinstance(value, str) or not pattern.fullmatch(value):
                errors.append(f"{prefix}.{field} must be exact lowercase hex")
            elif PLACEHOLDER.search(value):
                errors.append(f"{prefix}.{field} contains a placeholder")

        tag = item.get("tag")
        if tag is not None and (not isinstance(tag, str) or not tag.strip() or PLACEHOLDER.search(tag)):
            errors.append(f"{prefix}.tag is invalid")

        license_spdx = item.get("license_spdx")
        if (
            not isinstance(license_spdx, str)
            or not SPDX_TOKEN.fullmatch(license_spdx)
            or license_spdx in {"UNKNOWN", "NOASSERTION"}
        ):
            errors.append(f"{prefix}.license_spdx is not admitted")

        relationship = item.get("relationship")
        if relationship not in ALLOWED_RELATIONSHIPS:
            errors.append(f"{prefix}.relationship is invalid")

        imported_paths = item.get("imported_paths")
        excluded_paths = item.get("excluded_paths")
        for field, values in (("imported_paths", imported_paths), ("excluded_paths", excluded_paths)):
            if not isinstance(values, list):
                errors.append(f"{prefix}.{field} must be an array")
                continue
            if len(values) != len(set(values)):
                errors.append(f"{prefix}.{field} contains duplicates")
            for value in values:
                if not isinstance(value, str) or not relative_path_is_safe(value):
                    errors.append(f"{prefix}.{field} contains an unsafe or non-exact path")

        if isinstance(imported_paths, list):
            if not imported_paths:
                errors.append(f"{prefix}.imported_paths must bind at least one source boundary")
            for left, right in overlapping_paths(
                value for value in imported_paths if isinstance(value, str)
            ):
                errors.append(f"{prefix}.imported_paths contains overlapping boundaries: {left!r} and {right!r}")

        if not valid_datetime(item.get("observed_at")):
            errors.append(f"{prefix}.observed_at must be a timezone-aware date-time")

    if lock.get("release_state") == "RELEASE_ELIGIBLE":
        if lock.get("legal_admission") != "HUMAN_ADMITTED":
            errors.append("release eligibility requires Human legal admission")
        if not upstreams:
            errors.append("release eligibility requires an admitted source inventory")
        if lock.get("no_source_imports_admitted") is True and any(
            item.get("relationship") == "DERIVED_SOURCE" for item in upstreams if isinstance(item, dict)
        ):
            errors.append("derived source cannot be release eligible while source imports are declared absent")

    if lock.get("legal_admission") not in {"HUMAN_ADMIT_REQUIRED", "HUMAN_ADMITTED"}:
        errors.append("legal_admission state is invalid")
    if lock.get("release_state") not in {"BLOCKED", "RELEASE_ELIGIBLE"}:
        errors.append("release_state is invalid")

    return errors


def upstream_index(lock: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in lock.get("upstreams", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def path_within_boundary(path: str, boundaries: list[str]) -> bool:
    return any(path == boundary or path.startswith(boundary.rstrip("/") + "/") for boundary in boundaries)


def validate_imports(imports: dict[str, Any], lock: dict[str, Any], root: Path | None = None) -> list[str]:
    errors = strict_keys(imports, IMPORT_ROOT_KEYS, "imported paths")
    if imports.get("schema") != "actiongate-imported-paths/v1":
        errors.append("imported-paths schema mismatch")
    if imports.get("repository") != "ed3c/ActionGate":
        errors.append("imported-paths repository mismatch")

    mappings = imports.get("mappings")
    if not isinstance(mappings, list):
        return errors + ["mappings must be an array"]

    upstreams = upstream_index(lock)
    targets: list[str] = []
    source_keys: set[tuple[str, str]] = set()
    for index, mapping in enumerate(mappings):
        prefix = f"mappings[{index}]"
        if not isinstance(mapping, dict):
            errors.append(f"{prefix} must be an object")
            continue
        errors.extend(strict_keys(mapping, IMPORT_KEYS, prefix))

        upstream_id = mapping.get("upstream_id")
        upstream = upstreams.get(upstream_id)
        if upstream is None:
            errors.append(f"{prefix} references an unadmitted upstream")

        for field in ("source_path", "target_path"):
            value = mapping.get(field)
            if not isinstance(value, str) or not relative_path_is_safe(value):
                errors.append(f"{prefix}.{field} is unsafe or non-exact")

        source_blob = mapping.get("source_blob")
        if not isinstance(source_blob, str) or not HEX40.fullmatch(source_blob):
            errors.append(f"{prefix}.source_blob must be exact lowercase hex")

        mode = mapping.get("import_mode")
        if mode not in ALLOWED_IMPORT_MODES:
            errors.append(f"{prefix}.import_mode is invalid")

        source = mapping.get("source_path")
        target = mapping.get("target_path")
        if upstream and isinstance(source, str):
            boundaries = upstream.get("imported_paths")
            if not isinstance(boundaries, list) or not path_within_boundary(source, boundaries):
                errors.append(f"{prefix}.source_path is outside the upstream imported-path boundary")
            relationship = upstream.get("relationship")
            if mode == "GENERATED_FROM_PUBLIC_SPEC":
                if relationship != "SPECIFICATION_ONLY":
                    errors.append(f"{prefix} generated-from-spec mapping requires SPECIFICATION_ONLY")
            elif relationship not in COPY_RELATIONSHIPS:
                errors.append(f"{prefix} copied/derived mapping requires DERIVED_SOURCE or DEPENDENCY")

        if isinstance(target, str):
            targets.append(target)
            if root is not None and not (root / target).exists():
                errors.append(f"{prefix}.target_path does not exist in the candidate tree")
        if isinstance(upstream_id, str) and isinstance(source, str):
            key = (upstream_id, source)
            if key in source_keys:
                errors.append(f"{prefix} duplicates upstream source path {key!r}")
            source_keys.add(key)

    for left, right in overlapping_paths(targets):
        errors.append(f"overlapping imported target paths: {left!r} and {right!r}")

    if lock.get("state") == "UPSTREAM_SELECTION_REQUIRED" and mappings:
        errors.append("imports exist while upstream selection is required")
    if lock.get("no_source_imports_admitted") is True and mappings:
        errors.append("imports exist while no_source_imports_admitted is true")
    if imports.get("state") == "NO_IMPORTS_ADMITTED" and mappings:
        errors.append("NO_IMPORTS_ADMITTED must have zero mappings")
    if imports.get("state") == "IMPORTS_CLASSIFIED" and not mappings:
        errors.append("IMPORTS_CLASSIFIED requires mappings")
    if imports.get("state") not in {"NO_IMPORTS_ADMITTED", "IMPORTS_CLASSIFIED"}:
        errors.append("imported paths state is invalid")

    return errors


def validate_patch_lineage(
    lineage: dict[str, Any],
    lock: dict[str, Any],
    imports: dict[str, Any] | None = None,
    root: Path | None = None,
) -> list[str]:
    errors = strict_keys(lineage, LINEAGE_ROOT_KEYS, "patch lineage")
    if lineage.get("schema") != "actiongate-patch-lineage/v1":
        errors.append("patch-lineage schema mismatch")
    if lineage.get("repository") != "ed3c/ActionGate":
        errors.append("patch-lineage repository mismatch")

    records = lineage.get("records")
    if not isinstance(records, list):
        return errors + ["patch records must be an array"]

    upstreams = upstream_index(lock)
    targets: list[str] = []
    seen_changes: set[str] = set()
    record_by_target: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        errors.extend(strict_keys(record, LINEAGE_KEYS, prefix))

        change_id = record.get("change_id")
        if not isinstance(change_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", change_id):
            errors.append(f"{prefix}.change_id is invalid")
        elif change_id in seen_changes:
            errors.append(f"duplicate change_id: {change_id}")
        else:
            seen_changes.add(change_id)

        target = record.get("target_path")
        if not isinstance(target, str) or not relative_path_is_safe(target):
            errors.append(f"{prefix}.target_path is unsafe or non-exact")
        else:
            targets.append(target)
            if target in record_by_target:
                errors.append(f"duplicate patch-lineage target: {target}")
            record_by_target[target] = record
            if root is not None and not (root / target).exists():
                errors.append(f"{prefix}.target_path does not exist in the candidate tree")

        authorship = record.get("authorship")
        if authorship not in ALLOWED_AUTHORSHIP:
            errors.append(f"{prefix}.authorship is invalid")
            continue

        upstream_id = record.get("upstream_id")
        source_path = record.get("source_path")
        upstream_blob = record.get("upstream_blob")
        upstream = upstreams.get(upstream_id) if isinstance(upstream_id, str) else None

        if authorship == "ORIGINAL_PATCH":
            if upstream_id is not None or source_path is not None or upstream_blob is not None:
                errors.append(f"{prefix} original patch must not claim upstream source")
        else:
            if upstream is None:
                errors.append(f"{prefix} non-original record lacks admitted upstream")
            if not isinstance(source_path, str) or not relative_path_is_safe(source_path):
                errors.append(f"{prefix} non-original record lacks exact source_path")
            if not isinstance(upstream_blob, str) or not HEX40.fullmatch(upstream_blob):
                errors.append(f"{prefix} non-original record lacks exact upstream blob")
            if upstream and isinstance(source_path, str):
                if not path_within_boundary(source_path, upstream.get("imported_paths", [])):
                    errors.append(f"{prefix}.source_path is outside upstream imported-path boundary")
                relationship = upstream.get("relationship")
                if authorship == "GENERATED_FROM_PUBLIC_SPEC":
                    if relationship != "SPECIFICATION_ONLY":
                        errors.append(f"{prefix} generated-from-spec requires SPECIFICATION_ONLY")
                elif relationship not in COPY_RELATIONSHIPS:
                    errors.append(f"{prefix} copied/derived authorship requires DERIVED_SOURCE or DEPENDENCY")

        receipt = record.get("receipt")
        if not isinstance(receipt, str) or not relative_path_is_safe(receipt):
            errors.append(f"{prefix}.receipt is unsafe")
        elif root is not None and not (root / receipt).is_file():
            errors.append(f"{prefix}.receipt does not exist")

    for left, right in overlapping_paths(targets):
        errors.append(f"overlapping patch target paths: {left!r} and {right!r}")

    if lineage.get("state") == "BASELINE_ONLY" and records:
        errors.append("BASELINE_ONLY must have zero patch records")
    if lineage.get("state") == "PATCHES_RECORDED" and not records:
        errors.append("PATCHES_RECORDED requires records")
    if lineage.get("state") not in {"BASELINE_ONLY", "PATCHES_RECORDED"}:
        errors.append("patch lineage state is invalid")

    mappings_by_target: dict[str, dict[str, Any]] = {}
    if imports and isinstance(imports.get("mappings"), list):
        for mapping in imports["mappings"]:
            if isinstance(mapping, dict) and isinstance(mapping.get("target_path"), str):
                mappings_by_target[mapping["target_path"]] = mapping

        compatible = {
            "UNCHANGED_IMPORT": {"UNCHANGED_IMPORT"},
            "MODIFIED_DERIVATIVE": {"DERIVED_PATCH", "MECHANICAL_TRANSFORM"},
            "GENERATED_FROM_PUBLIC_SPEC": {"GENERATED_FROM_PUBLIC_SPEC"},
        }
        for target, mapping in mappings_by_target.items():
            record = record_by_target.get(target)
            if record is None:
                errors.append(f"imported target lacks patch-lineage record: {target}")
                continue
            if record.get("authorship") not in compatible.get(mapping.get("import_mode"), set()):
                errors.append(f"patch lineage mode mismatch for {target}")
            if record.get("upstream_id") != mapping.get("upstream_id"):
                errors.append(f"patch lineage upstream mismatch for {target}")
            if record.get("source_path") != mapping.get("source_path"):
                errors.append(f"patch lineage source_path mismatch for {target}")
            if record.get("upstream_blob") != mapping.get("source_blob"):
                errors.append(f"patch lineage source blob mismatch for {target}")

        for target, record in record_by_target.items():
            if record.get("authorship") == "ORIGINAL_PATCH":
                continue
            if target not in mappings_by_target:
                errors.append(f"non-original patch lacks imported-path mapping: {target}")

    return errors


def scan_private_material(root: Path, policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    excluded = set(policy.get("private_scan_exclusions", []))
    needles = policy.get("forbidden_public_substrings", [])
    if not isinstance(needles, list):
        return ["forbidden_public_substrings must be an array"]

    try:
        tracked = subprocess.check_output(
            ["git", "ls-files"], cwd=root, text=True, stderr=subprocess.DEVNULL
        ).splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        tracked = [
            str(path.relative_to(root))
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]

    for relative in tracked:
        if relative in excluded:
            continue
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for needle in needles:
            if isinstance(needle, str) and needle and needle in text:
                errors.append(f"forbidden public substring in {relative}")
    return errors


def validate_policy(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema", "repository", "current_control_state", "upstream_state",
        "allowed_relationships", "forbidden_source_classes",
        "forbidden_public_substrings", "private_scan_exclusions",
        "dco", "release_requirements", "release_authority",
    }
    errors.extend(strict_keys(policy, expected, "provenance policy"))
    if policy.get("schema") != "actiongate-provenance-policy/v1":
        errors.append("provenance policy schema mismatch")
    if policy.get("repository") != "ed3c/ActionGate":
        errors.append("provenance policy repository mismatch")
    if policy.get("current_control_state") != "PROVENANCE_CONTROL_PLANE_IMPLEMENTED":
        errors.append("control state mismatch")
    if policy.get("upstream_state") not in {"UPSTREAM_SELECTION_REQUIRED", "UPSTREAMS_ADMITTED"}:
        errors.append("policy upstream_state is invalid")

    relationships = policy.get("allowed_relationships")
    if not isinstance(relationships, list) or set(relationships) != ALLOWED_RELATIONSHIPS:
        errors.append("policy allowed_relationships drifted from the admitted contract")
    elif len(relationships) != len(set(relationships)):
        errors.append("policy allowed_relationships contains duplicates")

    forbidden = policy.get("forbidden_source_classes")
    if not isinstance(forbidden, list) or not REQUIRED_FORBIDDEN_SOURCE_CLASSES.issubset(set(forbidden)):
        errors.append("policy forbidden_source_classes is incomplete")
    elif len(forbidden) != len(set(forbidden)):
        errors.append("policy forbidden_source_classes contains duplicates")

    needles = policy.get("forbidden_public_substrings")
    if not isinstance(needles, list) or not needles or not all(isinstance(v, str) and v for v in needles):
        errors.append("policy forbidden_public_substrings is invalid")
    elif len(needles) != len(set(needles)):
        errors.append("policy forbidden_public_substrings contains duplicates")

    exclusions = policy.get("private_scan_exclusions")
    if exclusions != [".provenance/policy.json"]:
        errors.append("private scan exclusions must contain only the policy that declares the needles")

    dco = policy.get("dco")
    if not isinstance(dco, dict) or set(dco) != {
        "required_when_source_or_product_code_changes",
        "machine_must_not_invent_human_signoff",
    }:
        errors.append("DCO policy shape is invalid")
    else:
        if dco.get("required_when_source_or_product_code_changes") is not True:
            errors.append("source-bearing changes must require DCO")
        if dco.get("machine_must_not_invent_human_signoff") is not True:
            errors.append("machine Human-signoff fabrication must remain forbidden")

    requirements = policy.get("release_requirements")
    if not isinstance(requirements, list) or set(requirements) != REQUIRED_RELEASE_REQUIREMENTS:
        errors.append("release requirements drifted from the admitted denominator")
    elif len(requirements) != len(set(requirements)):
        errors.append("release requirements contain duplicates")

    if policy.get("release_authority") != "HUMAN_ONLY":
        errors.append("release authority must remain Human-only")
    return errors


def validate_queue(queue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {"schema", "repository", "active_item", "evidence_ceiling", "items"}
    errors.extend(strict_keys(queue, expected, "provenance queue"))
    if queue.get("schema") != "actiongate-provenance-handoff-queue/v1":
        errors.append("provenance queue schema mismatch")
    if queue.get("repository") != "ed3c/ActionGate":
        errors.append("provenance queue repository mismatch")
    items = queue.get("items")
    if not isinstance(items, list):
        return errors + ["provenance queue items must be an array"]

    ids: set[str] = set()
    active_ids: list[str] = []
    for index, item in enumerate(items):
        prefix = f"queue.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        unknown = set(item) - QUEUE_ITEM_KEYS
        if unknown:
            errors.append(f"{prefix} has unknown keys: {sorted(unknown)}")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not re.fullmatch(r"PV-LH-[0-9]{3}", item_id):
            errors.append(f"{prefix}.id is invalid")
            continue
        if item_id in ids:
            errors.append(f"duplicate queue item id: {item_id}")
        ids.add(item_id)

        state = item.get("state")
        if state not in QUEUE_STATES:
            errors.append(f"{prefix}.state is invalid")
        if isinstance(state, str) and state.startswith("ACTIVE"):
            active_ids.append(item_id)

        for field in ("objective", "entry", "exit"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{prefix}.{field} is invalid")

        commands = item.get("commands_after_binding")
        if commands is not None:
            if not isinstance(commands, list):
                errors.append(f"{prefix}.commands_after_binding must be an array")
            else:
                for command_index, command in enumerate(commands):
                    if (
                        not isinstance(command, list)
                        or not command
                        or not all(isinstance(arg, str) and arg for arg in command)
                    ):
                        errors.append(f"{prefix}.commands_after_binding[{command_index}] must be a non-empty argv array")

        next_items = item.get("next")
        if not isinstance(next_items, list) or not all(isinstance(value, str) for value in next_items):
            errors.append(f"{prefix}.next must be a string array")
        human_owned = item.get("human_owned")
        if not isinstance(human_owned, list) or not all(isinstance(value, str) for value in human_owned):
            errors.append(f"{prefix}.human_owned must be a string array")

        serialized = json.dumps(item, sort_keys=True)
        has_placeholder = bool(PLACEHOLDER.search(serialized))
        if has_placeholder:
            if state not in {
                "ACTIVE_INPUT_COLLECTION",
                "BLOCKED_BY_PV_LH_001",
                "BLOCKED_BY_PV_LH_002",
                "BLOCKED_BY_PV_LH_003_AND_PV_LH_004",
                "HUMAN_ADMIT_REQUIRED",
            }:
                errors.append(f"{prefix} contains unresolved placeholders in an executable state")
            if state == "ACTIVE_INPUT_COLLECTION" and not isinstance(item.get("parameter_law"), str):
                errors.append(f"{prefix} active placeholder input requires parameter_law")

    if active_ids != [queue.get("active_item")]:
        errors.append("queue must have exactly one active item matching active_item")

    for item in items:
        if not isinstance(item, dict):
            continue
        for successor in item.get("next", []) if isinstance(item.get("next"), list) else []:
            if successor not in ids:
                errors.append(f"{item.get('id')} references unknown successor {successor}")
    return errors


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_subject(root: Path) -> tuple[str, str]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=root, text=True).strip()
    return commit, tree


def validate_candidate_binding(root: Path, candidate_sha: Any, candidate_tree: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(candidate_sha, str) or not HEX40.fullmatch(candidate_sha):
        return ["candidate subject SHA is invalid"]
    if not isinstance(candidate_tree, str) or not HEX40.fullmatch(candidate_tree):
        return ["candidate subject tree is invalid"]
    try:
        observed_tree = subprocess.check_output(
            ["git", "rev-parse", f"{candidate_sha}^{{tree}}"], cwd=root, text=True
        ).strip()
    except subprocess.CalledProcessError:
        return ["candidate subject is not present in the repository"]
    if observed_tree != candidate_tree:
        errors.append("candidate subject tree mismatch")
    try:
        subprocess.check_call(
            ["git", "merge-base", "--is-ancestor", candidate_sha, "HEAD"],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        errors.append("candidate subject is not an ancestor of the receipt head")
    return errors


def validate_clean_room_receipt(receipt: dict[str, Any], policy: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema", "session_id", "repository", "subject_sha", "output_commit", "output_tree",
        "started_at", "completed_at", "runtime", "permitted_sources", "forbidden_sources",
        "personal_device_used", "personal_account_used", "employer_source_accessed",
        "employer_resources_used", "employer_time_used", "private_urls_echoed",
        "changed_paths", "dco_state", "dco_evidence", "evidence_state",
    }
    errors.extend(strict_keys(receipt, expected, "clean-room receipt"))
    if receipt.get("schema") != "clean-room-session-receipt/v1":
        errors.append("clean-room receipt schema mismatch")
    if receipt.get("repository") != "ed3c/ActionGate":
        errors.append("clean-room receipt repository mismatch")
    if receipt.get("subject_sha") != "ABSENT_AT_START" and not (
        isinstance(receipt.get("subject_sha"), str) and HEX40.fullmatch(receipt["subject_sha"])
    ):
        errors.append("clean-room subject_sha is invalid")
    for field in ("output_commit", "output_tree"):
        value = receipt.get(field)
        if not isinstance(value, str) or not HEX40.fullmatch(value):
            errors.append(f"clean-room {field} is invalid")
    if (
        isinstance(receipt.get("output_commit"), str)
        and isinstance(receipt.get("output_tree"), str)
        and HEX40.fullmatch(receipt["output_commit"])
        and HEX40.fullmatch(receipt["output_tree"])
    ):
        errors.extend(validate_candidate_binding(root, receipt["output_commit"], receipt["output_tree"]))

    if not valid_datetime(receipt.get("started_at")) or not valid_datetime(receipt.get("completed_at")):
        errors.append("clean-room timestamps must be timezone-aware")
    else:
        if datetime.fromisoformat(receipt["completed_at"].replace("Z", "+00:00")) < datetime.fromisoformat(
            receipt["started_at"].replace("Z", "+00:00")
        ):
            errors.append("clean-room completed_at precedes started_at")

    for field in ("personal_device_used", "personal_account_used"):
        if receipt.get(field) is not True:
            errors.append(f"clean-room {field} must be true")
    for field in (
        "employer_source_accessed", "employer_resources_used",
        "employer_time_used", "private_urls_echoed",
    ):
        if receipt.get(field) is not False:
            errors.append(f"clean-room {field} must be false")

    permitted = receipt.get("permitted_sources")
    if not isinstance(permitted, list) or not permitted:
        errors.append("clean-room permitted_sources must be non-empty")
    else:
        seen_sources: set[tuple[Any, ...]] = set()
        for index, source in enumerate(permitted):
            prefix = f"permitted_sources[{index}]"
            if not isinstance(source, dict):
                errors.append(f"{prefix} must be an object")
                continue
            allowed = {"type", "id", "locator", "commit", "tree"}
            errors.extend(strict_keys(source, allowed, prefix))
            source_type = source.get("type")
            if source_type not in {"PUBLIC_GIT", "PUBLIC_SPEC", "ACTIONGATE_SUBJECT", "SYNTHETIC_FIXTURE"}:
                errors.append(f"{prefix}.type is invalid")
            source_id = source.get("id")
            if not isinstance(source_id, str) or not source_id.strip():
                errors.append(f"{prefix}.id is invalid")
            locator = source.get("locator")
            if not isinstance(locator, str) or not locator:
                errors.append(f"{prefix}.locator is invalid")
            elif source_type in {"PUBLIC_GIT", "PUBLIC_SPEC"}:
                if not public_https_url_is_sane(locator):
                    errors.append(f"{prefix}.locator is not a sane public URL")
            elif not relative_path_is_safe(locator):
                errors.append(f"{prefix}.locator must be an exact repository-relative path")

            commit = source.get("commit")
            tree = source.get("tree")
            if source_type in {"PUBLIC_GIT", "ACTIONGATE_SUBJECT"}:
                for field, value in (("commit", commit), ("tree", tree)):
                    if not isinstance(value, str) or not HEX40.fullmatch(value):
                        errors.append(f"{prefix}.{field} must be exact for {source_type}")
            else:
                for field, value in (("commit", commit), ("tree", tree)):
                    if value is not None and (not isinstance(value, str) or not HEX40.fullmatch(value)):
                        errors.append(f"{prefix}.{field} is invalid")
                if source_type == "SYNTHETIC_FIXTURE" and (commit is not None or tree is not None):
                    errors.append(f"{prefix} synthetic fixture must not claim a Git subject")

            source_key = (source_type, source_id, locator, commit, tree)
            if source_key in seen_sources:
                errors.append(f"duplicate permitted source at {prefix}")
            seen_sources.add(source_key)

    forbidden = receipt.get("forbidden_sources")
    required_forbidden = set(policy.get("forbidden_source_classes", []))
    if not isinstance(forbidden, list) or not required_forbidden.issubset(set(forbidden)):
        errors.append("clean-room forbidden_sources does not cover the policy")

    changed = receipt.get("changed_paths")
    if not isinstance(changed, list) or not changed:
        errors.append("clean-room changed_paths must be non-empty")
    else:
        if len(changed) != len(set(changed)):
            errors.append("clean-room changed_paths contains duplicates")
        for path in changed:
            if not isinstance(path, str) or not relative_path_is_safe(path):
                errors.append("clean-room changed_paths contains unsafe path")
            elif not (root / path).exists():
                errors.append(f"clean-room changed path does not exist: {path}")

    dco_state = receipt.get("dco_state")
    if dco_state not in {"PASS", "NOT_APPLICABLE_WITH_EVIDENCE"}:
        errors.append("clean-room dco_state is not admitted")
    dco_evidence = receipt.get("dco_evidence")
    if not isinstance(dco_evidence, str) or not dco_evidence.strip():
        errors.append("clean-room dco_evidence is required")
    if dco_state == "PASS" and "Signed-off-by:" not in dco_evidence:
        errors.append("clean-room DCO PASS must identify the observed Signed-off-by trailer")
    if receipt.get("evidence_state") != "PASS":
        errors.append("clean-room receipt must be PASS for release")
    return errors


def validate_independent_review(
    receipt: dict[str, Any],
    candidate_sha: str,
    candidate_tree: str,
    root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema", "review_id", "repository", "base_sha", "subject_sha", "subject_tree",
        "reviewed_at", "reviewer_kind", "builder_participation", "read_only",
        "changed_path_denominator", "upstream_lock_sha256", "imported_paths_sha256",
        "patch_lineage_sha256", "sbom_sha256", "workflow_run_id", "workflow_job_id",
        "workflow_conclusion", "verdict", "falsifiers",
        "private_urls_echoed", "dissent", "evidence_ceiling",
    }
    errors.extend(strict_keys(receipt, expected, "independent review receipt"))
    if receipt.get("schema") != "independent-provenance-review-receipt/v1":
        errors.append("independent review schema mismatch")
    if receipt.get("repository") != "ed3c/ActionGate":
        errors.append("independent review repository mismatch")
    base_sha = receipt.get("base_sha")
    if not isinstance(base_sha, str) or not HEX40.fullmatch(base_sha):
        errors.append("independent review base_sha is invalid")
    if receipt.get("subject_sha") != candidate_sha or receipt.get("subject_tree") != candidate_tree:
        errors.append("independent review candidate subject mismatch")
    if not valid_datetime(receipt.get("reviewed_at")):
        errors.append("independent review timestamp is invalid")
    if receipt.get("reviewer_kind") not in {"INDEPENDENT_HUMAN", "INDEPENDENT_EXTERNAL_AGENT"}:
        errors.append("independent reviewer kind is invalid")
    if receipt.get("builder_participation") is not False or receipt.get("read_only") is not True:
        errors.append("independent review boundary is not satisfied")

    denominator = receipt.get("changed_path_denominator")
    if not isinstance(denominator, int) or isinstance(denominator, bool) or denominator <= 0:
        errors.append("independent review denominator is invalid")

    if root is not None and isinstance(base_sha, str) and HEX40.fullmatch(base_sha):
        try:
            subprocess.check_call(
                ["git", "merge-base", "--is-ancestor", base_sha, candidate_sha],
                cwd=root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            errors.append("independent review base is not an ancestor of candidate")
        else:
            observed = subprocess.check_output(
                ["git", "diff", "--name-only", f"{base_sha}..{candidate_sha}"],
                cwd=root,
                text=True,
            ).splitlines()
            if denominator != len(set(observed)):
                errors.append("independent review changed-path denominator mismatch")

    for field in ("upstream_lock_sha256", "imported_paths_sha256", "patch_lineage_sha256"):
        value = receipt.get(field)
        if not isinstance(value, str) or not HEX64.fullmatch(value):
            errors.append(f"independent review {field} is invalid")
    sbom_digest = receipt.get("sbom_sha256")
    if sbom_digest is not None and (not isinstance(sbom_digest, str) or not HEX64.fullmatch(sbom_digest)):
        errors.append("independent review sbom_sha256 is invalid")

    for field in ("workflow_run_id", "workflow_job_id"):
        value = receipt.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            errors.append(f"independent review {field} is invalid")
    if receipt.get("workflow_conclusion") != "SUCCESS":
        errors.append("independent review requires a successful exact-subject workflow")

    falsifiers = receipt.get("falsifiers")
    seen: set[str] = set()
    if not isinstance(falsifiers, list) or not falsifiers:
        errors.append("independent review falsifiers must be non-empty")
    else:
        for index, item in enumerate(falsifiers):
            if not isinstance(item, dict) or set(item) != {"id", "state", "detail"}:
                errors.append(f"independent falsifier[{index}] shape is invalid")
                continue
            item_id = item["id"]
            if item_id in seen:
                errors.append(f"duplicate independent falsifier id: {item_id}")
            seen.add(item_id)
            if item["state"] not in {"PASS", "FAIL", "NOT_EXERCISED"}:
                errors.append(f"independent falsifier[{index}] state is invalid")
            if not isinstance(item["detail"], str) or not item["detail"].strip():
                errors.append(f"independent falsifier[{index}] detail is empty")
        missing = REQUIRED_INDEPENDENT_FALSIFIERS - seen
        unknown = seen - REQUIRED_INDEPENDENT_FALSIFIERS
        if missing:
            errors.append(f"independent falsifier denominator missing: {sorted(missing)}")
        if unknown:
            errors.append(f"independent falsifier denominator has unknown IDs: {sorted(unknown)}")

    verdict = receipt.get("verdict")
    if verdict not in {"ADMIT_STATIC_PROVENANCE", "BLOCK", "REPLAN"}:
        errors.append("independent review verdict is invalid")
    if verdict == "ADMIT_STATIC_PROVENANCE" and isinstance(falsifiers, list):
        if any(not isinstance(item, dict) or item.get("state") != "PASS" for item in falsifiers):
            errors.append("independent admission requires every falsifier PASS")

    dissent = receipt.get("dissent")
    if not isinstance(dissent, list) or not all(isinstance(item, str) for item in dissent):
        errors.append("independent review dissent must be a string array")
    elif verdict in {"BLOCK", "REPLAN"} and not dissent:
        errors.append("BLOCK or REPLAN requires explicit dissent")

    if receipt.get("private_urls_echoed") is not False:
        errors.append("independent review leaked a private locator")
    if receipt.get("evidence_ceiling") != "STATIC_PROVENANCE_CONTROL_ONLY":
        errors.append("independent review evidence ceiling widened")
    return errors


def validate_outside_review(receipt: dict[str, Any], candidate_sha: str, candidate_tree: str) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema", "review_id", "repository", "subject_sha", "subject_tree", "reviewed_at",
        "employment_agreement_reviewed", "invention_assignment_reviewed",
        "confidentiality_reviewed", "moonlighting_conflict_reviewed",
        "public_upstream_only", "employer_resources_used",
        "employer_confidential_material_used", "business_overlap_state",
        "written_notice_state", "counsel_state", "legal_admission", "private_urls_echoed",
    }
    errors.extend(strict_keys(receipt, expected, "outside-project review receipt"))
    if receipt.get("schema") != "outside-project-review-receipt/v1":
        errors.append("outside-project review schema mismatch")
    if receipt.get("repository") != "ed3c/ActionGate":
        errors.append("outside-project review repository mismatch")
    if receipt.get("subject_sha") != candidate_sha or receipt.get("subject_tree") != candidate_tree:
        errors.append("outside-project review candidate subject mismatch")
    if not valid_datetime(receipt.get("reviewed_at")):
        errors.append("outside-project review timestamp is invalid")

    for field in (
        "employment_agreement_reviewed", "invention_assignment_reviewed",
        "confidentiality_reviewed", "moonlighting_conflict_reviewed",
        "public_upstream_only", "employer_resources_used",
        "employer_confidential_material_used", "private_urls_echoed",
    ):
        if not isinstance(receipt.get(field), bool):
            errors.append(f"outside-project {field} must be boolean")

    if receipt.get("business_overlap_state") not in {
        "PRIVATE_REVIEW_REQUIRED", "PRIVATE_REVIEW_COMPLETE", "UNRESOLVED"
    }:
        errors.append("outside-project business_overlap_state is invalid")
    if receipt.get("written_notice_state") not in {
        "NOT_REVIEWED", "NOT_REQUIRED", "REQUIRED", "OBTAINED"
    }:
        errors.append("outside-project written_notice_state is invalid")
    if receipt.get("counsel_state") not in {
        "NOT_REVIEWED", "NOT_REQUIRED", "REVIEWED", "REQUIRED"
    }:
        errors.append("outside-project counsel_state is invalid")
    if receipt.get("legal_admission") not in {
        "HUMAN_COUNSEL_REQUIRED", "HUMAN_ADMITTED", "BLOCKED"
    }:
        errors.append("outside-project legal_admission is invalid")

    if receipt.get("legal_admission") == "HUMAN_ADMITTED":
        for field in (
            "employment_agreement_reviewed", "invention_assignment_reviewed",
            "confidentiality_reviewed", "moonlighting_conflict_reviewed", "public_upstream_only",
        ):
            if receipt.get(field) is not True:
                errors.append(f"Human legal admission requires {field}=true")
        if receipt.get("employer_resources_used") is not False:
            errors.append("Human legal admission requires employer_resources_used=false")
        if receipt.get("employer_confidential_material_used") is not False:
            errors.append("Human legal admission requires employer_confidential_material_used=false")
        if receipt.get("business_overlap_state") != "PRIVATE_REVIEW_COMPLETE":
            errors.append("Human legal admission requires completed private business-overlap review")
        if receipt.get("written_notice_state") not in {"NOT_REQUIRED", "OBTAINED"}:
            errors.append("Human legal admission requires written notice disposition")
        if receipt.get("counsel_state") not in {"NOT_REQUIRED", "REVIEWED"}:
            errors.append("Human legal admission requires counsel disposition")
    if receipt.get("private_urls_echoed") is not False:
        errors.append("outside-project receipt leaked a private locator")
    return errors


def validate_spdx_sbom(
    sbom: dict[str, Any],
    candidate_sha: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if sbom.get("spdxVersion") != "SPDX-2.3":
        errors.append("SBOM must use SPDX-2.3")
    if sbom.get("dataLicense") != "CC0-1.0":
        errors.append("SBOM dataLicense must be CC0-1.0")
    if not isinstance(sbom.get("SPDXID"), str) or not sbom["SPDXID"].startswith("SPDXRef-"):
        errors.append("SBOM SPDXID is invalid")
    name = sbom.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("SBOM name is invalid")
    namespace = sbom.get("documentNamespace")
    if not isinstance(namespace, str) or not public_https_url_is_sane(namespace):
        errors.append("SBOM documentNamespace is invalid or non-public")
    if PLACEHOLDER.search(json.dumps(sbom, sort_keys=True)):
        errors.append("SBOM contains a placeholder")

    creation = sbom.get("creationInfo")
    if not isinstance(creation, dict):
        errors.append("SBOM creationInfo is missing")
    else:
        if not valid_datetime(creation.get("created")):
            errors.append("SBOM creation timestamp is invalid")
        creators = creation.get("creators")
        if not isinstance(creators, list) or not creators or not all(isinstance(v, str) and v for v in creators):
            errors.append("SBOM creators must be non-empty")

    document_describes = sbom.get("documentDescribes")
    if not isinstance(document_describes, list) or not document_describes:
        errors.append("SBOM documentDescribes must be non-empty")
        document_describes = []

    packages = sbom.get("packages")
    if not isinstance(packages, list) or not packages:
        errors.append("SBOM packages must be non-empty")
        packages = []

    package_ids: set[str] = set()
    root_package_seen = False
    for index, package in enumerate(packages):
        prefix = f"SBOM packages[{index}]"
        if not isinstance(package, dict):
            errors.append(f"{prefix} must be an object")
            continue
        spdx_id = package.get("SPDXID")
        if not isinstance(spdx_id, str) or not spdx_id.startswith("SPDXRef-"):
            errors.append(f"{prefix}.SPDXID is invalid")
        elif spdx_id in package_ids:
            errors.append(f"duplicate SBOM package SPDXID: {spdx_id}")
        else:
            package_ids.add(spdx_id)
        for field in ("name", "downloadLocation", "licenseConcluded", "licenseDeclared"):
            value = package.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} is invalid")
        for field in ("licenseConcluded", "licenseDeclared"):
            if package.get(field) in {"NOASSERTION", "NONE", "UNKNOWN"}:
                errors.append(f"{prefix}.{field} is not admitted")
        if spdx_id in document_describes:
            root_package_seen = True
            if candidate_sha is not None and package.get("versionInfo") != candidate_sha:
                errors.append("SBOM root package versionInfo is not the exact candidate SHA")

    unknown_described = set(document_describes) - package_ids
    if unknown_described:
        errors.append(f"SBOM documentDescribes references unknown packages: {sorted(unknown_described)}")
    if not root_package_seen:
        errors.append("SBOM does not describe a concrete root package")

    relationships = sbom.get("relationships")
    if not isinstance(relationships, list):
        errors.append("SBOM relationships must be an array")
    return errors


def validate_release_admission(
    receipt: dict[str, Any],
    candidate_sha: str,
    candidate_tree: str,
    independent_digest: str,
    outside_digest: str,
    sbom_digest: str,
) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema", "repository", "subject_sha", "subject_tree", "decision", "decided_at",
        "decider_kind", "independent_review_sha256", "outside_project_review_sha256",
        "sbom_sha256", "notices_verified", "private_urls_echoed",
    }
    errors.extend(strict_keys(receipt, expected, "release admission receipt"))
    if receipt.get("schema") != "actiongate-release-admission/v1":
        errors.append("release admission schema mismatch")
    if receipt.get("repository") != "ed3c/ActionGate":
        errors.append("release admission repository mismatch")
    if receipt.get("subject_sha") != candidate_sha or receipt.get("subject_tree") != candidate_tree:
        errors.append("release admission candidate subject mismatch")
    if receipt.get("decision") != "RELEASE_ELIGIBLE":
        errors.append("release admission decision is not RELEASE_ELIGIBLE")
    if not valid_datetime(receipt.get("decided_at")):
        errors.append("release admission timestamp is invalid")
    if receipt.get("decider_kind") not in {"HUMAN_REPOSITORY_OWNER", "HUMAN_LEGAL_AUTHORITY"}:
        errors.append("release admission decider is invalid")
    if receipt.get("independent_review_sha256") != independent_digest:
        errors.append("release admission independent-review digest mismatch")
    if receipt.get("outside_project_review_sha256") != outside_digest:
        errors.append("release admission outside-review digest mismatch")
    if receipt.get("sbom_sha256") != sbom_digest:
        errors.append("release admission SBOM digest mismatch")
    if receipt.get("notices_verified") is not True:
        errors.append("release admission requires notices_verified=true")
    if receipt.get("private_urls_echoed") is not False:
        errors.append("release admission leaked a private locator")
    return errors


def validate_release(root: Path, lock: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    if lock.get("release_state") != "RELEASE_ELIGIBLE":
        return []
    errors: list[str] = []

    clean_room_paths = sorted((root / ".provenance/receipts").glob("clean-room-session-*.json"))
    clean_receipts: list[dict[str, Any]] = []
    if not clean_room_paths:
        errors.append("release eligibility requires at least one clean-room Session receipt")
    for path in clean_room_paths:
        try:
            receipt = load_json(path)
            clean_receipts.append(receipt)
            errors.extend(validate_clean_room_receipt(receipt, policy, root))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid clean-room receipt {path.name}: {exc}")

    independent_path = root / ".provenance/receipts/independent-provenance-review.json"
    outside_path = root / ".provenance/receipts/outside-project-review-redacted.json"
    release_path = root / ".provenance/receipts/release-admission.json"
    sbom_path = root / "sbom/actiongate.spdx.json"
    for path in (independent_path, outside_path, release_path, sbom_path):
        if not path.is_file():
            errors.append(f"release eligibility missing artifact: {path.relative_to(root)}")
    if errors:
        return errors

    try:
        independent = load_json(independent_path)
        outside = load_json(outside_path)
        release = load_json(release_path)
        sbom = load_json(sbom_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return errors + [f"release artifact load failed: {exc}"]

    candidate_sha = release.get("subject_sha")
    candidate_tree = release.get("subject_tree")
    errors.extend(validate_candidate_binding(root, candidate_sha, candidate_tree))

    if isinstance(candidate_sha, str) and HEX40.fullmatch(candidate_sha):
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", f"{candidate_sha}..HEAD"], cwd=root, text=True
        ).splitlines()
        unexpected = sorted(set(changed) - RELEASE_SUCCESSOR_ALLOWED_PATHS)
        if unexpected:
            errors.append(f"release successor contains non-admission changes: {unexpected}")

    # A clean-room receipt may be earlier than the frozen release candidate, but never later or unrelated.
    covered_paths: set[str] = set()
    if isinstance(candidate_sha, str) and HEX40.fullmatch(candidate_sha):
        for receipt in clean_receipts:
            output_commit = receipt.get("output_commit")
            if isinstance(output_commit, str) and HEX40.fullmatch(output_commit):
                try:
                    subprocess.check_call(
                        ["git", "merge-base", "--is-ancestor", output_commit, candidate_sha],
                        cwd=root,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except subprocess.CalledProcessError:
                    errors.append(f"clean-room output is not an ancestor of release candidate: {output_commit}")
            if isinstance(receipt.get("changed_paths"), list):
                covered_paths.update(
                    value for value in receipt["changed_paths"] if isinstance(value, str)
                )

    imports = load_json(root / ".provenance/imported-paths.json")
    lineage = load_json(root / ".provenance/patch-lineage.json")
    required_covered_paths = {
        mapping.get("target_path")
        for mapping in imports.get("mappings", [])
        if isinstance(mapping, dict) and isinstance(mapping.get("target_path"), str)
    } | {
        record.get("target_path")
        for record in lineage.get("records", [])
        if isinstance(record, dict) and isinstance(record.get("target_path"), str)
    }
    missing_clean_coverage = sorted(required_covered_paths - covered_paths)
    if missing_clean_coverage:
        errors.append(f"clean-room receipts do not cover source-bearing paths: {missing_clean_coverage}")

    errors.extend(validate_independent_review(independent, candidate_sha, candidate_tree, root))
    errors.extend(validate_outside_review(outside, candidate_sha, candidate_tree))
    errors.extend(validate_spdx_sbom(sbom, candidate_sha))

    actual_lock_digest = sha256_file(root / ".provenance/upstreams.lock.json")
    actual_imports_digest = sha256_file(root / ".provenance/imported-paths.json")
    actual_lineage_digest = sha256_file(root / ".provenance/patch-lineage.json")
    actual_sbom_digest = sha256_file(sbom_path)
    if independent.get("upstream_lock_sha256") != actual_lock_digest:
        errors.append("independent review upstream-lock digest mismatch")
    if independent.get("imported_paths_sha256") != actual_imports_digest:
        errors.append("independent review imported-paths digest mismatch")
    if independent.get("patch_lineage_sha256") != actual_lineage_digest:
        errors.append("independent review patch-lineage digest mismatch")
    if independent.get("sbom_sha256") != actual_sbom_digest:
        errors.append("independent review SBOM digest mismatch")

    errors.extend(validate_release_admission(
        release,
        candidate_sha,
        candidate_tree,
        sha256_file(independent_path),
        sha256_file(outside_path),
        actual_sbom_digest,
    ))
    if independent.get("verdict") != "ADMIT_STATIC_PROVENANCE":
        errors.append("release requires independent ADMIT_STATIC_PROVENANCE")
    if outside.get("legal_admission") != "HUMAN_ADMITTED":
        errors.append("release requires Human legal admission")
    return errors


def validate_control(root: Path = ROOT) -> list[str]:
    errors = [
        f"missing required path: {path}"
        for path in REQUIRED_PATHS
        if not (root / path).exists()
    ]
    if errors:
        return errors

    try:
        lock = load_json(root / ".provenance/upstreams.lock.json")
        imports = load_json(root / ".provenance/imported-paths.json")
        lineage = load_json(root / ".provenance/patch-lineage.json")
        policy = load_json(root / ".provenance/policy.json")
        queue = load_json(root / ".provenance/local-handoff-queue.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"control JSON load failed: {exc}"]

    errors.extend(validate_schema_documents(root))
    errors.extend(validate_policy(policy))
    errors.extend(validate_lock(lock))
    if policy.get("upstream_state") != lock.get("state"):
        errors.append("policy upstream_state does not match upstream lock state")
    errors.extend(validate_imports(imports, lock, root))
    errors.extend(validate_patch_lineage(lineage, lock, imports, root))
    errors.extend(scan_private_material(root, policy))
    errors.extend(validate_queue(queue))

    if policy.get("current_control_state") != "PROVENANCE_CONTROL_PLANE_IMPLEMENTED":
        errors.append("control state mismatch")
    if policy.get("release_authority") != "HUMAN_ONLY":
        errors.append("release authority must remain Human-only")
    if queue.get("active_item") != "PV-LH-001":
        errors.append("PV-LH-001 must be the active provenance handoff")

    errors.extend(validate_release(root, lock, policy))

    license_path = root / "LICENSE"
    if not license_path.exists():
        errors.append("root LICENSE is missing")
    else:
        license_text = license_path.read_text(encoding="utf-8", errors="ignore")
        if "Apache License" not in license_text or "Version 2.0" not in license_text:
            errors.append("root LICENSE is not recognized as Apache-2.0 text")

    return sorted(set(errors))


def git_json_at_commit(root: Path, commit: str, path: str) -> dict[str, Any] | None:
    try:
        raw = subprocess.check_output(
            ["git", "show", f"{commit}:{path}"], cwd=root, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def commit_requires_dco(root: Path, commit: str) -> bool:
    output = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit],
        cwd=root,
        text=True,
    )
    paths = [line.strip() for line in output.splitlines() if line.strip()]
    lock = git_json_at_commit(root, commit, ".provenance/upstreams.lock.json") or {}
    imports = git_json_at_commit(root, commit, ".provenance/imported-paths.json") or {}
    source_inventory_nonempty = bool(lock.get("upstreams") or imports.get("mappings"))
    for path in paths:
        if path.startswith(PRODUCT_SOURCE_PREFIXES) or Path(path).name in DEPENDENCY_FILES:
            return True
        if source_inventory_nonempty and path in {
            ".provenance/upstreams.lock.json",
            ".provenance/imported-paths.json",
            ".provenance/patch-lineage.json",
        }:
            return True
    return False


def scan_commit_history(root: Path, commits: list[str], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    excluded = set(policy.get("private_scan_exclusions", []))
    needles = [needle for needle in policy.get("forbidden_public_substrings", []) if isinstance(needle, str) and needle]
    for commit in commits:
        paths = subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit],
            cwd=root,
            text=True,
        ).splitlines()
        for relative in paths:
            if relative in excluded:
                continue
            try:
                raw = subprocess.check_output(
                    ["git", "show", f"{commit}:{relative}"], cwd=root, stderr=subprocess.DEVNULL
                )
                text = raw.decode("utf-8")
            except (subprocess.CalledProcessError, UnicodeDecodeError):
                continue
            for needle in needles:
                if needle in text:
                    errors.append(f"{commit}: forbidden public substring persisted in {relative}")
    return errors


def check_commits(root: Path, base: str, head: str) -> list[str]:
    errors: list[str] = []
    try:
        subprocess.check_call(
            ["git", "merge-base", "--is-ancestor", base, head],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return ["base is not an ancestor of head; commit denominator is invalid"]

    commits = subprocess.check_output(
        ["git", "rev-list", "--reverse", f"{base}..{head}"], cwd=root, text=True
    ).splitlines()
    if not commits:
        errors.append("commit range is empty")
        return errors

    policy = load_json(root / ".provenance/policy.json")
    errors.extend(scan_commit_history(root, commits, policy))

    for commit in commits:
        if not commit_requires_dco(root, commit):
            continue
        message = subprocess.check_output(
            ["git", "show", "-s", "--format=%B", commit], cwd=root, text=True
        )
        if not re.search(r"^Signed-off-by:\s+.+\s+<[^<>@\s]+@[^<>\s]+>$", message, re.M):
            errors.append(f"{commit}: source-bearing commit lacks a real DCO sign-off")
    return errors


def hash_license(path: Path) -> int:
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2
    print(hashlib.sha256(path.read_bytes()).hexdigest())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-commits", nargs=2, metavar=("BASE", "HEAD"))
    parser.add_argument("--hash-license", type=Path)
    args = parser.parse_args()

    if args.hash_license:
        return hash_license(args.hash_license)

    errors = validate_control(ROOT)
    if args.check_commits:
        errors.extend(check_commits(ROOT, *args.check_commits))

    if errors:
        print("ActionGate provenance control: FAIL", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ActionGate provenance control: PASS")
    print("Upstream/import/clean-room/independent/legal/release lanes: NOT_EXERCISED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
