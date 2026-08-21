#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PRIVATE_URL_RE = re.compile(r"https?://(?:docs|drive)\.google\.com", re.I)
SECRET_RE = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)
PLACEHOLDER_RE = re.compile(r"<[A-Z0-9_ -]+>")

EXPECTED_C01 = "b63589e5a16e82fda1a9554227f2ebbb55398c8a"
EXPECTED_EXEC = "9f41038240837ea2dd9dcdb9befd13e6ba81a78e"
EXPECTED_BASE = ("ag/C01-worker-launch-packets", "98c9545c0dd2bbfdabdaf27c8a992822a78b3840", "fd65f2fa9278fe0c0251987939663f42a22ec24b", 41)
EXPECTED_WORKERS = {
    "kotlin": {
        "issue": 18,
        "pr": 34,
        "branch": "ag/C01-kotlin-vectors",
        "current_head": "511b26ad10389e0d0076f463f59f3a9c0e8a1b6e",
        "current_tree": "92d6e5affe027df8c6ea4a03cf0e49b756248ee3",
        "source_candidate": "8d56b1533bc5b9b56fae8b515d7a64b280ababb3",
        "source_tree": "f08ec00d212aecfc04e8ba6db4ecca97ae75971c",
        "receipt_subject": "7cd754840b471844b6215685671b3e8e2829a43a",
        "receipt_tree": "9b2f07b220ee40d9b1b7641fa0a5aca9372252f8",
        "receipt_blob": "6bfa88ca2f3e2a928c8785f2fb87fdcaee5e6c67",
        "shadow_receipt_blob": "17ede5d60b45f8bdc38b6ffb1917bb5ea1c70c8a",
        "lease": "contracts/impl/kotlin/**",
    },
    "swift": {
        "issue": 19,
        "pr": 35,
        "branch": "ag/C01-swift-vectors",
        "current_head": "48bc9cf00105f40d5444542ddcdad85106f3c1d5",
        "current_tree": "91458fe771874c3798edeedcaa2a3bde777bd14c",
        "source_candidate": "d4abae30f9822667b14912a3964a0f21bff04772",
        "source_tree": "6159f45a8be6a774f69ec955af1900b4d54950b1",
        "receipt_subject": "4d38cf1451d95f83fb9251d707fe9ab173e2ca45",
        "receipt_tree": "31f0efacb44e92eb6c8fabf8facdf9facfc7eabd",
        "receipt_blob": "38d762d2ae306b30e607f2de71794a2609debfca",
        "shadow_receipt_blob": "87346e102a1be351c0a95a5628ccda47d3cb829e",
        "lease": "contracts/impl/swift/**",
    },
    "typescript": {
        "issue": 20,
        "pr": 36,
        "branch": "ag/C01-typescript-vectors",
        "current_head": "6a99c61150d00be56c7eddf70eb9e3f423cfb7fa",
        "current_tree": "5c392c2e72bef44732617c13fd3d698fc4955594",
        "source_candidate": "3cca770448d37610e494bb4147d03fe93da8b0b9",
        "source_tree": "2e51037be1214c52ce0961d5b6a972884f2d1284",
        "receipt_subject": "f3c0f57e2e32adbfc0754466322f18bbd724a71e",
        "receipt_tree": "eae7ddab948aad05e1576deb6984a614525e9311",
        "receipt_blob": "62e4a49035a1522bf23b60d858dfd38cba98bf8c",
        "shadow_receipt_blob": "dd946070466ea2287700d549c92f97756685da89",
        "lease": "contracts/impl/typescript/**",
    },
}
COMMON_IDS = {
    "three_frozen_hashes",
    "ordering",
    "float_rejected",
    "unsafe_integer_rejected",
    "invalid_key_rejected",
    "unsupported_value_rejected",
    "duplicate_key_control",
    "unicode_no_normalization",
}
REQUIRED_FALSIFIERS = {
    "three_frozen_hashes",
    "ordering",
    "float_rejected",
    "unsafe_integer_rejected",
    "invalid_key_rejected",
    "unsupported_value_rejected",
    "duplicate_key_control",
    "unicode_no_normalization",
    "exact_ascii_domain_trailing_nul",
    "non_ascii_domain_rejected",
    "missing_nul_rejected",
    "escaped_native_duplicate_equivalence",
    "surrogate_pair_acceptance",
    "lone_surrogate_rejection",
    "leading_zero_rejection",
    "recursive_container_rejection",
    "mutable_foundation_container_rejection",
    "sha256_known_answer_vectors",
    "sparse_array_rejection",
    "accessor_rejection",
    "symbol_key_rejection",
    "extra_array_property_rejection",
    "unsupported_prototype_rejection",
}
READY_STATE = "C01_INDEPENDENT_SHADOW_DISPATCH_READY_FOR_EXTERNAL_REVIEW"
CANDIDATE_STATE = "C01_INDEPENDENT_SHADOW_DISPATCH_CANDIDATE"


