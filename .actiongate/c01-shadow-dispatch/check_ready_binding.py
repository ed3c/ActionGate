#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("base_checker", ROOT / "check_dispatch.py")
base_checker = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(base_checker)

READY_STATE = "C01_INDEPENDENT_SHADOW_DISPATCH_READY_FOR_EXTERNAL_REVIEW"
EXPECTED_IMPLEMENTATION = {
    "pr": 59,
    "commit": "f2acfc2e67276aaa0509bc93ae7a4cd0f24e1e59",
    "tree": "d08d865e63058cda3a2ff4a9842da69821261082",
    "receipt_relation": "SUCCESSOR_DISPATCH_RECEIPT_BINDS_IMPLEMENTATION_CANDIDATE",
}
EXPECTED_WORKFLOW = {
    "run_id": 32457982037,
    "job_id": 96698905081,
    "conclusion": "success",
    "passed_steps": ["checkout", "structural_dispatch_check", "mutation_selftest"],
}


class ReadyBindingError(ValueError):
    pass


def fail(code: str) -> None:
    raise ReadyBindingError(code)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_ready(
    registry: dict[str, Any],
    receipt: dict[str, Any],
    phase: dict[str, Any],
) -> None:
    if registry.get("state") != READY_STATE:
        fail("REGISTRY_NOT_READY")
    if registry.get("dispatch_implementation") != EXPECTED_IMPLEMENTATION:
        fail("STALE_DISPATCH_IMPLEMENTATION")
    review = registry.get("independent_review", {})
    if review.get("state") != "READY_FOR_EXTERNAL_INDEPENDENT_SESSION":
        fail("INDEPENDENT_REVIEW_NOT_READY")
    queue = registry.get("local_handoff_queue", {})
    if queue.get("active_item") != "C01-SHADOW-002":
        fail("WRONG_READY_ACTIVE_ITEM")
    by_id = {item.get("id"): item for item in queue.get("items", [])}
    if by_id.get("C01-DISPATCH-CHECK-001", {}).get("state") != "CLOSED":
        fail("DISPATCH_CHECK_NOT_CLOSED")
    if by_id.get("C01-SHADOW-002", {}).get("state") != "ACTIVE":
        fail("SHADOW_ITEM_NOT_ACTIVE")
    if by_id.get("C01-CONVERGENCE-003", {}).get("state") != "BLOCKED_BY_INDEPENDENT_RECEIPT":
        fail("CONVERGENCE_NOT_BLOCKED")

    if receipt.get("schema") != "actiongate-c01-shadow-dispatch-receipt/v1":
        fail("BAD_RECEIPT_SCHEMA")
    if receipt.get("repository") != "ed3c/ActionGate" or receipt.get("issue") != 58 or receipt.get("pr") != 59:
        fail("BAD_RECEIPT_IDENTITY")
    if receipt.get("implementation_candidate") != {
        "commit": EXPECTED_IMPLEMENTATION["commit"],
        "tree": EXPECTED_IMPLEMENTATION["tree"],
    }:
        fail("RECEIPT_STALE_IMPLEMENTATION")
    if receipt.get("hosted_workflow") != EXPECTED_WORKFLOW:
        fail("RECEIPT_WORKFLOW_DRIFT")
    if receipt.get("state") != READY_STATE:
        fail("RECEIPT_FALSE_STATE")
    shadow = receipt.get("shadow_monitor", {})
    if shadow != {
        "observer_kind": "SAME_CONTEXT_READ_ONLY_SHADOW",
        "independence_claimed": False,
    }:
        fail("RECEIPT_FALSE_INDEPENDENCE")
    if receipt.get("evidence_ceiling") != "exact-head hosted dispatch preparation only":
        fail("RECEIPT_EVIDENCE_CEILING_WIDENED")

    if phase.get("state") != READY_STATE or phase.get("draft_pr") != 59:
        fail("PHASE_STATE_DRIFT")
    if phase.get("implementation_candidate") != receipt.get("implementation_candidate"):
        fail("PHASE_IMPLEMENTATION_DRIFT")
    hosted = phase.get("verification", {}).get("exact_head_hosted_workflow")
    if hosted != {
        "run_id": EXPECTED_WORKFLOW["run_id"],
        "job_id": EXPECTED_WORKFLOW["job_id"],
        "conclusion": "success",
        "passed_steps": EXPECTED_WORKFLOW["passed_steps"],
    }:
        fail("PHASE_WORKFLOW_DRIFT")
    if phase.get("verification", {}).get("successor_dispatch_receipt") != "PASS":
        fail("PHASE_RECEIPT_NOT_PASS")

    base_checker.reject_public_leaks(
        {"registry": registry, "receipt": receipt, "phase": phase},
        "READY_BINDING",
    )


