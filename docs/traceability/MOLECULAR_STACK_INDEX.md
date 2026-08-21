# Molecular Stack Index

Dependency is derived from consumed unmerged bytes/contracts, not chronology or branch names. A Draft being mergeable is not semantic admission. Review-only Shadow is never a Git parent.

## Relation vocabulary

```text
SIBLING
TRUE_CHILD
CONVERGENCE
PROCESS_DEPENDENCY
EXTERNAL_EVIDENCE
HISTORICAL
```

## Integrated main lineage

| Atom | Class | Issue | PR | Merge commit | Evidence ceiling |
|---|---|---:|---:|---|---|
| C00 | C/D | #2 | #14 | `fee8c290061542bfb93e27ddcc33cce7fbf8c653` | cloud/static |
| S01 | C/E | #3 | #15 | `8810fe41f66ad1b4fe80db5f93bf9539e2a38899` | source disposition |
| D00 | D | #2 | #16 | `76efa9297d147712bb9dfbb9e797d69ca9432a99` | prompt/handoff contract |
| D00-MAIN | D | #40 | #42 | `71796b8c4d50fdfbcade85f9bbdf4d3ec988ba99` | exact-main docs |
| D00-DELTA | D | #43 | #44 | `53f1014e4c75a0083c8ebe2972e8f52f3ff33b9d` | state reconciliation |
| D00-FINALIZE | D | #45 | #46 | `70573aed229404772827829a1ce069a6e72184fa` | aggregate finalization |

## Current C01 molecular stack

| Atom | Class | Issue | PR | Exact head | True relation | Disposition |
|---|---|---:|---:|---|---|---|
| C01 | C | #4 | #17 | `b63589e5a16e82fda1a9554227f2ebbb55398c8a` | consumes S01 constraints | `KEEP_DRAFT / NOT_ADMITTED` |
| C01-K | C/E | #18 CLOSED | #34 | `cf589a0990aaaa6422be9c649b52b44230d570f6` | `SIBLING` | profile-hardened local-deterministic candidate; keep Draft |
| C01-S | C/E | #19 CLOSED | #35 | `039827061f54aa72e2b81365a4c904d25833f83e` | `SIBLING` | profile-hardened local-deterministic candidate; keep Draft |
| C01-T | C/E | #20 CLOSED | #36 | `3ed9f0307df0937028bbf52fe8fbd2a6621acafe` | `SIBLING` | profile-hardened local-deterministic candidate; keep Draft |
| C01-EXEC | D/E | #37 CLOSED | #38 CLOSED | `9f41038240837ea2dd9dcdb9befd13e6ba81a78e` | `HISTORICAL` | completed preparation; closed unmerged; exact commit retained |
| C01-LAUNCH | D | #39 CLOSED | #41 CLOSED | `98c9545c0dd2bbfdabdaf27c8a992822a78b3840` | `HISTORICAL` | completed launch preparation; closed unmerged |
| C01-SH-v1 | D/E | #58 | #59 CLOSED | `ce57d5db1e71223f18d1095024297391a36611f3` | `HISTORICAL` | hosted-green but stale after #57 |
| C01-SH-v2 | D/E | #60 CLOSED | #61 | `2998b0a93d23ddfca0934250d82bdbd892f2c84b` | `TRUE_CHILD` superseding dispatch epoch | hosted-green external review packet; keep Draft |
| C01-SH | E/H | #26 | n/a | n/a | `EXTERNAL_EVIDENCE` | NOT_EXERCISED |
| C01-CV-CTRL | D/E | #62 CLOSED | #63 | `e4196305284b4751286b01f5d1d33e82fc34af0b` | `TRUE_CHILD` of #61 | fail-closed convergence control; keep Draft |
| C01-CV | X/D | #24 | n/a | n/a | `CONVERGENCE` | BLOCKED_BY_#26 |
| K01-PREP | D | #25/#28 | n/a | n/a | `PROCESS_DEPENDENCY` | BLOCKED_BY_C01_ADMISSION |

### C01 ordering as a dependency graph

```text
                    C01 / PR #17
                  /       |       \
        PR #34 Kotlin  PR #35 Swift  PR #36 TypeScript
                  \       |       /
                   \      |      /
                  #60 / PR #61
                   profile-v2 dispatch
                         |
                         +---- EXTERNAL_EVIDENCE ----> #26
                         |
                         +---- TRUE_CHILD -----------> #62 / PR #63
                                                      convergence control
                                   #26 receipt ---------+
                                                       |
                                                       v
                                                  #24 CONVERGENCE
                                                       |
                                                C01_ADMITTED only
                                                       v
                                                   #25/#28
```

PR #38/#41/#59 remain exact historical provenance but are not active admission parents.

## PRV01 provenance stack

| Atom | Class | Issue | PR | Exact head | Relation | Disposition |
|---|---|---:|---:|---|---|---|
| PRV01 | C/E | #53 | #54 | `d9716d029578608b6179c56def6f7ea8c3728146` | parallel governance candidate from main | KEEP DRAFT |
| PRV01-SH | E/H | #55 | n/a | n/a | `EXTERNAL_EVIDENCE` | NOT_EXERCISED |
| PRV01-CV | D | #56 | n/a | n/a | `CONVERGENCE` after independent admission + merge | BLOCKED |
| PV02 | C/E | #51 | n/a | n/a | downstream upstream-selection lane | OPEN / NOT_ADMITTED |

PR #54 cannot merge from hosted deterministic evidence alone. It requires Issue #55 independent admission and an explicit Human merge decision.

## Downstream product atoms

| Atom | Issue | Prerequisite | State |
|---|---:|---|---|
| K01 | #5 | exact `C01_ADMITTED` | BLOCKED |
| A01 | #6 | admitted C01 + K01 | NOT_IMPLEMENTED |
| A02 | #7 | admitted C01 + stable core port | NOT_IMPLEMENTED |
| A03 | #8 | admitted C01 + stable core port | NOT_IMPLEMENTED |
| A04 | #9 | admitted C01 + K01 | NOT_IMPLEMENTED |
| E01 | #10 | admitted C01 + K01 | NOT_IMPLEMENTED |
| X01 | #11 | admitted C/K/A/E | NOT_IMPLEMENTED |
| D01 | #12 | selected admitted terminal set | OPEN / BLOCKED |
| H01 | #13 | immutable D01 candidate + external lane entries | NOT_EXERCISED |

## Closure and merge policy

### Safe closed leaf/process subjects

```text
Issues #18 #19 #20
  completed at local-deterministic profile-hardened ceiling

PR #38
  closed unmerged as HISTORICAL_PROCESS_EVIDENCE

PR #41
  closed unmerged as HISTORICAL_LAUNCH_PREPARATION

PR #59
  already closed unmerged as superseded stale-profile dispatch
```

### Keep Draft/open

```text
#17 contract oracle
#34/#35/#36 current language candidates
#54 PRV01 provenance candidate
#61 current profile-v2 independent-review dispatch
#63 current fail-closed convergence control
```

None of those should be merged merely because the PR is mergeable.

## Receipt-staleness law

If an audited subject moves:

```text
old green receipt
-> HISTORICAL
-> explicit superseding epoch
-> re-bind exact commit/tree/blob denominator
-> re-run owning verification
```

Do not rewrite or silently reuse stale evidence.
