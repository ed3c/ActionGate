# Molecular Stack Index

Dependency is derived from consumed unmerged bytes/contracts—not chronology or branch names. Draft/mergeable is not verified. Review-only Shadow is never a Git parent.

## Merged

| Atom | Class | Issue | PR | Merge commit | Relation | Evidence ceiling |
|---|---|---:|---:|---|---|---|
| C00 | C/D | #2 | #14 | `fee8c290061542bfb93e27ddcc33cce7fbf8c653` | top-level | cloud/static |
| S01 | C/E | #3 | #15 | `8810fe41f66ad1b4fe80db5f93bf9539e2a38899` | consumed C00; sibling to D00 | source disposition |
| D00 | D | #2 | #16 | `76efa9297d147712bb9dfbb9e797d69ca9432a99` | consumed C00; sibling to S01 | queue contract |
| D00-MAIN | D | #40 | #42 | `71796b8c4d50fdfbcade85f9bbdf4d3ec988ba99` | partial exact-main convergence | cloud/static |
| D00-DELTA | D | #43 | #44 | `53f1014e4c75a0083c8ebe2972e8f52f3ff33b9d` | late PR #41 state reconciliation | cloud/static |

## Active C01 Stack — keep Draft/open

| Atom | Class | Issue | PR | Head | True relation | State |
|---|---|---:|---:|---|---|---|
| C01 | C | #4 | #17 | `b63589e5a16e82fda1a9554227f2ebbb55398c8a` | consumed S01 constraints | not admitted |
| C01-K | C/E | #18 | #34 | `0136936e7d63ba0c538d2cb40db60409107ababc` | language sibling | preparation only |
| C01-S | C/E | #19 | #35 | `76b10b5a05898410ed361761626b381158edb306` | language sibling | preparation only |
| C01-T | C/E | #20 | #36 | `c62e24ffa0ceb2224fe6931929bfaeeceabe3c39` | language sibling | preparation only |
| C01-EP | D/E | #37 | #38 | `9f41038240837ea2dd9dcdb9befd13e6ba81a78e` | true child of C01; process sibling of languages | preparation only |
| C01-LP | D | #39 | #41 | `98c9545c0dd2bbfdabdaf27c8a992822a78b3840` | true child of PR #38; routing sibling of languages | packets ready; Sessions not launched |
| C01-SH | E/H | #26 | absent | absent | independent read-only | not exercised |
| C01-CV | X/D | #24 | absent | absent | one semantic convergence owner | blocked by receipts |

## Admission law

```text
language prep != implementation
toolchain presence != vector parity
launch packet/request != Session observed
schema validity != authorization
same-context Shadow != independent Shadow
mergeable Draft != C01_ADMITTED
```

Only #24 emits `C01_ADMITTED | HOLD | REJECT`.

## Downstream

| Atom | Issue | Prerequisite | State |
|---|---:|---|---|
| K01 | #5 | C01_ADMITTED | BLOCKED |
| A01 | #6 | C01 + K01 | NOT_IMPLEMENTED |
| A02 | #7 | C01 + stable port | NOT_IMPLEMENTED |
| A03 | #8 | C01 + stable port | NOT_IMPLEMENTED |
| A04 | #9 | C01 + K01 | NOT_IMPLEMENTED |
| E01 | #10 | C01 + K01 | NOT_IMPLEMENTED |
| X01 | #11 | admitted C/K/A/E | NOT_IMPLEMENTED |
| D01 | #12 | admitted terminal set | OPEN/BLOCKED |
| H01 | #13 | immutable D01 candidate | NOT_EXERCISED |

Parent movement invalidates affected receipts. Preserve old candidates and issue explicit replay/supersession decisions; do not silently rewrite non-empty Worker history.
