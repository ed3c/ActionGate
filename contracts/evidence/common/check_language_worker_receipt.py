#!/usr/bin/env python3
"""Semantic gate for ActionGate C01 language-worker receipts.

Uses only the Python standard library. JSON-Schema shape validation is a
separate lane; this checker owns exact identities, denominator integrity,
lease boundaries, forbidden commands/data and evidence-state consistency.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

BASE = "b63589e5a16e82fda1a9554227f2ebbb55398c8a"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED = {
    "kotlin": (18, "ag/C01-kotlin-vectors", "contracts/impl/kotlin/"),
    "swift": (19, "ag/C01-swift-vectors", "contracts/impl/swift/"),
    "typescript": (20, "ag/C01-typescript-vectors", "contracts/impl/typescript/"),
}
POSITIVE_IDS = {
    "arguments_hash",
    "action_digest",
    "authorization_signing_input_sha256",
}
NEGATIVE_IDS = {
    "ordering",
    "float_rejected",
    "unsafe_integer_rejected",
    "invalid_key_rejected",
    "unsupported_value_rejected",
    "duplicate_key_control",
    "unicode_no_normalization",
}
RESULT_STATES = {
    "PASS", "FAIL", "NOT_EXERCISED", "NOT_REPRESENTABLE_WITH_REASON"
}
FORBIDDEN_FRAGMENTS = (
    "docs" + ".google.com", "drive" + ".google.com", "-----" + "BEGIN",
    "ghp" + "_", "github" + "_pat_", "Bearer" + " ", "AI" + "za",
    "PRIVATE_CONTEXT", "employer-internal",
)
FORBIDDEN_ARGV = {
    ("curl",), ("wget",), ("npm", "install"), ("npx",),
    ("brew", "install"), ("apt", "install"), ("apt-get", "install"),
}


class Refusal(ValueError):
    pass


def walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from walk_strings(item)


def result_map(items: list[dict[str, Any]], required: set[str], label: str):
    seen: dict[str, str] = {}
    for item in items:
        rid = item.get("id")
        state = item.get("state")
        if not isinstance(rid, str) or rid in seen:
            raise Refusal(f"{label}: duplicate or invalid result id {rid!r}")
        if state not in RESULT_STATES:
            raise Refusal(f"{label}:{rid}: invalid state {state!r}")
        if state == "NOT_REPRESENTABLE_WITH_REASON" and not item.get("reason"):
            raise Refusal(f"{label}:{rid}: reason required")
        seen[rid] = state
    if set(seen) != required:
        raise Refusal(
            f"{label}: denominator ids differ; missing={sorted(required-set(seen))} "
            f"extra={sorted(set(seen)-required)}"
        )
    return seen


def check(path: Path, fixture_mode: bool = False) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "actiongate-c01-language-worker-receipt/v1":
        raise Refusal("schema identity mismatch")
    if data.get("repository") != "ed3c/ActionGate":
        raise Refusal("repository mismatch")
    kind = data.get("evidence_kind")
    if kind == "FIXTURE" and not fixture_mode:
        raise Refusal("fixture receipt requires --fixture-mode")
    if kind not in {"LIVE", "FIXTURE"}:
        raise Refusal("invalid evidence_kind")
    if data.get("base_sha") != BASE or data.get("rollback") != BASE:
        raise Refusal("base/rollback mismatch")

    language = data.get("language")
    if language not in EXPECTED:
        raise Refusal("unknown language")
    issue, branch, prefix = EXPECTED[language]
    if data.get("issue") != issue or data.get("branch") != branch:
        raise Refusal("language/issue/branch mismatch")
    for key in ("head_sha", "tree_sha"):
        if not isinstance(data.get(key), str) or not SHA40.fullmatch(data[key]):
            raise Refusal(f"{key} is not a 40-hex subject")

    lease_paths = data.get("lease", {}).get("paths", [])
    if not lease_paths or any(not p.startswith(prefix) for p in lease_paths):
        raise Refusal("lease escapes language prefix")
    changed = data.get("changed_paths", [])
    if any(not p.startswith(prefix) for p in changed):
        raise Refusal("changed path escapes language prefix")

    runtime = data.get("runtime", {})
    if runtime.get("state") not in {"PASS", "ABSENT", "BLOCKED_ABSENT_EXECUTABLE"}:
        raise Refusal("runtime state invalid")
    if runtime.get("transferable") is not False:
        raise Refusal("runtime capability must not be transferable")
    for command in runtime.get("commands", []):
        argv = command.get("argv")
        if not isinstance(argv, list) or not argv:
            raise Refusal("command argv missing")
        lower = tuple(str(x).lower() for x in argv)
        for blocked in FORBIDDEN_ARGV:
            if lower[:len(blocked)] == blocked:
                raise Refusal(f"forbidden installation/download command: {argv}")

    digests = data.get("contract_digests", {})
    for key in ("profile_sha256", "schema_sha256", "vectors_sha256"):
        if not isinstance(digests.get(key), str) or not SHA64.fullmatch(digests[key]):
            raise Refusal(f"invalid contract digest {key}")

    pos = result_map(data.get("positive_results", []), POSITIVE_IDS, "positive")
    neg = result_map(data.get("negative_results", []), NEGATIVE_IDS, "negative")
    all_states = list(pos.values()) + list(neg.values())
    counts = {
        "pass": all_states.count("PASS"),
        "fail": all_states.count("FAIL"),
        "not_exercised": all_states.count("NOT_EXERCISED"),
        "not_representable": all_states.count("NOT_REPRESENTABLE_WITH_REASON"),
    }
    denominator = data.get("denominator", {})
    if denominator.get("required") != 10 or sum(counts.values()) != 10:
        raise Refusal("required denominator must remain 10")
    for key, value in counts.items():
        if denominator.get(key) != value:
            raise Refusal(f"denominator count mismatch for {key}")

    evidence_state = data.get("evidence_state")
    blockers = data.get("blockers", [])
    if evidence_state == "PASS":
        if runtime.get("state") != "PASS":
            raise Refusal("PASS requires runtime PASS")
        if any(state != "PASS" for state in pos.values()):
            raise Refusal("PASS requires all positive results PASS")
        if any(state == "FAIL" or state == "NOT_EXERCISED" for state in neg.values()):
            raise Refusal("PASS cannot retain failed/unexercised negative controls")
        if blockers:
            raise Refusal("PASS cannot retain blockers")
        if data.get("clean_room_state") != "CLEAN_ROOM_PRECHECK_PASS":
            raise Refusal("PASS requires clean-room precheck")
    elif evidence_state == "NOT_EXERCISED" and counts["pass"]:
        raise Refusal("NOT_EXERCISED cannot carry PASS results")

    shadow = data.get("shadow", {})
    if shadow.get("independence_claimed") is not False:
        raise Refusal("Worker receipt may not claim independent Shadow")
    if data.get("evidence_lane") != "local-deterministic canonicalization only":
        raise Refusal("evidence lane widened")

    for text in walk_strings(data):
        if any(fragment.lower() in text.lower() for fragment in FORBIDDEN_FRAGMENTS):
            raise Refusal("private/secret-shaped content detected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--fixture-mode", action="store_true")
    args = parser.parse_args()
    try:
        check(args.receipt, fixture_mode=args.fixture_mode)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID_INPUT: {exc}", file=sys.stderr)
        return 64
    except Refusal as exc:
        print(f"RECEIPT_REFUSED: {exc}", file=sys.stderr)
        return 2
    print("LANGUAGE_WORKER_RECEIPT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
