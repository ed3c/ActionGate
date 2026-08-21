#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_C01 = "b63589e5a16e82fda1a9554227f2ebbb55398c8a"
EXPECTED_EXEC = "9f41038240837ea2dd9dcdb9befd13e6ba81a78e"
EXPECTED = {
  "kotlin": (18, 34, "ag/C01-kotlin-vectors", "0136936e7d63ba0c538d2cb40db60409107ababc", "d5d9a7d4a4d6f725b80f324035ef8880bb347240", "contracts/impl/kotlin/**"),
  "swift": (19, 35, "ag/C01-swift-vectors", "76b10b5a05898410ed361761626b381158edb306", "d71add9be3bea0149347e2f3dd81d2ba183e4bd7", "contracts/impl/swift/**"),
  "typescript": (20, 36, "ag/C01-typescript-vectors", "c62e24ffa0ceb2224fe6931929bfaeeceabe3c39", "e69eb7fcd2162c7d07a674677a3433eeb2aa9e57", "contracts/impl/typescript/**"),
}
PRIVATE_URL_RE = re.compile(r"https?://(?:docs|drive)\.google\.com", re.I)
PLACEHOLDER_RE = re.compile(r"<[A-Z0-9_ -]+>")

class PacketError(ValueError):
    pass

def fail(code: str) -> None:
    raise PacketError(code)

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def check_registry(data: dict) -> None:
    if data.get("schema") != "actiongate-c01-worker-launch-registry/v1": fail("BAD_SCHEMA")
    if data.get("repository") != "ed3c/ActionGate" or data.get("issue") != 39: fail("BAD_IDENTITY")
    if data.get("state") != "C01_WORKER_SESSION_LAUNCH_PACKETS_READY": fail("BAD_PHASE_STATE")
    if data.get("contract_epoch", {}).get("sha") != EXPECTED_C01: fail("STALE_C01_EPOCH")
    if data.get("execution_control", {}).get("sha") != EXPECTED_EXEC: fail("STALE_EXECUTION_CONTROL")
    ctx = data.get("current_conversation_eligibility", {})
    if ctx.get("implementation_session_allowed") is not False: fail("PRIVATE_CONTEXT_IMPLEMENTATION_WIDENED")
    if ctx.get("may_fabricate_human_attestation") is not False: fail("HUMAN_ATTESTATION_AUTHORITY_WIDENED")
    if data.get("worker_relation") != "PATH_DISJOINT_SIBLINGS_NO_INTER_WORKER_GIT_PARENT": fail("FALSE_WORKER_SERIALIZATION")

    seen_branch, seen_lease, seen_prompt = set(), set(), set()
    workers = data.get("workers")
    if not isinstance(workers, list) or len(workers) != 3: fail("BAD_WORKER_COUNT")
    for worker in workers:
        lang = worker.get("language")
        if lang not in EXPECTED: fail("UNKNOWN_WORKER")
        issue, pr, branch, head, tree, lease = EXPECTED[lang]
        actual_branch = worker.get("branch")
        actual_lease = (worker.get("lease", {}).get("paths") or [None])[0]
        actual_prompt = worker.get("prompt")
        for value, seen, code in [
            (actual_branch, seen_branch, "DUPLICATE_BRANCH"),
            (actual_lease, seen_lease, "LEASE_OVERLAP"),
            (actual_prompt, seen_prompt, "DUPLICATE_PROMPT"),
        ]:
            if value in seen: fail(code)
            seen.add(value)
        actual = (
            worker.get("issue"), worker.get("pr"), actual_branch,
            worker.get("preparation_head"), worker.get("preparation_tree"),
            actual_lease
        )
        if actual != (issue, pr, branch, head, tree, lease): fail(f"STALE_OR_MISBOUND_{lang.upper()}")
        if worker.get("state") != "LAUNCH_PACKET_READY_NOT_LAUNCHED": fail("FALSE_SESSION_OBSERVED")
        if worker.get("clean_room_state") != "HUMAN_DECLARATION_REQUIRED": fail("CLEAN_ROOM_FALSE_PASS")
        if worker.get("runtime_state") != "REPROBE_IN_ACTUAL_SESSION": fail("RUNTIME_RECEIPT_REUSED")
        if worker.get("implementation_state") != "NOT_IMPLEMENTED": fail("FALSE_IMPLEMENTATION_STATE")

        prompt_path = ROOT.parent.parent / worker["prompt"]
        if not prompt_path.exists(): fail(f"MISSING_PROMPT_{lang.upper()}")
        text = prompt_path.read_text(encoding="utf-8")
        if PLACEHOLDER_RE.search(text): fail(f"UNRESOLVED_PLACEHOLDER_{lang.upper()}")
        for token in [str(issue), str(pr), branch, head, tree, lease, EXPECTED_C01, EXPECTED_EXEC,
                      "NO_PRIOR_CONTEXT", "CLEAN-ROOM GATE", "LAUNCH_REQUEST_IS_NOT_SESSION_OBSERVED",
                      "NO_MERGE"]:
            if token not in text: fail(f"PROMPT_BINDING_MISSING_{lang.upper()}")
        if PRIVATE_URL_RE.search(text): fail("PRIVATE_URL_IN_PROMPT")

    shadow = data.get("independent_shadow", {})
    if shadow.get("same_context_may_satisfy") is not False: fail("SAME_CONTEXT_SHADOW_WIDENED")
    if shadow.get("state") != "BLOCKED_BY_WORKER_RECEIPTS": fail("FALSE_INDEPENDENT_SHADOW_STATE")

    queue = data.get("local_handoff_queue", {})
    items = queue.get("items", [])
    active = [x for x in items if x.get("state") == "ACTIVE"]
    if len(active) != 1 or active[0].get("id") != queue.get("active_item"): fail("QUEUE_ACTIVE_CARDINALITY")
    if "CLH-001" != queue.get("active_item"): fail("WRONG_ACTIVE_ITEM")
    for op in ["clean-room declaration","merge","release","security/legal acceptance"]:
        if op not in data.get("human_owned", []): fail("MISSING_HUMAN_AUTHORITY")
    raw = json.dumps(data)
    if PRIVATE_URL_RE.search(raw): fail("PRIVATE_URL_IN_REGISTRY")

