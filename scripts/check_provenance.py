#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ID = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
RELATIONSHIPS = {
    "DEPENDENCY_ONLY",
    "DERIVED_PUBLIC_UPSTREAM",
    "VENDOR_IMPORT",
    "CLEAN_ROOM_REIMPLEMENTATION",
}
REQUIRED_FILES = (
    "PROVENANCE.md",
    "CONTRIBUTING.md",
    "docs/provenance/AGENTS.md",
    ".provenance/upstreams.lock.json",
    ".provenance/imported-paths.json",
    ".provenance/release-gate.json",
    ".provenance/local-handoff-queue.json",
    ".provenance/templates/clean-room-session.example.json",
    ".provenance/templates/outside-project-review.example.json",
    "LICENSES/README.md",
    "sbom/actiongate.spdx.json",
    ".github/pull_request_template.md",
    ".github/workflows/provenance-guard.yml",
)
SKIP_DIRS = {".git", ".venv", "node_modules", "build", "DerivedData", "__pycache__"}
LOCAL_PRIVATE_PREFIXES = (
    ".provenance/private/",
    ".provenance/receipts/local/",
    ".actiongate/local/",
    ".actiongate/receipts/local/",
)


class GuardError(ValueError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GuardError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GuardError(f"invalid JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_relpath(value: str) -> bool:
    if not value or value.startswith(("/", "\\")):
        return False
    parts = value.replace("\\", "/").split("/")
    return all(part not in {"", ".", "..", ".git"} for part in parts)


def public_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if rel.startswith(LOCAL_PRIVATE_PREFIXES):
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        yield path


def disclosure_patterns() -> list[tuple[str, re.Pattern[str]]]:
    private_locations = [
        "https://" + "docs." + "google.com" + "/document/d/",
        "https://" + "docs." + "google.com" + "/spreadsheets/d/",
        "https://" + "drive." + "google.com" + "/drive/folders/",
    ]
    patterns: list[tuple[str, re.Pattern[str]]] = [
        ("PRIVATE_DOCUMENT_LOCATOR", re.compile("|".join(re.escape(v) for v in private_locations), re.I)),
        ("PRIVATE_KEY", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
        ("GITHUB_TOKEN", re.compile(r"\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,})\b")),
        ("OPENAI_STYLE_KEY", re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b")),
        ("GOOGLE_API_KEY", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
        ("AWS_ACCESS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ]
    local_patterns_path = Path(".provenance/private-patterns.local.json")
    if local_patterns_path.exists():
        data = load_json(local_patterns_path)
        for index, raw in enumerate(data.get("patterns", [])):
            patterns.append((f"LOCAL_PRIVATE_PATTERN_{index}", re.compile(raw)))
    return patterns


def scan_disclosures(root: Path) -> list[str]:
    errors: list[str] = []
    patterns = disclosure_patterns()
    for path in public_text_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for name, pattern in patterns:
            if pattern.search(text):
                errors.append(f"{name}: {rel}")
    return errors


def validate_upstreams(root: Path, lock: dict[str, Any], imports: dict[str, Any], sbom: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if lock.get("schema") != "actiongate-upstream-lock/v1":
        errors.append("upstream lock schema mismatch")
    if lock.get("repository") != "ed3c/ActionGate":
        errors.append("upstream lock repository mismatch")
    upstreams = lock.get("upstreams")
    if not isinstance(upstreams, list):
        return errors + ["upstreams must be an array"]

    state = lock.get("state")
    if upstreams and state != "UPSTREAMS_ADMITTED":
        errors.append("non-empty upstreams require UPSTREAMS_ADMITTED")
    if not upstreams and state != "NO_DERIVED_UPSTREAM_ADMITTED":
        errors.append("empty upstreams require NO_DERIVED_UPSTREAM_ADMITTED")

    sbom_packages = {
        package.get("SPDXID"): package
        for package in sbom.get("packages", [])
        if isinstance(package, dict) and isinstance(package.get("SPDXID"), str)
    }

    by_id: dict[str, dict[str, Any]] = {}
    for entry in upstreams:
        if not isinstance(entry, dict):
            errors.append("upstream entry must be an object")
            continue
        uid = entry.get("id")
        if not isinstance(uid, str) or not ID.fullmatch(uid):
            errors.append(f"invalid upstream id: {uid!r}")
            continue
        if uid in by_id:
            errors.append(f"duplicate upstream id: {uid}")
            continue
        by_id[uid] = entry
        for key in (
            "name", "repository", "commit", "tree", "relationship",
            "license_spdx", "license_file", "license_sha256", "sbom_spdx_id",
        ):
            if not isinstance(entry.get(key), str) or not entry[key]:
                errors.append(f"{uid}: missing {key}")
        if not HEX40.fullmatch(str(entry.get("commit", ""))):
            errors.append(f"{uid}: commit must be 40 lowercase hex")
        if not HEX40.fullmatch(str(entry.get("tree", ""))):
            errors.append(f"{uid}: tree must be 40 lowercase hex")
        if entry.get("relationship") not in RELATIONSHIPS:
            errors.append(f"{uid}: invalid relationship")
        if not HEX64.fullmatch(str(entry.get("license_sha256", ""))):
            errors.append(f"{uid}: license_sha256 must be 64 lowercase hex")
        repository = str(entry.get("repository", ""))
        if not repository.startswith("https://"):
            errors.append(f"{uid}: repository must be an HTTPS public locator")
        license_file = str(entry.get("license_file", ""))
        if safe_relpath(license_file):
            license_path = root / license_file
            if not license_path.is_file():
                errors.append(f"{uid}: license file missing: {license_file}")
            elif HEX64.fullmatch(str(entry.get("license_sha256", ""))) and sha256_file(license_path) != entry["license_sha256"]:
                errors.append(f"{uid}: license digest mismatch")
        else:
            errors.append(f"{uid}: unsafe license_file")
        spdx_id = entry.get("sbom_spdx_id")
        package = sbom_packages.get(spdx_id)
        if not package:
            errors.append(f"{uid}: SBOM package missing: {spdx_id}")
        elif package.get("versionInfo") != entry.get("commit"):
            errors.append(f"{uid}: SBOM versionInfo must equal upstream commit")

    if imports.get("schema") != "actiongate-imported-paths/v1":
        errors.append("import map schema mismatch")
    mappings = imports.get("mappings")
    if not isinstance(mappings, list):
        return errors + ["mappings must be an array"]
    if mappings and imports.get("state") != "IMPORTED_PATHS_ADMITTED":
        errors.append("non-empty mappings require IMPORTED_PATHS_ADMITTED")
    if not mappings and imports.get("state") != "NO_IMPORTED_PATHS_ADMITTED":
        errors.append("empty mappings require NO_IMPORTED_PATHS_ADMITTED")

    local_paths: set[str] = set()
    mapping_counts: dict[str, int] = {uid: 0 for uid in by_id}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            errors.append("mapping must be an object")
            continue
        uid = mapping.get("upstream_id")
        if uid not in by_id:
            errors.append(f"mapping references unlocked upstream: {uid!r}")
            continue
        upstream_path = mapping.get("upstream_path")
        local_path = mapping.get("local_path")
        source_blob = mapping.get("source_blob")
        if not isinstance(upstream_path, str) or not safe_relpath(upstream_path):
            errors.append(f"{uid}: unsafe upstream_path")
        if not isinstance(local_path, str) or not safe_relpath(local_path):
            errors.append(f"{uid}: unsafe local_path")
        elif local_path in local_paths:
            errors.append(f"duplicate local mapping: {local_path}")
        else:
            local_paths.add(local_path)
        if not isinstance(source_blob, str) or not HEX40.fullmatch(source_blob):
            errors.append(f"{uid}: source_blob must be exact 40-hex Git blob")
        mapping_counts[uid] += 1

    for uid, entry in by_id.items():
        if entry.get("relationship") in {"DERIVED_PUBLIC_UPSTREAM", "VENDOR_IMPORT"} and mapping_counts.get(uid, 0) == 0:
            errors.append(f"{uid}: derived/vendor relationship requires imported-path mapping")
    return errors


def validate_release_gate(gate: dict[str, Any], release_gate: bool) -> list[str]:
    errors: list[str] = []
    if gate.get("schema") != "actiongate-provenance-release-gate/v1":
        errors.append("release gate schema mismatch")
    blockers = gate.get("blockers")
    if not isinstance(blockers, list):
        errors.append("release blockers must be an array")
        blockers = []
    if gate.get("state") == "RELEASE_ELIGIBLE" and blockers:
        errors.append("RELEASE_ELIGIBLE cannot retain blockers")
    if release_gate and (gate.get("state") != "RELEASE_ELIGIBLE" or blockers):
        errors.append("release gate is not admitted")
    return errors


def validate_templates(root: Path) -> list[str]:
    errors: list[str] = []
    clean = load_json(root / ".provenance/templates/clean-room-session.example.json")
    outside = load_json(root / ".provenance/templates/outside-project-review.example.json")
    for key in ("employer_source_accessed", "employer_resource_used", "private_material_included"):
        if clean.get(key) is not None:
            errors.append(f"clean-room template must not self-assert {key}")
    if clean.get("legal_admission") != "HUMAN_ADMIT_REQUIRED":
        errors.append("clean-room template must retain Human legal gate")
    for key in (
        "private_review_completed",
        "employment_agreement_reviewed",
        "employer_resources_used",
        "employer_confidential_material_used",
        "public_upstream_only",
    ):
        if outside.get(key) is not None:
            errors.append(f"outside-project template must not self-assert {key}")
    if outside.get("private_urls_echoed") is not False:
        errors.append("outside-project template must forbid private URL echo")
    return errors


def parse_commit_records(raw: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for chunk in raw.split("\x1e"):
        if not chunk.strip():
            continue
        parts = chunk.strip("\n").split("\x1f", 3)
        if len(parts) != 4:
            raise GuardError("unexpected git log record")
        records.append({"sha": parts[0], "author": parts[1], "email": parts[2], "body": parts[3]})
    return records


def validate_dco_records(records: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"^Signed-off-by:\s*(.+?)\s*<([^>]+)>\s*$", re.I | re.M)
    for record in records:
        matches = pattern.findall(record["body"])
        if not matches:
            errors.append(f"DCO missing: {record['sha']}")
            continue
        author_email = record["email"].lower()
        if not any(email.lower() == author_email for _, email in matches):
            errors.append(f"DCO email does not match author: {record['sha']}")
    return errors


def validate_commit_range(root: Path, commit_range: str) -> list[str]:
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}\.\.[0-9a-fA-F]{7,40}", commit_range):
        return ["unsafe commit range"]
    result = subprocess.run(
        ["git", "-C", str(root), "log", "--format=%H%x1f%an%x1f%ae%x1f%B%x1e", commit_range],
        check=False, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return [f"git log failed: {result.stderr.strip()}"]
    try:
        records = parse_commit_records(result.stdout)
    except GuardError as exc:
        return [str(exc)]
    if not records:
        return ["commit range is empty"]
    return validate_dco_records(records)


def validate_repository(root: Path, release_gate: bool = False) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")
    if errors:
        return errors

    lock = load_json(root / ".provenance/upstreams.lock.json")
    imports = load_json(root / ".provenance/imported-paths.json")
    gate = load_json(root / ".provenance/release-gate.json")
    sbom = load_json(root / "sbom/actiongate.spdx.json")

    errors.extend(validate_upstreams(root, lock, imports, sbom))
    errors.extend(validate_release_gate(gate, release_gate))
    errors.extend(validate_templates(root))
    errors.extend(scan_disclosures(root))

    if sbom.get("spdxVersion") != "SPDX-2.3":
        errors.append("SBOM must be SPDX-2.3")
    if sbom.get("dataLicense") != "CC0-1.0":
        errors.append("SPDX document dataLicense must be CC0-1.0")
    packages = sbom.get("packages")
    if not isinstance(packages, list) or not any(
        isinstance(p, dict) and p.get("SPDXID") == "SPDXRef-Package-ActionGate" for p in packages
    ):
        errors.append("SBOM missing ActionGate package")

    handoff = load_json(root / ".provenance/local-handoff-queue.json")
    if handoff.get("active_item") != "ABSENT":
        errors.append("provenance handoff must not self-activate without Human input")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--commit-range")
    parser.add_argument("--release-gate", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors = validate_repository(root, release_gate=args.release_gate)
    if args.commit_range:
        errors.extend(validate_commit_range(root, args.commit_range))

    if errors:
        print("ActionGate provenance guard: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    lock = load_json(root / ".provenance/upstreams.lock.json")
    gate = load_json(root / ".provenance/release-gate.json")
    print("ActionGate provenance guard: PASS")
    print(f"upstreams={len(lock['upstreams'])} upstream_state={lock['state']}")
    print(f"release_state={gate['state']} (structural PASS is not legal/release admission)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
