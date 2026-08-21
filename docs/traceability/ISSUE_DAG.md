# Issue DAG

## Edge semantics

One node graph carries two independent edge classes.

- **Start edge:** the prerequisite is readable and the child path/resource lease can begin. It is cheap and reversible.
- **Completion edge:** the child may claim completion only after an exact-subject receipt admits the prerequisite in its required lane. It is expensive and irreversible.

A startable child is not therefore completable. An unreceipted completion edge is `ABSENT`.

## Nodes

| Node | Atom | Issue | Completion owner | Required lane |
|---|---|---:|---|---|
| `N00` | Epic/global objective | #1 | Tech Lead convergence owner | multi-lane |
| `N01` | public/private authority and routes | #2 | C00 | cloud/static |
| `N02` | source/claim/rights admission | #3 | S01 | cloud/static + primary-source |
| `N03` | canonical protocol contracts | #4 | C01 | local-deterministic |
| `N04` | deterministic domain core | #5 | K01 | local-deterministic |
| `N05` | gateway/persistence/distributed semantics | #6 | A01 | local integration |
| `N06` | Android signer/integrity adapter | #7 | A02 | deterministic + physical |
| `N07` | iOS signer/integrity adapter | #8 | A03 | deterministic + physical |
| `N08` | MCP middleware | #9 | A04 | local integration |
| `N09` | adversarial/fault evidence harness | #10 | E01 | local/adversarial |
| `N10` | protected DevOps E2E | #11 | X01 | local integration |
| `N11` | aggregate convergence and handoff | #12 | D01 | exact-head read-back |
| `N12` | physical/security/legal/Human lanes | #13 | Human/independent authorities | physical/security/Human |

## Start edges

```text
N01 -> N02
N01 -> N03
N02 -> N03
N03 -> N04
N03 -> N06
N03 -> N07
N03 -> N09
N04 -> N05
N04 -> N08
N04 -> N09
N05 -> N10
N08 -> N10
N09 -> N10
N10 -> N11
N06 -> N12
N07 -> N12
N11 -> N12
```

An adapter may start against a stable published contract before every unrelated sibling is complete.

## Completion edges

```text
N01 + N02 -> N03
N03 -> N04
N03 + N04 -> N05
N03 -> deterministic portion of N06/N07
N03 + N04 -> N08
N03 + N04 -> N09
N03 + N04 + N05 + N08 + N09 -> N10
selected admitted C/K/A/E/X set -> N11
N11 + own-lane receipts -> N12
all required terminal receipts + Human Admit -> N00 closure
```

## Convergence ownership

`N11` is the only aggregate index writer. Terminal C/K/A/E/X workers write atom-local receipts and do not update README, AGENTS, global DAG, Stack index, or release/handoff summaries.

## Current state

```text
N01 IN_PROGRESS
N02-N12 BLOCKED or NOT_EXERCISED
```

Issue UI state is coordination metadata, not completion evidence.