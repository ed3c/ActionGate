#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "DISPATCH_RECEIPT.json"
RECEIPT_PATH = ".actiongate/c01-shadow-dispatch/profile-v2/DISPATCH_RECEIPT.json"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def fail(message: str) -> None:
    raise ValueError(message)


def checked_out_subject() -> tuple[str, str]:
    """Return (checkout commit, branch-head subject).

    GitHub pull_request workflows check out a synthetic merge commit. In that
    case parent 2 is the exact PR head; push/manual workflows use HEAD itself.
    """
    checkout = git("rev-parse", "HEAD")
    parts = git("rev-list", "--parents", "-n", "1", checkout).split()
    parents = parts[1:]
    if len(parents) == 2:
        return checkout, parents[1]
    return checkout, checkout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-receipt", type=Path)
    args = parser.parse_args()

    if not RECEIPT.exists():
        print("C01_PROFILE_DISPATCH_READY_BINDING: NOT_READY_NO_RECEIPT")
        return 0

    try:
        data = json.loads(RECEIPT.read_text(encoding="utf-8"))
        if data.get("schema") != "actiongate-c01-profile-dispatch-receipt/v2":
            fail("dispatch receipt schema mismatch")
        if data.get("repository") != "ed3c/ActionGate" or data.get("issue") != 60:
            fail("dispatch receipt identity mismatch")
        if data.get("state") != "C01_PROFILE_HARDENED_SHADOW_DISPATCH_READY_FOR_EXTERNAL_REVIEW":
            fail("dispatch receipt state mismatch")

        checkout, receipt_commit = checked_out_subject()
        candidate = data.get("dispatch_candidate", {})
        commit = candidate.get("commit")
        tree = candidate.get("tree")
        if git("rev-parse", f"{receipt_commit}^") != commit:
            fail("receipt branch-head commit is not immediate successor of dispatch candidate")
        if git("rev-parse", f"{commit}^{{tree}}") != tree:
            fail("dispatch candidate tree mismatch")
        if git("rev-parse", f"{receipt_commit}:{RECEIPT_PATH}") != git("hash-object", RECEIPT_PATH):
            fail("checked-out dispatch receipt differs from exact branch-head receipt blob")

        workflow = data.get("hosted_workflow", {})
        if workflow.get("conclusion") != "success":
            fail("hosted workflow not successful")
        if not isinstance(workflow.get("run_id"), int) or workflow["run_id"] <= 0:
            fail("hosted workflow run id missing")
        if not isinstance(workflow.get("job_id"), int) or workflow["job_id"] <= 0:
            fail("hosted workflow job id missing")
        if workflow.get("head_sha") != commit:
            fail("hosted workflow does not bind dispatch candidate")

        if data.get("independent_review") != "NOT_EXERCISED":
            fail("dispatch receipt fabricates independent review")
        if data.get("c01_admitted") is not False or data.get("k01_started") is not False:
            fail("dispatch receipt widens authority")

        if args.review_receipt is not None:
            import importlib.util

            spec = importlib.util.spec_from_file_location("checker", ROOT / "check_dispatch.py")
            checker = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(checker)
            registry = checker.load(ROOT / "dispatch-registry.json")
            checker.validate_review_receipt(checker.load(args.review_receipt), registry)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"C01_PROFILE_DISPATCH_READY_BINDING: FAIL: {exc}", file=sys.stderr)
        return 2

    print("C01_PROFILE_DISPATCH_READY_BINDING: PASS")
    print(f"CHECKOUT_SUBJECT: {checkout}")
    print(f"RECEIPT_BRANCH_HEAD: {receipt_commit}")
    print("INDEPENDENT_REVIEW: NOT_EXERCISED" if args.review_receipt is None else "INDEPENDENT_REVIEW_RECEIPT: VALID")
    print("C01_ADMITTED: FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
