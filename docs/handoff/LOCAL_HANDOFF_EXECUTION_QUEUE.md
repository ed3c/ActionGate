# Local Handoff Execution Queue

Machine authority: `.actiongate/local-handoff-queue.json`. This projection cannot widen it.

Exactly one item is ACTIVE. After a valid receipt, the controller may activate exactly one eligible candidate. Queue scheduling does not create Git ancestry or semantic dependency between otherwise independent evidence lanes.

## Boundary

Use an empty personal clean-room directory. Keep employer/private source, credentials, customer data, private protocols, and private locator values outside implementation/evidence outputs.

No queue item grants reset, rebase, sync, push, branch deletion, merge, dependency installation/license acceptance, legal/security admission, release, production, or rollback unless the item explicitly routes to the Human authority that owns that decision.

## LH-MAIN-001 — ACTIVE

Purpose: bind the **then-current** `origin/main` after this documentation convergence lands.

Pre-checkpoint main:

```text
70573aed229404772827829a1ce069a6e72184fa
tree e31f35bf0b60977df995df6f97dde941dfe529f9
```

Required operation:

```bash
git clone https://github.com/ed3c/ActionGate.git ActionGate
git -C ActionGate fetch origin --prune
git -C ActionGate switch --detach origin/main
git -C ActionGate rev-parse HEAD
git -C ActionGate rev-parse HEAD^{tree}
git -C ActionGate merge-base --is-ancestor 70573aed229404772827829a1ce069a6e72184fa HEAD
git -C ActionGate diff --check
python3 -m json.tool ActionGate/.actiongate/system-contract.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/task-dag.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/local-handoff-queue.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/source-claims.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/technology-candidates.json >/dev/null
```

Manual exact-state readback must check:

```text
PR #17   b63589e5a16e82fda1a9554227f2ebbb55398c8a   open/Draft
PR #34   cf589a0990aaaa6422be9c649b52b44230d570f6   open/Draft
PR #35   039827061f54aa72e2b81365a4c904d25833f83e   open/Draft
PR #36   3ed9f0307df0937028bbf52fe8fbd2a6621acafe   open/Draft
PR #54   d9716d029578608b6179c56def6f7ea8c3728146   open/Draft
PR #61   2998b0a93d23ddfca0934250d82bdbd892f2c84b   open/Draft
PR #63   e4196305284b4751286b01f5d1d33e82fc34af0b   open/Draft

PR #38 / #41 / #59
  closed unmerged historical subjects

Issues #18/#19/#20/#60/#62
  closed at declared evidence ceilings

Issues #24/#26/#55/#56
  remain open/blocked according to their exact current state
```

Any mismatch is a typed `STATE_DELTA`; do not “repair” it by reset/rebase/sync/push.

Receipt:

```text
ActionGate/.actiongate/receipts/local/LH-MAIN-001.json
```

Exit: exact current-main and current-topology readback PASS.

Next eligible candidates are independent scheduling alternatives:

```text
LH-STACK-002
C01-EXT-SHADOW-003
PRV01-EXT-SHADOW-004
```

The controller chooses at most one ACTIVE next item.

## LH-STACK-002 — BLOCKED_BY_CONTROLLER_SELECTION

Entry: valid `LH-MAIN-001`.

Observe only:

```text
git-town --version
C01 contract -> PR #34/#35/#36 sibling ancestry
historical exact preparation commits
PR #61 -> PR #63 true-child ancestry
```

If Git Town is unavailable, record `BLOCKED_ABSENT_EXECUTABLE`. Do not install it in this item.

Forbidden:

```text
git town sync
rebase
reset
push
merge
branch deletion
semantic conflict resolution
```

Evidence ceiling: local branch/Stack capability only.

## C01-EXT-SHADOW-003 — BLOCKED_BY_CONTROLLER_SELECTION

Critical-path external evidence item.

Entry:

```text
PR #61 == 2998b0a93d23ddfca0934250d82bdbd892f2c84b
PR #34 == cf589a0990aaaa6422be9c649b52b44230d570f6
PR #35 == 039827061f54aa72e2b81365a4c904d25833f83e
PR #36 == 3ed9f0307df0937028bbf52fe8fbd2a6621acafe
reviewer did not implement or repair the audited subjects
```

Operation:

```text
read PR #61 profile-v2 scoped AGENTS/README
execute Issue #26 independent Shadow prompt
bind exact contract/common/Worker commit/tree/blob identities
execute all 33 required falsifiers exactly once
return a schema-valid independent receipt
```

Allowed terminal:

```text
ELIGIBLE_FOR_C01_CONVERGENCE
HOLD
REJECT
```

The reviewer is read-only with respect to repository source/branches/PR metadata.

A same-context Builder or hosted checker cannot satisfy this item.

## PRV01-EXT-SHADOW-004 — BLOCKED_BY_CONTROLLER_SELECTION

Parallel external evidence candidate, not a dependency of C01.

Entry:

```text
PR #54 == d9716d029578608b6179c56def6f7ea8c3728146
changed-path denominator == 30
reviewer did not implement/repair PR #54
```

Execute Issue #55 and all fourteen fixed provenance falsifiers.

Allowed terminal:

```text
ADMIT_STATIC_PROVENANCE
BLOCK
REPLAN
```

This proves static provenance controls only. It cannot decide employment/IP/business overlap, legal clearance, or merge.

## C01-CONVERGENCE-005 — BLOCKED_BY_ISSUE_26

Entry:

```text
valid Issue #26 external receipt
PR #63 == e4196305284b4751286b01f5d1d33e82fc34af0b
```

Issue #24 is the sole semantic owner. It consumes the independent receipt plus the exact language/schema/rights/evidence subjects.

Allowed terminal:

```text
C01_ADMITTED
HOLD
REJECT
```

Even `C01_ADMITTED` does not itself merge PRs, start production, or prove hardware/MCP/security/legal behavior.

## PRV01-HUMAN-MERGE-006 — BLOCKED_BY_ISSUE_55

Entry: Issue #55 returns `ADMIT_STATIC_PROVENANCE`.

A Human explicitly decides whether PR #54 may merge. If merged, bind the GitHub merge receipt and post-merge main SHA/tree before Issue #56.

## K01-PREP-007 — BLOCKED_BY_C01_ADMISSION

Entry: exact Issue #24 verdict `C01_ADMITTED`.

Activate Issues #25/#28 preparation only. Do not promote preparation to K01 implementation.

## PRV01-CONVERGENCE-008 — BLOCKED_BY_PRV01_MERGE

Entry: PR #54 independently admitted, Human-approved, actually merged, and post-merge main read back.

Issue #56 then updates provenance navigation as one aggregate writer.

## Later evidence lanes

- `LH-ANDROID-009`: blocked until Android adapter implementation exists; physical device only.
- `LH-IOS-010`: blocked until iOS adapter implementation exists; physical iPhone only.
- `LH-HUMAN-011`: legal/security/merge/release/production/rollback/public-private decisions; Human-owned.

## Non-substitution law

```text
queue correctness != command execution
local main readback != independent review
hosted dispatch PASS != independent Shadow PASS
same-context Shadow != independent Shadow
C01_ADMITTED != hardware/MCP/security/legal PASS
simulator != physical device
static provenance admission != employment/legal clearance
technical readiness != user value/payment
```