class DispatchError(ValueError):
    pass


def fail(code: str) -> None:
    raise DispatchError(code)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(value: Any, code: str) -> str:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        fail(code)
    return value


def reject_public_leaks(value: Any, code: str) -> None:
    raw = json.dumps(value, ensure_ascii=False)
    if PRIVATE_URL_RE.search(raw):
        fail(f"{code}_PRIVATE_URL")
    if SECRET_RE.search(raw):
        fail(f"{code}_SECRET")
    if PLACEHOLDER_RE.search(raw):
        fail(f"{code}_PLACEHOLDER")


def check_registry(data: dict[str, Any]) -> None:
    if data.get("schema") != "actiongate-c01-independent-shadow-dispatch/v1":
        fail("BAD_SCHEMA")
    if data.get("repository") != "ed3c/ActionGate" or data.get("issue") != 58:
        fail("BAD_IDENTITY")
    if data.get("parent_shadow_issue") != 26 or data.get("convergence_issue") != 24:
        fail("BAD_ROUTE")
    state = data.get("state")
    if state not in {CANDIDATE_STATE, READY_STATE}:
        fail("BAD_PHASE_STATE")

    base = data.get("base", {})
    observed_base = (base.get("branch"), base.get("commit"), base.get("tree"), base.get("pr"))
    if observed_base != EXPECTED_BASE:
        fail("STALE_BASE")
    if base.get("relationship") != "TRUE_CHILD_CONSUMES_LAUNCH_PACKET_CONTRACT":
        fail("FALSE_STACK_RELATION")
    if data.get("dispatch_branch") != "ag/C01-independent-shadow-dispatch":
        fail("BAD_DISPATCH_BRANCH")
    if data.get("contract", {}).get("sha") != EXPECTED_C01:
        fail("STALE_C01")
    if data.get("common_evidence", {}).get("sha") != EXPECTED_EXEC:
        fail("STALE_COMMON_EVIDENCE")
    if data.get("common_evidence", {}).get("access_rule") != "EXACT_READ_ONLY_FETCH_NO_CHERRY_PICK":
        fail("COMMON_EVIDENCE_AUTHORITY_WIDENED")
    if data.get("worker_relation") != "PATH_DISJOINT_SIBLINGS_NO_INTER_WORKER_GIT_PARENT":
        fail("FALSE_INTER_WORKER_PARENT")

    seen_leases: set[str] = set()
    workers = data.get("workers")
    if not isinstance(workers, list) or len(workers) != 3:
        fail("BAD_WORKER_COUNT")
    actual_languages = {w.get("language") for w in workers}
    if actual_languages != set(EXPECTED_WORKERS):
        fail("BAD_LANGUAGE_SET")

    for worker in workers:
        language = worker["language"]
        expected = EXPECTED_WORKERS[language]
        lease_value = worker.get("lease")
        if lease_value in seen_leases:
            fail("WORKER_LEASE_OVERLAP")
        seen_leases.add(lease_value)
        for key, value in expected.items():
            if worker.get(key) != value:
                fail(f"STALE_{language.upper()}_{key.upper()}")
        for key in (
            "current_head",
            "current_tree",
            "source_candidate",
            "source_tree",
            "receipt_subject",
            "receipt_tree",
            "receipt_blob",
            "shadow_receipt_blob",
        ):
            sha(worker.get(key), f"BAD_{language.upper()}_{key.upper()}")
        if worker["receipt_subject"] in {worker["current_head"], worker["source_candidate"]}:
            fail("RECEIPT_NOT_SUCCESSOR_BOUND")
        if worker.get("receipt_relation") != "SUCCESSOR_RECEIPT_BINDS_PRECEDING_METADATA_CANDIDATE":
            fail("BAD_RECEIPT_RELATION")
        denominator = worker.get("common_denominator", {})
        if denominator != {"positive": 3, "negative": 7, "pass": 10, "fail": 0}:
            fail("DENOMINATOR_SHRINKAGE")
        if worker.get("implementation_state") != "SHADOW_HARDENED_LOCAL_DETERMINISTIC_PASS":
            fail("FALSE_IMPLEMENTATION_STATE")
        same_context = worker.get("same_context_shadow", {})
        if same_context.get("state") != "PASS" or same_context.get("independence_claimed") is not False:
            fail("SAME_CONTEXT_PROMOTED_TO_INDEPENDENT")
        if worker.get("independent_shadow_state") != "NOT_EXERCISED":
            fail("FALSE_INDEPENDENT_STATE")

    common = data.get("common_denominator", {})
    if common.get("positive_required") != 3 or common.get("negative_required") != 7:
        fail("COMMON_DENOMINATOR_SHRINKAGE")
    if common.get("total_required") != 10:
        fail("COMMON_DENOMINATOR_SHRINKAGE")
    if common.get("required_states") != {"pass": 10, "fail": 0, "not_exercised": 0, "not_representable": 0}:
        fail("COMMON_DENOMINATOR_STATE_DRIFT")
    if set(common.get("ids", [])) != COMMON_IDS:
        fail("COMMON_DENOMINATOR_IDS_DRIFT")
    falsifiers = data.get("required_falsifiers")
    if not isinstance(falsifiers, list) or len(falsifiers) != len(set(falsifiers)):
        fail("DUPLICATE_OR_BAD_FALSIFIER_SET")
    if set(falsifiers) != REQUIRED_FALSIFIERS:
        fail("REQUIRED_FALSIFIER_OMITTED")

    review = data.get("independent_review", {})
    if review.get("issue") != 26:
        fail("BAD_INDEPENDENT_ROUTE")
    if review.get("observer_rule") != "SEPARATE_READ_ONLY_CONTEXT_DID_NOT_IMPLEMENT_OR_REPAIR":
        fail("INDEPENDENCE_RULE_WIDENED")
    if review.get("builder_or_same_context_may_satisfy") is not False:
        fail("BUILDER_LISTED_AS_INDEPENDENT_REVIEWER")
    if review.get("source_or_pr_mutation_allowed") is not False:
        fail("INDEPENDENT_REVIEW_WRITE_WIDENED")
    if review.get("allowed_verdicts") != ["ELIGIBLE_FOR_C01_CONVERGENCE", "HOLD", "REJECT"]:
        fail("BAD_INDEPENDENT_VERDICTS")
    expected_review_state = (
        "READY_FOR_EXTERNAL_INDEPENDENT_SESSION"
        if state == READY_STATE
        else "BLOCKED_BY_EXACT_HEAD_HOSTED_DISPATCH_CHECK"
    )
    if review.get("state") != expected_review_state:
        fail("BAD_INDEPENDENT_PHASE_STATE")

    convergence = data.get("convergence", {})
    if convergence.get("issue") != 24 or convergence.get("sole_semantic_owner") is not True:
        fail("CONVERGENCE_OWNER_WIDENED")
    if convergence.get("state") != "BLOCKED_BY_INDEPENDENT_SHADOW_RECEIPT":
        fail("INDEPENDENT_PACKET_PROMOTED_TO_C01_ADMISSION")
    if convergence.get("allowed_verdicts") != ["C01_ADMITTED", "HOLD", "REJECT"]:
        fail("BAD_CONVERGENCE_VERDICTS")
    if convergence.get("automatic_k01_start") is not False:
        fail("AUTOMATIC_K01_START")

    current = data.get("current_context", {})
    if current.get("may_emit_independent_verdict") is not False or current.get("independence_claimed") is not False:
        fail("CURRENT_CONTEXT_AUTHORITY_WIDENED")

    queue = data.get("local_handoff_queue", {})
    active = [item for item in queue.get("items", []) if item.get("state") == "ACTIVE"]
    if len(active) != 1 or active[0].get("id") != queue.get("active_item"):
        fail("QUEUE_ACTIVE_CARDINALITY")
    expected_active = "C01-SHADOW-002" if state == READY_STATE else "C01-DISPATCH-CHECK-001"
    if queue.get("active_item") != expected_active:
        fail("WRONG_ACTIVE_ITEM")

    for operation in (
        "independent reviewer selection",
        "semantic conflict resolution",
        "merge",
        "release",
        "security/legal acceptance",
        "production",
    ):
        if operation not in data.get("human_owned", []):
            fail("HUMAN_AUTHORITY_MISSING")

    reject_public_leaks(data, "REGISTRY")


