#!/usr/bin/env python3
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECK = ROOT / "check_language_worker_receipt.py"
FIX = ROOT / "fixtures"
CASES = [
    (FIX / "valid.fixture.json", True, 0),
    (FIX / "valid.fixture.json", False, 2),
    (FIX / "bad-denominator.fixture.json", True, 2),
    (FIX / "private-url.fixture.json", True, 2),
]
for path, fixture_mode, expected in CASES:
    argv = [sys.executable, str(CHECK), str(path)]
    if fixture_mode:
        argv.append("--fixture-mode")
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode != expected:
        raise SystemExit(
            f"{path.name}: expected {expected}, got {result.returncode}: "
            f"{result.stdout}{result.stderr}"
        )
print(f"language-worker receipt selftest: PASS ({len(CASES)} cases)")
