# Issue DAG

## Edge classes

- **start:** exact interface readable;
- **completion:** prerequisite receipt admitted in its own lane;
- **process/evidence:** runtime, Shadow, local, projection or Human receipt; no Git ancestry;
- **publication:** branch/PR published without implementation completion.

## Stage nodes

| Node | Issue | Atom | State |
|---|---:|---|---|
| N00 | #1 | Epic | OPEN |
| N01 | #2 | C00 | MERGED / CLOSED |
| N02 | #3 | S01 | MERGED / CLOSED |
| N02D | #2 | D00 | MERGED; queue not exercised |
| N03 | #4 | C01 | DRAFT_PREPARATION |
| N04 | #5 | K01 | BLOCKED_BY_C01_ADMISSION |
| N05 | #6 | A01 | NOT_IMPLEMENTED |
| N06 | #7 | A02 | NOT_IMPLEMENTED |
| N07 | #8 | A03 | NOT_IMPLEMENTED |
| N08 | #9 | A04 | NOT_IMPLEMENTED |
| N09 | #10 | E01 | NOT_IMPLEMENTED |
| N10 | #11 | X01 | NOT_IMPLEMENTED |
| N11 | #12 | final D01 | OPEN / BLOCKED |
| N12 | #13 | H01 | NOT_EXERCISED |
| N40 | #40 / PR #42 | partial main convergence | MERGED / CLOSED |
| N43 | #43 / PR #44 | PR #41 state delta | MERGED / CLOSED |

## C01 subgraph

| Node | Issue/PR | Relation | State |
|---|---|---|---|
| C01-K | #18/#34 | language sibling after frozen C01 | PREPARATION_ONLY |
| C01-S | #19/#35 | language sibling after frozen C01 | PREPARATION_ONLY |
| C01-T | #20/#36 | language sibling after frozen C01 | PREPARATION_ONLY |
| C01-EP | #37/#38 | true child of C01; process sibling of languages | DRAFT_PREPARATION |
| C01-LP | #39/#41 | true child of PR #38; routing sibling of languages | DRAFT_PUBLISHED / NOT_LAUNCHED |
| C01-SH | #26 | independent read-only; no Git parent | NOT_EXERCISED |
| C01-CV | #24 | one semantic convergence owner | BLOCKED_BY_WORKERS |
| K01-PREP | #25/#28 | process successor after C01 | BLOCKED_BY_C01_ADMISSION |

## Start DAG

```text
N01 -> N02/N02D/N03
N02 -> N03
N03 -> C01-K/C01-S/C01-T/C01-EP
C01-EP -> C01-LP
C01-LP -> fresh Kotlin/Swift/TypeScript Sessions
C01-CV(C01_ADMITTED) -> N04
N04 -> N05/N08
N03 -> N06/N07 preparation
N03 + N04 -> N09
N05 + N08 + N09 -> N10
N10 -> N11
N06 + N07 + N11 -> N12
```

## Completion DAG

```text
Kotlin receipt
+ Swift receipt
+ TypeScript receipt
+ exact schema/receipt evidence
+ independent C01-SH receipt
-> C01-CV

C01-CV == C01_ADMITTED -> N04
N03 + N04 -> N05/N08/N09
N03 + N04 + N05 + N08 + N09 -> N10
N10 -> N11
N11 + required physical/security/legal/Human receipts -> N12
all required terminals + Human admit -> N00
```

## Non-substitution laws

```text
queue contract != queue execution
toolchain presence != vector correctness
PR #41 packet/request != Session observed
Agent cannot fabricate Human clean-room declaration
schema shape != signature/auth/replay correctness
same-context Shadow != independent Shadow
source disposition != implementation
bootstrap/profile PASS != provider/user/paid PASS
```

## Convergence ownership

- #24: C01 semantic admission;
- #12: final repository convergence;
- terminal Workers do not update aggregate README/AGENTS/DAG/Stack.

## Current summary

```text
P0/P1               MERGED / CLOSED at declared ceilings
D00                  MERGED / execution NOT_EXERCISED
C01 contract         DRAFT_PREPARATION
C01 execution prep   PR #38 DRAFT
C01 launch prep      #39 CLOSED_PREP_ONLY / PR #41 DRAFT / NOT_LAUNCHED
C01 language code    NOT_IMPLEMENTED
C01 independent SH   NOT_EXERCISED
P3-P6                NOT_IMPLEMENTED
P7 final             OPEN / BLOCKED
P8                   NOT_EXERCISED / HUMAN_ADMIT_REQUIRED
```
