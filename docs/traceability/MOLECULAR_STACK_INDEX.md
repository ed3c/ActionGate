# Molecular Stack Index

## Laws

The index is derived from observed Issues, refs, parent relationships, changed paths, PR heads, checks, and receipts. Branch names and chronological creation order are not dependency evidence.

Each atom declares:

```text
class
issue
branch/ref
base/true parents
path/resource lease
required evidence lane
owning oracle
blockers
review/build-on policy
```

A published atom carrying an unresolved blocker is not complete. A review-only atom is never a parent and never merges.

## Planned atoms

| Atom | Class | Issue | Branch | True parent(s) | Lease | Oracle | Lane | State |
|---|---|---:|---|---|---|---|---|---|
| `C00` | C/D | #2 | `ag/C00-technical-control-plane` | `main` | README/AGENTS/architecture/governance/traceability/bootstrap JSON | exact-tree read-back + leak scan | cloud/static | `IN_PROGRESS` |
| `S01` | C/E | #3 | `ag/S01-source-rights` | `C00` | `docs/sources/**`, source/right JSON | primary-source/license locator checks | cloud/static | `PLANNED` |
| `D00` | D | #2 | `ag/D00-prompts-handoff` | `C00` | `docs/prompts/**`, `docs/handoff/**`, handoff JSON | prompt/queue contract review | cloud/static | `PLANNED` |
| `C01` | C | #4 | `ag/C01-action-contracts` | admitted `C00+S01` | `contracts/**` | cross-language vectors + mutation fixtures | local-deterministic | `BLOCKED` |
| `K01` | K | #5 | `ag/K01-domain-core` | `C01` | core/policy paths | unit/property/mutation tests | local-deterministic | `BLOCKED` |
| `A01` | A | #6 | `ag/A01-gateway` | `C01+K01` | gateway/verifier/persistence | restart/concurrency/reconciliation tests | integration | `BLOCKED` |
| `A02` | A | #7 | `ag/A02-android` | `C01`, stable K port | Android SDK only | unit/instrumentation + physical queue | deterministic/physical | `BLOCKED` |
| `A03` | A | #8 | `ag/A03-ios` | `C01`, stable K port | iOS SDK only | unit/simulator + physical queue | deterministic/physical | `BLOCKED` |
| `A04` | A | #9 | `ag/A04-mcp` | `C01+K01` | MCP middleware only | bypass/audience/replay integration tests | integration | `BLOCKED` |
| `E01` | E | #10 | `ag/E01-evidence-harness` | `C01+K01` | tests/testkit/CI | mutation/fault/trace assertions | adversarial | `BLOCKED` |
| `X01` | X | #11 | `ag/X01-devops-e2e` | admitted A01+A04+E01 | DevOps example/E2E receipts | exact canary + attacks | integration | `BLOCKED` |
| `D01` | D/X | #12 | `ag/D01-convergence` | selected admitted release set | aggregate indexes/handoff | exact-head + synthetic-merge read-back | multi-lane | `BLOCKED` |
| `H01` | H | #13 | local/Human lanes | D01 | devices/review/legal/Human | own-lane receipts | physical/Human | `NOT_EXERCISED` |

## Publication states

Use exact states:

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

This bootstrap document is a plan. After the first Draft PR is created, the convergence owner must replace `pending` topology with observed PR URLs, heads, bases, and verification receipts.