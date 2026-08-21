#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("dispatch_checker", ROOT / "check_dispatch.py")
checker = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(checker)

def expect_refusal(label: str, fn, expected_fragment: str) -> None:
    try:
        fn()
    except checker.Refusal:
        print(f"{label}: PASS")
        return
    raise AssertionError(f"{label}: mutation accepted")

def valid_review(registry: dict) -> dict:
    receipt = checker.load(ROOT / "independent-review-receipt.template.json")
    receipt["template"] = False
    receipt["dispatch_pr"] = registry.get("stack", {}).get("dispatch_pr", 0)
    receipt["dispatch_epoch"] = registry.get("dispatch_candidate", {}).get("commit", "0" * 40)
    receipt["reviewer"] = {
        "context_id": "external-review-context-0001",
        "kind": "OTHER_SEPARATE_READ_ONLY_SESSION",
        "separate_context": True,
        "implemented_or_repaired_audited_subjects": False,
        "built_dispatch_packet": False,
        "same_context_as_builder": False,
        "read_only": True,
        "source_mutation_performed": False,
        "private_context_accessed": False,
    }
    for item in receipt["falsifiers"]:
        item["state"] = "PASS"
        item["evidence"] = f"independent evidence for {item['id']}"
    receipt["findings"] = [{
        "id": "SH-EXT-000",
        "severity": "INFO",
        "disposition": "NO_FINDING",
        "summary": "All required falsifiers were independently exercised."
    }]
    receipt["dissent"] = ["Hardware, MCP, legal, merge, release, and production remain outside this review."]
    receipt["verdict"] = "ELIGIBLE_FOR_C01_CONVERGENCE"
    return receipt

def main() -> int:
    registry = checker.load(ROOT / "dispatch-registry.json")
    checker.run()
    cases = []

    data = copy.deepcopy(registry)
    data["workers"][0]["current_head"] = "511b26ad10389e0d0076f463f59f3a9c0e8a1b6e"
    cases.append(("STALE_ISSUE_49_HEAD_REUSED", lambda d=data: checker.check_registry(d), "stale Issue #49 head reused"))

    data = copy.deepcopy(registry)
    data["required_falsifiers"].remove("raw_exponent_rejected")
    cases.append(("PROFILE_CONTROL_OMITTED", lambda d=data: checker.check_registry(d), "falsifier denominator"))

    data = copy.deepcopy(registry)
    data["common_receipt_denominator"]["required"] = 9
    cases.append(("DENOMINATOR_SHRINKAGE", lambda d=data: checker.check_registry(d), "denominator"))

    data = copy.deepcopy(registry)
    data["workers"][1]["lease"] = data["workers"][0]["lease"]
    cases.append(("WORKER_LEASE_OVERLAP", lambda d=data: checker.check_registry(d), "lease overlap"))

    data = copy.deepcopy(registry)
    data["worker_relation"] = "KOTLIN_PARENT_OF_SWIFT"
    cases.append(("FALSE_INTER_WORKER_PARENT", lambda d=data: checker.check_registry(d), "serialization"))

    data = copy.deepcopy(registry)
    data["current_context"]["independent_reviewer_eligible"] = True
    cases.append(("SAME_CONTEXT_PROMOTED_TO_INDEPENDENT", lambda d=data: checker.check_registry(d), "authority"))

    data = copy.deepcopy(registry)
    data["current_context"]["may_emit_c01_admitted"] = True
    cases.append(("DISPATCH_PROMOTED_TO_C01_ADMISSION", lambda d=data: checker.check_registry(d), "authority"))

    data = copy.deepcopy(registry)
    data["private_route"] = "https://docs" + ".google.com/document/d/forbidden"
    cases.append(("PRIVATE_ROUTE_IN_PACKET", lambda d=data: checker.check_registry(d), "private"))

    template = checker.load(ROOT / "independent-review-receipt.template.json")
    template["falsifiers"][0]["state"] = "PASS"
    cases.append(("TEMPLATE_FABRICATES_PASS", lambda d=template: checker.check_template(d, registry), "template"))

    review = valid_review(registry)
    review["reviewer"]["same_context_as_builder"] = True
    cases.append(("BUILDER_LISTED_AS_REVIEWER", lambda d=review: checker.validate_review_receipt(d, registry), "reviewer"))

    review = valid_review(registry)
    review["falsifiers"][0]["state"] = "NOT_EXERCISED"
    cases.append(("ELIGIBLE_WITH_UNEXERCISED_CONTROL", lambda d=review: checker.validate_review_receipt(d, registry), "eligible"))

    review = valid_review(registry)
    review["audited_subjects"]["typescript"]["receipt_blob"] = "0" * 40
    cases.append(("RECEIPT_BLOB_DRIFT", lambda d=review: checker.validate_review_receipt(d, registry), "subjects"))

    review = valid_review(registry)
    review["evidence_ceiling"] = "hardware and MCP security review"
    cases.append(("AUTHORITY_WIDENING", lambda d=review: checker.validate_review_receipt(d, registry), "authority"))

    for label, fn, fragment in cases:
        expect_refusal(label, fn, fragment)

    review = valid_review(registry)
    checker.validate_review_receipt(review, registry)
    print("VALID_INDEPENDENT_REVIEW_FIXTURE: PASS")
    print(f"C01 profile dispatch selftest: PASS {len(cases) + 2}/{len(cases) + 2}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
