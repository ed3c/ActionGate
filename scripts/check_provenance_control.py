#!/usr/bin/env python3
"""Fail-closed checks for ActionGate independent-source provenance controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
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
    ".provenance/schemas/outside-project-review-receipt.schema.json",
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

ALLOWED_RELATIONSHIPS = {
    "DERIVED_SOURCE",
    "DEPENDENCY",
    "REFERENCE_IMPLEMENTATION",
    "SPECIFICATION_ONLY",
    "BUILD_TOOLING",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def relative_path_is_safe(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\x00" not in value


def overlapping_paths(paths: Iterable[str]) -> list[tuple[str, str]]:
    normalized = sorted({path.strip("/") for path in paths})
    conflicts: list[tuple[str, str]] = []
    for index, left in enumerate(normalized):
        for right in normalized[index + 1 :]:
            if right == left or right.startswith(left + "/"):
                conflicts.append((left, right))
    return conflicts


def validate_lock(lock: dict[str, Any]) -> list[str]:
    errors: list[str] = []
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
    else:
        errors.append(f"unsupported upstream state: {state!r}")

    seen: set[str] = set()
    for index, item in enumerate(upstreams):
        prefix = f"upstreams[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        upstream_id = item.get("id")
        if not isinstance(upstream_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,63}", upstream_id):
            errors.append(f"{prefix}.id is invalid")
        elif upstream_id in seen:
            errors.append(f"duplicate upstream id: {upstream_id}")
        else:
            seen.add(upstream_id)

        repository = item.get("repository")
        if not isinstance(repository, str) or not repository.startswith("https://"):
            errors.append(f"{prefix}.repository must be a public HTTPS URL")
        elif PLACEHOLDER.search(repository):
            errors.append(f"{prefix}.repository contains a placeholder")

        for field, pattern in (("commit", HEX40), ("tree", HEX40), ("license_sha256", HEX64)):
            value = item.get(field)
            if not isinstance(value, str) or not pattern.fullmatch(value):
                errors.append(f"{prefix}.{field} must be exact lowercase hex")
            elif PLACEHOLDER.search(value):
                errors.append(f"{prefix}.{field} contains a placeholder")

        license_spdx = item.get("license_spdx")
        if not isinstance(license_spdx, str) or not license_spdx or license_spdx in {"UNKNOWN", "NOASSERTION"}:
            errors.append(f"{prefix}.license_spdx is not admitted")

        if item.get("relationship") not in ALLOWED_RELATIONSHIPS:
            errors.append(f"{prefix}.relationship is invalid")

        for field in ("imported_paths", "excluded_paths"):
            values = item.get(field)
            if not isinstance(values, list):
                errors.append(f"{prefix}.{field} must be an array")
                continue
            for value in values:
                if not isinstance(value, str) or not relative_path_is_safe(value):
                    errors.append(f"{prefix}.{field} contains an unsafe path")

    if lock.get("release_state") == "RELEASE_ELIGIBLE":
        if lock.get("legal_admission") != "HUMAN_ADMITTED":
            errors.append("release eligibility requires Human legal admission")
        if not upstreams:
            errors.append("release eligibility requires an admitted source inventory")

    return errors


def validate_imports(imports: dict[str, Any], lock: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if imports.get("schema") != "actiongate-imported-paths/v1":
        errors.append("imported-paths schema mismatch")
    if imports.get("repository") != "ed3c/ActionGate":
        errors.append("imported-paths repository mismatch")

    mappings = imports.get("mappings")
    if not isinstance(mappings, list):
        return errors + ["mappings must be an array"]

    upstream_ids = {
        item["id"] for item in lock.get("upstreams", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    targets: list[str] = []
    for index, mapping in enumerate(mappings):
        prefix = f"mappings[{index}]"
        if not isinstance(mapping, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if mapping.get("upstream_id") not in upstream_ids:
            errors.append(f"{prefix} references an unadmitted upstream")
        for field in ("source_path", "target_path"):
            value = mapping.get(field)
            if not isinstance(value, str) or not relative_path_is_safe(value):
                errors.append(f"{prefix}.{field} is unsafe")
        source_blob = mapping.get("source_blob")
        if not isinstance(source_blob, str) or not HEX40.fullmatch(source_blob):
            errors.append(f"{prefix}.source_blob must be exact lowercase hex")
        target = mapping.get("target_path")
        if isinstance(target, str):
            targets.append(target)

    for left, right in overlapping_paths(targets):
        errors.append(f"overlapping imported target paths: {left!r} and {right!r}")

    if lock.get("state") == "UPSTREAM_SELECTION_REQUIRED" and mappings:
        errors.append("imports exist while upstream selection is required")
    if imports.get("state") == "NO_IMPORTS_ADMITTED" and mappings:
        errors.append("NO_IMPORTS_ADMITTED must have zero mappings")
    if imports.get("state") == "IMPORTS_CLASSIFIED" and not mappings:
        errors.append("IMPORTS_CLASSIFIED requires mappings")

    return errors


def validate_patch_lineage(lineage: dict[str, Any], lock: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if lineage.get("schema") != "actiongate-patch-lineage/v1":
        errors.append("patch-lineage schema mismatch")
    records = lineage.get("records")
    if not isinstance(records, list):
        return errors + ["patch records must be an array"]
    upstream_ids = {
        item["id"] for item in lock.get("upstreams", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        authorship = record.get("authorship")
        upstream_id = record.get("upstream_id")
        upstream_blob = record.get("upstream_blob")
        if authorship in {"DERIVED_PATCH", "MECHANICAL_TRANSFORM"}:
            if upstream_id not in upstream_ids:
                errors.append(f"{prefix} derived patch lacks admitted upstream")
            if not isinstance(upstream_blob, str) or not HEX40.fullmatch(upstream_blob):
                errors.append(f"{prefix} derived patch lacks exact upstream blob")
        elif authorship == "ORIGINAL_PATCH":
            if upstream_id is not None or upstream_blob is not None:
                errors.append(f"{prefix} original patch must not claim upstream blob")
        else:
            errors.append(f"{prefix}.authorship is invalid")
        target = record.get("target_path")
        if not isinstance(target, str) or not relative_path_is_safe(target):
            errors.append(f"{prefix}.target_path is unsafe")
        receipt = record.get("receipt")
        if not isinstance(receipt, str) or not relative_path_is_safe(receipt):
            errors.append(f"{prefix}.receipt is unsafe")

    if lineage.get("state") == "BASELINE_ONLY" and records:
        errors.append("BASELINE_ONLY must have zero patch records")
    if lineage.get("state") == "PATCHES_RECORDED" and not records:
        errors.append("PATCHES_RECORDED requires records")
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


def validate_control(root: Path = ROOT) -> list[str]:
    errors = [
        f"missing required path: {path}"
        for path in REQUIRED_PATHS
        if not (root / path).exists()
    ]
    if errors:
        return errors

    lock = load_json(root / ".provenance/upstreams.lock.json")
    imports = load_json(root / ".provenance/imported-paths.json")
    lineage = load_json(root / ".provenance/patch-lineage.json")
    policy = load_json(root / ".provenance/policy.json")
    queue = load_json(root / ".provenance/local-handoff-queue.json")

    errors.extend(validate_lock(lock))
    errors.extend(validate_imports(imports, lock))
    errors.extend(validate_patch_lineage(lineage, lock))
    errors.extend(scan_private_material(root, policy))

    if policy.get("current_control_state") != "PROVENANCE_CONTROL_PLANE_IMPLEMENTED":
        errors.append("control state mismatch")
    if policy.get("release_authority") != "HUMAN_ONLY":
        errors.append("release authority must remain Human-only")
    if queue.get("active_item") != "PV-LH-001":
        errors.append("PV-LH-001 must be the active provenance handoff")

    if lock.get("release_state") == "RELEASE_ELIGIBLE":
        required = (
            root / ".provenance/receipts/independent-provenance-review.json",
            root / ".provenance/receipts/outside-project-review-redacted.json",
            root / ".provenance/receipts/release-admission.json",
            root / "sbom/actiongate.spdx.json",
        )
        for path in required:
            if not path.exists():
                errors.append(f"release eligibility missing receipt/artifact: {path.relative_to(root)}")

    license_path = root / "LICENSE"
    if not license_path.exists():
        errors.append("root LICENSE is missing")
    else:
        license_text = license_path.read_text(encoding="utf-8", errors="ignore")
        if "Apache License" not in license_text or "Version 2.0" not in license_text:
            errors.append("root LICENSE is not recognized as Apache-2.0 text")

    return sorted(set(errors))


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


def commit_requires_dco(root: Path, commit: str, source_inventory_nonempty: bool) -> bool:
    output = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit],
        cwd=root,
        text=True,
    )
    paths = [line.strip() for line in output.splitlines() if line.strip()]
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


def check_commits(root: Path, base: str, head: str) -> list[str]:
    errors: list[str] = []
    lock = load_json(root / ".provenance/upstreams.lock.json")
    imports = load_json(root / ".provenance/imported-paths.json")
    source_inventory_nonempty = bool(lock.get("upstreams") or imports.get("mappings"))
    commits = subprocess.check_output(
        ["git", "rev-list", "--reverse", f"{base}..{head}"], cwd=root, text=True
    ).splitlines()
    for commit in commits:
        if not commit_requires_dco(root, commit, source_inventory_nonempty):
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
