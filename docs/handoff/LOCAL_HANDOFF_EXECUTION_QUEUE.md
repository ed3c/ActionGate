# Local Handoff Execution Queue

Machine authority: `.actiongate/local-handoff-queue.json`. This file cannot widen it.

Exactly one item is ACTIVE. A receipt may make siblings eligible, but no item auto-executes and queue order does not create Git ancestry.

## Boundary

Use an empty personal clean-room directory. Keep employer/private source, credentials, customer data and private protocols outside implementation Sessions.

No item grants reset, rebase, sync, push, merge, branch deletion, semantic-conflict resolution, dependency installation/license acceptance, release, production or rollback without explicit Human authority.

## LH-MAIN-001 — ACTIVE

Resolve `origin/main` at execution time and bind exact SHA/tree. Required stable ancestors:

```text
fee8c290061542bfb93e27ddcc33cce7fbf8c653  # C00/#14
8810fe41f66ad1b4fe80db5f93bf9539e2a38899  # S01/#15
76efa9297d147712bb9dfbb9e797d69ca9432a99  # D00/#16
71796b8c4d50fdfbcade85f9bbdf4d3ec988ba99  # D00-MAIN/#42
53f1014e4c75a0083c8ebe2972e8f52f3ff33b9d  # D00-DELTA/#44
```

```bash
git clone https://github.com/ed3c/ActionGate.git ActionGate
git -C ActionGate fetch origin --prune
git -C ActionGate switch --detach origin/main
git -C ActionGate rev-parse HEAD
git -C ActionGate rev-parse HEAD^{tree}
git -C ActionGate merge-base --is-ancestor fee8c290061542bfb93e27ddcc33cce7fbf8c653 HEAD
git -C ActionGate merge-base --is-ancestor 8810fe41f66ad1b4fe80db5f93bf9539e2a38899 HEAD
git -C ActionGate merge-base --is-ancestor 76efa9297d147712bb9dfbb9e797d69ca9432a99 HEAD
git -C ActionGate merge-base --is-ancestor 71796b8c4d50fdfbcade85f9bbdf4d3ec988ba99 HEAD
git -C ActionGate merge-base --is-ancestor 53f1014e4c75a0083c8ebe2972e8f52f3ff33b9d HEAD
git -C ActionGate diff --check
python3 -m json.tool ActionGate/.actiongate/system-contract.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/task-dag.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/local-handoff-queue.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/source-claims.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/technology-candidates.json >/dev/null
```

Receipt: `ActionGate/.actiongate/receipts/local/LH-MAIN-001.json`.

It records exact SHA/tree, ancestor and parse results, required document presence, PR #41 state, public/private review and clean-room separation without private locator values.

Next: at most one of `LH-STACK-002` or `C01-SESSION-003`.

## LH-STACK-002 — BLOCKED_BY_PREDECESSOR

After LH-MAIN-001, observe Git Town capability and the S01 → C01 → PR #38 → PR #41 graph plus the three language siblings. No sync/rebase/reset/push/merge. Tool absence may be recorded as `BLOCKED_ABSENT_EXECUTABLE` without installing it.

## C01-SESSION-003 — BLOCKED_BY_HUMAN_CLEANROOM_AND_FRESH_SESSION

Exact launch source:

```text
Issue #39  CLOSED_PREPARATION_ONLY
PR #41     98c9545c0dd2bbfdabdaf27c8a992822a78b3840
```

Entry:

```text
PR #41 exact head current
+ selected PR #34/#35/#36 head/lease current
+ Human clean-room declaration
+ new public-input-only Session
+ target Session runtime re-probe
```

This private-context conversation cannot satisfy that gate. A launch packet/request is not `SESSION_OBSERVED`. The selected Session may implement one language lease and return one Worker receipt; it cannot close another language, independent Shadow, C01 convergence, hardware, MCP, legal, merge or release.

## Later lanes

- `LH-ANDROID-004`: physical Android, blocked by implementation;
- `LH-IOS-005`: physical iOS, blocked by implementation;
- `LH-SECURITY-006`: independent security/clean-room review, blocked by immutable candidate;
- `LH-HUMAN-007`: explicit legal/security/merge/release/production/rollback/public-private decision.

Queue correctness is not command execution, Session existence, implementation correctness, physical proof, independent review, legal clearance or release/production admission.