def check_template(data: dict[str, Any]) -> None:
    if data.get("schema") != "actiongate-c01-independent-review-receipt-template/v1":
        fail("BAD_TEMPLATE_SCHEMA")
    if data.get("template") is not True or data.get("repository") != "ed3c/ActionGate" or data.get("issue") != 26:
        fail("BAD_TEMPLATE_IDENTITY")
    subject = data.get("audit_subject", {})
    if subject.get("contract_sha") != EXPECTED_C01 or subject.get("common_evidence_sha") != EXPECTED_EXEC:
        fail("STALE_TEMPLATE_SUBJECT")
    if subject.get("dispatch_implementation_sha") != "HUMAN_INPUT_REQUIRED":
        fail("TEMPLATE_FALSE_DISPATCH_BINDING")
    independence = data.get("independence", {})
    required_human = {
        "same_context",
        "implemented_or_repaired_audited_subject",
        "read_only",
        "source_or_pr_mutation",
    }
    if set(independence) != required_human or any(value != "HUMAN_INPUT_REQUIRED" for value in independence.values()):
        fail("TEMPLATE_FABRICATES_INDEPENDENCE")
    if data.get("verdict") != "HUMAN_INPUT_REQUIRED":
        fail("TEMPLATE_FABRICATES_VERDICT")
    if set(data.get("checks", {}).get("required_falsifiers", [])) != REQUIRED_FALSIFIERS:
        fail("TEMPLATE_FALSIFIER_DRIFT")
    reject_public_leaks(data, "TEMPLATE")


