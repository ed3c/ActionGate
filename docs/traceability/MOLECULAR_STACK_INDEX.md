# Molecular Stack Index

## Derivation law

This index is derived from observed Issues, PR bases/heads, commits, changed paths, checks and receipts. Chronology and branch naming do not create dependency.

A Draft PR is candidate evidence. `MERGEABLE` is not `VERIFIED`. A review-only Shadow is never a Git parent. When a parent contract moves after Worker results exist, preserve the old candidate and create a typed replay/supersession decision rather than silently rebasing.

## Merged bootstrap stack

| Atom | Class | Issue | PR | Stable merge commit | Historical relation | Lease | Evidence ceiling | State |
|---|---|---:|---:|---|---|---|---|---|
| `C00` | C/D | #2 | [#14](https://github.com/ed3c/ActionGate/pull/14) | `fee8c290061542bfb93e27ddcc33cce7fbf8c653` | top-level from original main | root control/governance/trace paths | cloud/static | `MERGED` |
| `S01` | C/E | #3 | [#15](https://github.com/ed3c/ActionGate/pull/15) | `8810fe41f66ad1b4fe80db5f93bf9539e2a38899` | consumed C00 authority; sibling to D00 | source/rights/candidate ledger | source disposition | `MERGED` |
| `D00` | D | #2 | [#16](https://github.com/ed3c/ActionGate/pull/16) | `76efa9297d147712bb9dfbb9e797d69ca9432a99` | consumed C00 authority; sibling to S01 | prompts/handoff/queue | cloud/static | `MERGED`; queue not executed |

The merge graph records historical parents. Current technical truth is the exact `main` tree.

## Active C01 Stack

| Atom | Class | Issue | Branch / PR | Exact observed head | True relation | Lease | Oracle / lane | Current disposition |
|---|---|---:|---|---|---|---|---|---|
| `C01` | C | #4 | `ag/C01-action-contracts` / [#17](https://github.com/ed3c/ActionGate/pull/17) | `b63589e5a16e82fda1a9554227f2ebbb55398c8a` | consumed S01 constraints | `contracts/v1/**` and C01 control files | cross-language vectors + mutations | `DRAFT_PREPARATION`; do not merge |
| `C01-K` | C/E | #18 | `ag/C01-kotlin-vectors` / [#34](https://github.com/ed3c/ActionGate/pull/34) | `0136936e7d63ba0c538d2cb40db60409107ababc` | sibling after C01 freeze | `contracts/impl/kotlin/**` | Kotlin exact bytes/hashes | `PREPARATION_ONLY` |
| `C01-S` | C/E | #19 | `ag/C01-swift-vectors` / [#35](https://github.com/ed3c/ActionGate/pull/35) | `76b10b5a05898410ed361761626b381158edb306` | sibling after C01 freeze | `contracts/impl/swift/**` | Swift exact bytes/hashes | `PREPARATION_ONLY` |
| `C01-T` | C/E | #20 | `ag/C01-typescript-vectors` / [#36](https://github.com/ed3c/ActionGate/pull/36) | `c62e24ffa0ceb2224fe6931929bfaeeceabe3c39` | sibling after C01 freeze | `contracts/impl/typescript/**` | TypeScript exact bytes/hashes | `PREPARATION_ONLY` |
| `C01-EP` | D/E | #37 | `ag/C01-execution-preflight` / [#38](https://github.com/ed3c/ActionGate/pull/38) | `9f41038240837ea2dd9dcdb9befd13e6ba81a78e` | true child of C01; process/evidence sibling of C01-K/S/T | `.actiongate/c01-execution/**`, common/schema evidence | preparation checks | `DRAFT_PREPARATION`; do not merge into frozen C01 |
| `C01-LP` | D | #39 | `ag/C01-worker-launch-packets` / PR absent | absent | true child of C01-EP; routing sibling of implementations | `.actiongate/c01-launch/**` | launch-packet mutations | `READY_TO_PREPARE` |
| `C01-SH` | E/H | #26 | no branch/PR | absent | independent read-only evidence | no implementation writer | same-subject audit | `NOT_EXERCISED` |
| `C01-CV` | X/D | #24 | one semantic convergence subject | absent | consumes exact language/schema/Shadow receipts | convergence receipt/index only | C01 admission | `BLOCKED_BY_WORKERS` |

### C01 admission law

```text
language preparation PRs
!= language implementation

toolchain presence
!= vector parity

schema validity
!= grant authenticity or authorization

same-context preflight
!= independent Shadow

mergeable Draft
!= C01_ADMITTED
```

Only Issue #24 can emit `C01_ADMITTED | HOLD | REJECT`. Until `C01_ADMITTED`, K01 remains blocked.

## Partial main convergence atom

| Atom | Class | Issue | Branch | Relation | Lease | State |
|---|---|---:|---|---|---|---|
| `D00-MAIN` | D | #40 | `docs/40-main-convergence` | consumes merged #14/#15/#16 main state; not a parent of C01 workers | aggregate README/AGENTS/DAG/Stack/handoff paths | `IN_PROGRESS` |

This atom records current reality only. It does not repair C01 or close final P7/#12.

## Downstream planned atoms

| Atom | Issue | True prerequisite | Lease | Required oracle | State |
|---|---:|---|---|---|---|
| `K01` | #5 | exact `C01_ADMITTED` | core/policy | property and mutation tests | `BLOCKED` |
| `A01` | #6 | C01 + K01 | gateway/verifier/persistence | concurrency/restart/reconciliation | `NOT_IMPLEMENTED` |
| `A02` | #7 | C01 + stable core port | Android SDK | deterministic + physical | `NOT_IMPLEMENTED` |
| `A03` | #8 | C01 + stable core port | iOS SDK | deterministic + physical | `NOT_IMPLEMENTED` |
| `A04` | #9 | C01 + K01 | MCP middleware | bypass/audience/replay | `NOT_IMPLEMENTED` |
| `E01` | #10 | C01 + K01 | tests/testkit/CI | full mutation/fault denominator | `NOT_IMPLEMENTED` |
| `X01` | #11 | admitted A01/A04/E01 + C/K | DevOps E2E | happy path once + attack matrix | `NOT_IMPLEMENTED` |
| `D01` | #12 | selected admitted terminal set | aggregate indexes | exact-main/clean-checkout readback | `OPEN / BLOCKED` |
| `H01` | #13 | immutable D01 candidate | devices/security/legal/Human | own-lane receipts | `NOT_EXERCISED` |

## PR disposition at this checkpoint

| PR | Disposition |
|---:|---|
| #14 | merged; close history retained |
| #15 | merged; close history retained |
| #16 | merged; close history retained |
| #17 | keep Draft/open until C01 convergence |
| #34/#35/#36 | keep Draft/open; implementation not present |
| #38 | keep Draft/open; preparation only and merging would move the frozen C01 epoch |
| future #40 PR | may merge after exact path/readback review; documentation-only ceiling |

## Publication states

```text
PLANNED
BRANCH_CREATED
DRAFT_PUBLISHED
PREPARATION_ONLY
EXACT_HEAD_VERIFIED
READY_FOR_REVIEW
MERGED
BLOCKED
NOT_IMPLEMENTED
NOT_EXERCISED
HUMAN_ADMIT_REQUIRED
```

## Movement and stale-evidence rule

Parent movement invalidates affected candidate receipts. Empty pre-result branches may move only with exact readback and no force. Non-empty Worker branches require explicit supersession/replay. Merge/release remain Human-owned.
