# Stage Prompt Catalogue

These files are copyable system prompts for separate ChatGPT/Codex sessions. They bind one exact ActionGate stage or molecular atom and must be instantiated with the current Issue, branch, base SHA, path/resource lease and acceptance criteria.

## Stages

| Stage | File | Primary issue(s) | Parallelism |
|---|---|---:|---|
| P0 authority/control plane | `P0_CONTROL_PLANE.md` | #2 | bounded documentation split |
| P1 sources/claims/rights | `P1_SOURCE_RIGHTS.md` | #3 | source, claim and rights workers may be parallel with disjoint outputs |
| P2 canonical contracts | `P2_CONTRACTS.md` | #4 | serializers/test-vector workers after one schema owner freezes interfaces |
| P3 deterministic core | `P3_CORE.md` | #5 | policy, lifecycle and property-test slices after contracts |
| P4 adapters | `P4_ADAPTERS.md` | #6-#9 | gateway, Android, iOS and MCP are sibling workers |
| P5 evidence | `P5_EVIDENCE.md` | #10 | mutation, concurrency, failure and trace/redaction workers |
| P6 E2E canary | `P6_E2E.md` | #11 | one convergence owner; attack workers remain read/test only |
| P7 convergence | `P7_CONVERGENCE.md` | #12 | exactly one aggregate writer |
| P8 physical/Human lanes | `P8_PHYSICAL_HUMAN.md` | #13 | Android, iOS, independent Shadow, rights/security and Human lanes remain independent |

## Required prompt instantiation

Replace every variable before dispatch:

```text
<BASE_SHA>
<BASE_BRANCH>
<WORK_BRANCH>
<ISSUE_URL>
<PARENT_PR_URLS>
<PATH_LEASE>
<RESOURCE_LEASE>
<PRIVATE_CONTEXT_STATE>
```

Private URLs are supplied only through the connected private binding and are never inserted into the prompt transcript when that transcript may be published.

## Common read order

```text
README.md
AGENTS.md
ARCHITECTURE.md
public/private authority contract
Issue DAG
Molecular Stack index
system contract and task DAG
exact Issue/parent PRs/heads/checks
applicable skills-shared procedure delta
optional private CodexDoc binding
```

## Common output

Every session emits a handoff packet matching `AGENTS.md`, plus:

```text
source/contract inputs consumed
changed paths and exact tree/head
verification commands and durable receipt
negative controls exercised
Shadow deltas/dissent
highest evidence ceiling earned
blockers and next entry condition
Human-owned operations
```

A chat answer is not a receipt. Persist the technical result in the owning branch/Issue/PR or declare `ABSENT`.

## Parallel session law

Parallel prompts are allowed only when:

```text
true prerequisites are readable
path/resource leases are disjoint
no two workers own the same schema/index/state
one convergence owner is declared
terminal workers cannot edit aggregate navigation
```

If two tasks merely happen in sequence but do not consume one another's unmerged state, keep them as siblings.