def check_review_receipt(path: Path, registry: dict[str, Any]) -> None:
    review = load(path)
    base_checker.check_review_receipt(review, registry)
    subject = review.get("audit_subject", {})
    if subject.get("dispatch_implementation_sha") != EXPECTED_IMPLEMENTATION["commit"]:
        fail("REVIEW_STALE_DISPATCH_IMPLEMENTATION")


def expect_error(code: str, func) -> None:
    try:
        func()
    except ReadyBindingError as exc:
        if str(exc) != code:
            raise AssertionError(f"{code}: got {exc}") from exc
        print(f"{code}: PASS")
        return
    raise AssertionError(f"{code}: mutation accepted")


def selftest(registry: dict[str, Any], receipt: dict[str, Any], phase: dict[str, Any]) -> None:
    cases = []

    bad_registry = copy.deepcopy(registry)
    bad_registry["dispatch_implementation"]["commit"] = "0" * 40
    cases.append((
        "STALE_DISPATCH_IMPLEMENTATION",
        lambda bad_registry=bad_registry: check_ready(bad_registry, receipt, phase),
    ))

    bad_receipt = copy.deepcopy(receipt)
    bad_receipt["implementation_candidate"]["tree"] = "1" * 40
    cases.append((
        "RECEIPT_STALE_IMPLEMENTATION",
        lambda bad_receipt=bad_receipt: check_ready(registry, bad_receipt, phase),
    ))

    bad_receipt = copy.deepcopy(receipt)
    bad_receipt["hosted_workflow"]["run_id"] += 1
    cases.append((
        "RECEIPT_WORKFLOW_DRIFT",
        lambda bad_receipt=bad_receipt: check_ready(registry, bad_receipt, phase),
    ))

    bad_receipt = copy.deepcopy(receipt)
    bad_receipt["shadow_monitor"]["independence_claimed"] = True
    cases.append((
        "RECEIPT_FALSE_INDEPENDENCE",
        lambda bad_receipt=bad_receipt: check_ready(registry, bad_receipt, phase),
    ))

    bad_phase = copy.deepcopy(phase)
    bad_phase["verification"]["successor_dispatch_receipt"] = "PENDING"
    cases.append((
        "PHASE_RECEIPT_NOT_PASS",
        lambda bad_phase=bad_phase: check_ready(registry, receipt, bad_phase),
    ))

    bad_registry = copy.deepcopy(registry)
    bad_registry["local_handoff_queue"]["active_item"] = "C01-DISPATCH-CHECK-001"
    cases.append((
        "WRONG_READY_ACTIVE_ITEM",
        lambda bad_registry=bad_registry: check_ready(bad_registry, receipt, phase),
    ))

    for code, func in cases:
        expect_error(code, func)

    print(f"C01 ready binding selftest: PASS {len(cases)}/{len(cases)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-receipt", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    try:
        registry = load(ROOT / "dispatch-registry.json")
        receipt = load(ROOT / "DISPATCH_RECEIPT.json")
        phase = load(ROOT / "phase-status.json")
        check_ready(registry, receipt, phase)
        if args.review_receipt:
            check_review_receipt(args.review_receipt, registry)
        if args.selftest:
            selftest(registry, receipt, phase)
    except (
        ReadyBindingError,
        base_checker.DispatchError,
        json.JSONDecodeError,
        OSError,
        KeyError,
        TypeError,
    ) as exc:
        print(f"C01 exact ready binding check: FAIL: {exc}")
        return 1
    print("C01 exact ready binding check: PASS")
    print(f"implementation={EXPECTED_IMPLEMENTATION['commit']}")
    print(f"workflow_run={EXPECTED_WORKFLOW['run_id']} job={EXPECTED_WORKFLOW['job_id']}")
    print("Independent Shadow Issue #26: READY_FOR_EXTERNAL_SESSION / NOT_EXECUTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