def check_review_receipt(data: dict[str, Any], registry: dict[str, Any]) -> None:
    if data.get("schema") != "actiongate-c01-independent-review-receipt/v1":
        fail("BAD_REVIEW_RECEIPT_SCHEMA")
    if data.get("repository") != "ed3c/ActionGate" or data.get("issue") != 26:
        fail("BAD_REVIEW_RECEIPT_IDENTITY")
    subject = data.get("audit_subject", {})
    if subject.get("contract_sha") != EXPECTED_C01 or subject.get("common_evidence_sha") != EXPECTED_EXEC:
        fail("REVIEW_STALE_FOUNDATION")
    sha(subject.get("dispatch_implementation_sha"), "BAD_REVIEW_DISPATCH_SHA")

    expected_workers = {w["language"]: w for w in registry["workers"]}
    actual_workers = subject.get("workers")
    if not isinstance(actual_workers, list) or {w.get("language") for w in actual_workers} != set(expected_workers):
        fail("REVIEW_BAD_WORKER_SET")
    for actual in actual_workers:
        expected = expected_workers[actual["language"]]
        for key in ("current_head", "current_tree", "receipt_subject", "receipt_tree", "receipt_blob", "shadow_receipt_blob"):
            if actual.get(key) != expected.get(key):
                fail(f"REVIEW_STALE_{actual['language'].upper()}_{key.upper()}")

    reviewer = data.get("reviewer", {})
    if reviewer.get("kind") != "INDEPENDENT_READ_ONLY_SHADOW":
        fail("REVIEWER_KIND_WIDENED")
    context_id = reviewer.get("context_id")
    if not isinstance(context_id, str) or len(context_id) < 8 or context_id == "HUMAN_INPUT_REQUIRED":
        fail("REVIEWER_CONTEXT_MISSING")

    independence = data.get("independence", {})
    if independence != {
        "same_context": False,
        "implemented_or_repaired_audited_subject": False,
        "read_only": True,
        "source_or_pr_mutation": False,
    }:
        fail("REVIEW_INDEPENDENCE_NOT_PROVEN")

    checks = data.get("checks", {})
    if set(checks.get("required_falsifiers", [])) != REQUIRED_FALSIFIERS:
        fail("REVIEW_FALSIFIER_DENOMINATOR_SHRUNK")
    passed = set(checks.get("passed", []))
    failed = set(checks.get("failed", []))
    not_exercised = set(checks.get("not_exercised", []))
    if (passed | failed | not_exercised) != REQUIRED_FALSIFIERS:
        fail("REVIEW_FALSIFIER_ACCOUNTING_INCOMPLETE")
    if (passed & failed) or (passed & not_exercised) or (failed & not_exercised):
        fail("REVIEW_FALSIFIER_ACCOUNTING_OVERLAP")

    verdict = data.get("verdict")
    if verdict not in {"ELIGIBLE_FOR_C01_CONVERGENCE", "HOLD", "REJECT"}:
        fail("BAD_REVIEW_VERDICT")
    if verdict == "ELIGIBLE_FOR_C01_CONVERGENCE" and (failed or not_exercised):
        fail("ELIGIBLE_WITH_UNCLOSED_FALSIFIER")
    findings = data.get("findings")
    if not isinstance(findings, list):
        fail("REVIEW_FINDINGS_MISSING")
    if verdict in {"HOLD", "REJECT"} and not findings:
        fail("BLOCKING_VERDICT_WITHOUT_FINDING")
    if data.get("evidence_ceiling") != "independent read-only C01 contract/language review only":
        fail("REVIEW_EVIDENCE_CEILING_WIDENED")
    reject_public_leaks(data, "REVIEW_RECEIPT")


