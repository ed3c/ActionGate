#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("checker", ROOT / "check_dispatch.py")
checker = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(checker)


def set_path(obj, path, value):
    current = obj
    for part in path[:-1]:
        current = current[part]
    current[path[-1]] = value


def run_case(base, expected, path, value):
    candidate = copy.deepcopy(base)
    set_path(candidate, path, value)
    try:
        checker.check_registry(candidate)
    except checker.DispatchError as exc:
        if str(exc) != expected:
            raise AssertionError(f"{expected}: got {exc}") from exc
        print(f"{expected}: PASS")
        return
    raise AssertionError(f"{expected}: mutation accepted")


def main() -> int:
    registry = checker.load(ROOT / "dispatch-registry.json")
    template = checker.load(ROOT / "independent-review-receipt.template.json")
    checker.check_registry(registry)
    checker.check_template(template)

    private_url = "https://docs" + ".google.com/document/d/forbidden"
    cases = [
        ("STALE_KOTLIN_CURRENT_HEAD", ["workers", 0, "current_head"], "0" * 40),
        ("STALE_SWIFT_CURRENT_TREE", ["workers", 1, "current_tree"], "1" * 40),
        ("STALE_TYPESCRIPT_RECEIPT_BLOB", ["workers", 2, "receipt_blob"], "2" * 40),
        ("WORKER_LEASE_OVERLAP", ["workers", 1, "lease"], registry["workers"][0]["lease"]),
        ("DENOMINATOR_SHRINKAGE", ["workers", 0, "common_denominator", "pass"], 9),
        ("COMMON_DENOMINATOR_SHRINKAGE", ["common_denominator", "negative_required"], 6),
        ("REQUIRED_FALSIFIER_OMITTED", ["required_falsifiers"], registry["required_falsifiers"][:-1]),
        ("BUILDER_LISTED_AS_INDEPENDENT_REVIEWER", ["independent_review", "builder_or_same_context_may_satisfy"], True),
        ("INDEPENDENT_REVIEW_WRITE_WIDENED", ["independent_review", "source_or_pr_mutation_allowed"], True),
        ("INDEPENDENT_PACKET_PROMOTED_TO_C01_ADMISSION", ["convergence", "state"], "C01_ADMITTED"),
        ("AUTOMATIC_K01_START", ["convergence", "automatic_k01_start"], True),
        ("CURRENT_CONTEXT_AUTHORITY_WIDENED", ["current_context", "may_emit_independent_verdict"], True),
        ("REGISTRY_PRIVATE_URL", ["private_context_url"], private_url),
    ]
    for expected, path, value in cases:
        run_case(registry, expected, path, value)

    bad_template = copy.deepcopy(template)
    bad_template["independence"]["same_context"] = False
    try:
        checker.check_template(bad_template)
    except checker.DispatchError as exc:
        if str(exc) != "TEMPLATE_FABRICATES_INDEPENDENCE":
            raise
        print("TEMPLATE_FABRICATES_INDEPENDENCE: PASS")
    else:
        raise AssertionError("TEMPLATE_FABRICATES_INDEPENDENCE: mutation accepted")

    print(f"C01 independent Shadow dispatch selftest: PASS {len(cases)+2}/{len(cases)+2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
