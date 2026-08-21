# Issue DAG

## Edge semantics

The graph carries separate edge classes:

- **start edge** — an exact prerequisite interface is readable and a disjoint lease may begin;
- **completion edge** — the child may claim completion only after the prerequisite's exact-subject receipt is admitted in its own lane;
- **process/evidence edge** — a runtime, Shadow, projection, local or Human receipt is required but does not create Git ancestry;
- **publication edge** — a branch/PR may be published without satisfying implementation completion.

A startable or mergeable atom is not therefore completable.

## Primary stage nodes

| Node | Atom | Issue | Owner | Required lane | Current state |
|---|---|---:|---|---|---|
| `N00` | Epic/global objective | #1 | final Tech Lead + Human convergence | multi-lane | `OPEN` |
| `N01` | C00 authority/routes | #2 | control-plane owner | cloud/static | `MERGED` |
| `N02` | S01 source/claim/rights | #3 | source-rights owner | cloud/static + source read-back | `MERGED` |
| `N02D` | D00 prompts/handoff | #2 | prompt/handoff owner | cloud/static | `MERGED`; execution not exercised |
| `N03` | C01 canonical contracts | #4 | one semantic contract owner | local-deterministic | `DRAFT_PREPARATION` |
| `N04` | K01 deterministic core | #5 | core owner | local-deterministic | `BLOCKED_BY_C01_ADMISSION` |
| `N05` | A01 gateway/persistence | #6 | gateway owner | integration | `NOT_IMPLEMENTED` |
| `N06` | A02 Android | #7 | Android owner | deterministic + physical | `NOT_IMPLEMENTED` |
| `N07` | A03 iOS | #8 | iOS owner | deterministic + physical | `NOT_IMPLEMENTED` |
| `N08` | A04 MCP | #9 | MCP owner | integration | `NOT_IMPLEMENTED` |
| `N09` | E01 evidence harness | #10 | evidence owner | adversarial/deterministic | `NOT_IMPLEMENTED` |
| `N10` | X01 protected DevOps E2E | #11 | E2E owner | integration | `NOT_IMPLEMENTED` |
| `N11` | final aggregate convergence | #12 | one D01 writer | exact-head multi-lane | `OPEN / BLOCKED` |
| `N12` | physical/security/legal/Human | #13 | external/Human authorities | physical/security/Human | `NOT_EXERCISED` |
| `N40` | bootstrap-main partial convergence | #40 | temporary aggregate writer | exact-head documentation | `IN_PROGRESS` |

## C01 subgraph

| Node | Issue | Purpose | Git relation | Current state |
|---|---:|---|---|---|
| `C01-K` | #18 | Kotlin canonical-vector candidate | sibling after frozen C01 | `PREPARATION_ONLY` |
| `C01-S` | #19 | Swift canonical-vector candidate | sibling after frozen C01 | `PREPARATION_ONLY` |
| `C01-T` | #20 | TypeScript canonical-vector candidate | sibling after frozen C01 | `PREPARATION_ONLY` |
| `C01-EP` | #37 / PR #38 | capability/schema/receipt/convergence preparation | true child of C01; process sibling of language candidates | `DRAFT_PREPARATION` |
| `C01-LP` | #39 | zero-placeholder clean-room Session packets | true child of PR #38; routing sibling | `READY_TO_PREPARE` |
| `C01-SH` | #26 | independent read-only Shadow | no writer / no Git parent | `NOT_EXERCISED` |
| `C01-CV` | #24 | semantic convergence and admission | one convergence owner | `BLOCKED_BY_WORKERS` |
| `K01-PREP` | #25/#28 | core packets and Shadow falsifiers | process successor after C01 | `BLOCKED_BY_C01_ADMISSION` |

## Start-readiness DAG

```text
N01 -> N02
N01 -> N02D
N01 + N02 -> N03

N03 -> C01-K
N03 -> C01-S
N03 -> C01-T
N03 -> C01-EP
C01-EP -> C01-LP

readable C01 plus stable port -> N06/N07 preparation only
C01-CV(C01_ADMITTED) -> N04
N04 -> N05/N08
N03 + N04 -> N09
N05 + N08 + N09 -> N10
selected admitted C/K/A/E/X -> N11
N11 -> N12
```

## Completion-readiness DAG

```text
N01 + N02 + N02D exact-main readback -> bootstrap-control/source checkpoint

C01-K receipt
+ C01-S receipt
+ C01-T receipt
+ exact schema/receipt evidence
+ C01-SH independent receipt
-> C01-CV

C01-CV == C01_ADMITTED
-> N04 completion may begin

N03 + N04 -> N05/N08/N09 completion
N03 -> deterministic part of N06/N07
N03 + N04 + N05 + N08 + N09 -> N10
selected admitted terminal receipts -> N11
N11 + required physical/security/legal/Human receipts -> N12
all required terminals + explicit Human admit -> N00
```

## Process and evidence dependencies

```text
D00 queue readability != local queue execution
toolchain presence != language-vector correctness
schema shape != signature/auth/replay correctness
same-context Shadow != independent Shadow
prompt packet != observed Session
bootstrap/profile PASS != provider/user/paid PASS
source disposition != technical implementation
```

## Convergence ownership

- Issue #40 is the single writer for this partial main reconciliation only.
- Issue #12 remains the final P7 aggregate owner.
- Issue #4/#24 remains the only C01 semantic convergence authority.
- Terminal C/K/A/E/X Workers do not update root README, AGENTS, Issue DAG or Molecular Stack index.

## Current terminal summary

```text
P0/C00              MERGED / eligible for issue closure at cloud-static ceiling
P1/S01              MERGED / eligible for issue closure at source-disposition ceiling
D00                  MERGED / queue execution NOT_EXERCISED
P2/C01               OPEN / DRAFT_PREPARATION
C01 language code    NOT_IMPLEMENTED
C01 independent SH   NOT_EXERCISED
P3-P6                NOT_IMPLEMENTED
P7 final             OPEN / BLOCKED
P8                   NOT_EXERCISED / HUMAN_ADMIT_REQUIRED
```

Issue UI state remains coordination metadata; exact Git and owning receipts determine closure.
