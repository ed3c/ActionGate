#!/usr/bin/env python3
from __future__ import annotations
import copy, importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("checker", ROOT / "check_launch_packets.py")
checker = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(checker)

def set_path(obj, path, value):
    cur = obj
    for part in path[:-1]:
        cur = cur[part] if isinstance(part, str) else cur[part]
    cur[path[-1]] = value

def run() -> int:
    base = checker.load(ROOT / "launch-registry.json")
    checker.check_registry(base)
    checker.check_attestation(checker.load(ROOT / "clean-room-attestation.template.json"))
    cases = [
        ("STALE_C01_EPOCH", ["contract_epoch", "sha"], "0" * 40),
        ("LEASE_OVERLAP", ["workers", 1, "lease", "paths", 0], base["workers"][0]["lease"]["paths"][0]),
        ("FALSE_SESSION_OBSERVED", ["workers", 0, "state"], "SESSION_OBSERVED"),
        ("SAME_CONTEXT_SHADOW_WIDENED", ["independent_shadow", "same_context_may_satisfy"], True),
        ("HUMAN_ATTESTATION_AUTHORITY_WIDENED", ["current_conversation_eligibility", "may_fabricate_human_attestation"], True),
        ("PRIVATE_URL_IN_REGISTRY", ["private_context_url"], "https://docs.google.com/document/d/forbidden"),
    ]
    passed = 1
    for expected, path, value in cases:
        data = copy.deepcopy(base)
        set_path(data, path, value)
        try:
            checker.check_registry(data)
        except checker.PacketError as exc:
            if str(exc) != expected:
                print(f"{expected}: FAIL got {exc}")
                return 1
            print(f"{expected}: PASS")
            passed += 1
        else:
            print(f"{expected}: FAIL mutation accepted")
            return 1
    print(f"C01 launch selftest: PASS {passed}/{len(cases)+1}")
    return 0

if __name__ == "__main__":
    raise SystemExit(run())