def check_attestation(template: dict) -> None:
    if template.get("schema") != "actiongate-clean-room-session-declaration/v1": fail("BAD_ATTESTATION_SCHEMA")
    if template.get("template") is not True: fail("ATTESTATION_TEMPLATE_FALSE")
    if template.get("contract_epoch") != EXPECTED_C01: fail("ATTESTATION_STALE_EPOCH")
    declarations = template.get("declarations", {})
    if not declarations or any(value is not False for value in declarations.values()): fail("TEMPLATE_FABRICATES_HUMAN_PASS")
    if template.get("technical_disposition") != "HUMAN_REVIEW_REQUIRED": fail("TECHNICAL_ATTESTATION_FALSE_PASS")
    if template.get("legal_clearance") != "HUMAN_ADMIT_REQUIRED": fail("LEGAL_CLEARANCE_WIDENED")
    if PRIVATE_URL_RE.search(json.dumps(template)): fail("PRIVATE_URL_IN_ATTESTATION")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=ROOT / "launch-registry.json")
    parser.add_argument("--attestation", type=Path, default=ROOT / "clean-room-attestation.template.json")
    args = parser.parse_args()
    try:
        check_registry(load(args.registry))
        check_attestation(load(args.attestation))
    except (PacketError, json.JSONDecodeError, OSError, KeyError, TypeError) as exc:
        print(f"C01 launch packet check: FAIL: {exc}")
        return 1
    print("C01 launch packet check: PASS")
    print("Worker Session execution: NOT_LAUNCHED")
    print("Human clean-room declaration: REQUIRED")
    print("Independent Shadow / C01 convergence / K01: BLOCKED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
