# Molecular Stack Index

## Derivation law

This index is derived from observed Issues, refs, PR bases/heads, changed paths, checks and receipts. Branch names and chronological order are not dependency evidence.

Each atom declares class, Issue, branch/ref, true parents, path/resource lease, required evidence lane, owning oracle, blockers and review/build-on policy.

A Draft PR is not a verified atom. A published atom carrying a blocker remains incomplete. A review-only atom is never a parent and never merges.

## Observed bootstrap stack

| Atom | Class | Issue | Branch | PR | Observed base | Current observed head | Lease | Oracle / evidence lane | State |
|---|---|---:|---|---:|---|---|---|---|---|
| `C00` | C/D | #2 | `ag/C00-technical-control-plane` | [#14](https://github.com/ed3c/ActionGate/pull/14) | `main` | authoritative in PR #14 | aggregate bootstrap paths | GitHub exact-tree read-back + public/private leak scan / cloud-static | `DRAFT_PUBLISHED` |
| `S01` | C/E | #3 | `ag/S01-source-rights` | [#15](https://github.com/ed3c/ActionGate/pull/15) | `ag/C00-technical-control-plane` | authoritative in PR #15 | `docs/sources/**`, rights/candidate JSON | primary repository/license read-back / cloud-static | `DRAFT_PUBLISHED` |
| `D00` | D | #2 | `ag/D00-prompts-handoff` | [#16](https://github.com/ed3c/ActionGate/pull/16) | `ag/C00-technical-control-plane` | authoritative in PR #16 | `docs/prompts/**`, `docs/handoff/**`, queue/catalog JSON | prompt/queue contract review / cloud-static | `DRAFT_PUBLISHED` |

`S01` and `D00` are siblings. Each consumes C00 authority/contracts and neither consumes the other's unmerged files or state.

## Planned downstream atoms

| Atom | Class | Issue | Branch | True parent(s) | Lease | Oracle | Lane | State |
|---|---|---:|---|---|---|---|---|---|
| `C01` | C | #4 | `ag/C01-action-contracts` | admitted `C00+S01` | `contracts/**` | cross-language vectors + mutation fixtures | local-deterministic | `BLOCKED` |
| `K01` | K | #5 | `ag/K01-domain-core` | `C01` | core/policy paths | unit/property/mutation tests | local-deterministic | `BLOCKED` |
| `A01` | A | #6 | `ag/A01-gateway` | `C01+K01` | gateway/verifier/persistence | restart/concurrency/reconciliation tests | integration | `BLOCKED` |
| `A02` | A | #7 | `ag/A02-android` | `C01`, stable K port | Android SDK only | unit/instrumentation + physical queue | deterministic/physical | `BLOCKED` |
| `A03` | A | #8 | `ag/A03-ios` | `C01`, stable K port | iOS SDK only | unit/simulator + physical queue | deterministic/physical | `BLOCKED` |
| `A04` | A | #9 | `ag/A04-mcp` | `C01+K01` | MCP middleware only | bypass/audience/replay integration tests | integration | `BLOCKED` |
| `E01` | E | #10 | `ag/E01-evidence-harness` | `C01+K01` | tests/testkit/CI | mutation/fault/trace assertions | adversarial | `BLOCKED` |
| `X01` | X | #11 | `ag/X01-devops-e2e` | admitted A01+A04+E01 | DevOps example/E2E receipts | exact canary + attack matrix | integration | `BLOCKED` |
| `D01` | D/X | #12 | `ag/D01-convergence` | selected admitted release set | aggregate indexes/handoff | exact-head + synthetic-merge/clean-checkout read-back | multi-lane | `BLOCKED` |
| `H01` | H | #13 | local/Human lanes | `D01` | devices/review/legal/Human | own-lane receipts | physical/security/legal/Human | `NOT_EXERCISED` |

## Publication states

```text
PLANNED
BRANCH_CREATED
DRAFT_PUBLISHED
EXACT_HEAD_VERIFIED
READY_FOR_REVIEW
MERGED
RELEASED
BLOCKED
NOT_EXERCISED
HUMAN_ADMIT_REQUIRED
```

## Movement and stale-evidence rule

When a parent branch moves, every affected child must rebind its base, recompute changed paths, and rerun owning assertions. A successful merge/rebase/sync proves graph movement only. It cannot promote implementation or evidence state.

Exact heads and checks are read from GitHub PR metadata. Aggregate documentation intentionally avoids copying a head SHA that would become stale on its own next commit.