def check_dispatch_receipt(data: dict[str, Any]) -> None:
    if data.get("schema") != "actiongate-c01-shadow-dispatch-receipt/v1":
        fail("BAD_DISPATCH_RECEIPT_SCHEMA")
    if data.get("repository") != "ed3c/ActionGate" or data.get("issue") != 58:
        fail("BAD_DISPATCH_RECEIPT_IDENTITY")
    implementation = data.get("implementation_candidate", {})
    sha(implementation.get("commit"), "BAD_IMPLEMENTATION_COMMIT")
    sha(implementation.get("tree"), "BAD_IMPLEMENTATION_TREE")
    workflow = data.get("hosted_workflow", {})
    if workflow.get("conclusion") != "success":
        fail("HOSTED_WORKFLOW_NOT_GREEN")
    if not isinstance(workflow.get("run_id"), int) or not isinstance(workflow.get("job_id"), int):
        fail("HOSTED_WORKFLOW_ID_MISSING")
    expected_steps = {"checkout", "structural_dispatch_check", "mutation_selftest"}
    if set(workflow.get("passed_steps", [])) != expected_steps:
        fail("HOSTED_WORKFLOW_DENOMINATOR_DRIFT")
    if data.get("state") != READY_STATE:
        fail("DISPATCH_RECEIPT_FALSE_STATE")
    shadow = data.get("shadow_monitor", {})
    if shadow.get("observer_kind") != "SAME_CONTEXT_READ_ONLY_SHADOW" or shadow.get("independence_claimed") is not False:
        fail("DISPATCH_RECEIPT_FALSE_INDEPENDENCE")
    reject_public_leaks(data, "DISPATCH_RECEIPT")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=ROOT / "dispatch-registry.json")
    parser.add_argument("--template", type=Path, default=ROOT / "independent-review-receipt.template.json")
    parser.add_argument("--review-receipt", type=Path)
    args = parser.parse_args()
    try:
        registry = load(args.registry)
        check_registry(registry)
        check_template(load(args.template))
        if registry["state"] == READY_STATE:
            receipt_path = ROOT / "DISPATCH_RECEIPT.json"
            if not receipt_path.exists():
                fail("READY_WITHOUT_DISPATCH_RECEIPT")
            check_dispatch_receipt(load(receipt_path))
        if args.review_receipt:
            check_review_receipt(load(args.review_receipt), registry)
    except (DispatchError, json.JSONDecodeError, OSError, KeyError, TypeError) as exc:
        print(f"C01 independent Shadow dispatch check: FAIL: {exc}")
        return 1
    print("C01 independent Shadow dispatch check: PASS")
    print(f"Dispatch state: {registry['state']}")
    print("Independent Shadow Issue #26: NOT_EXECUTED_BY_THIS_CONTEXT")
    print("C01 convergence Issue #24: BLOCKED_BY_INDEPENDENT_SHADOW_RECEIPT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
