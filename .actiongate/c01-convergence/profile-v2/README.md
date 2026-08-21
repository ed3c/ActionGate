# C01 Profile-v2 Convergence Control

Issue #62. Parent dispatch: PR #61 at `2998b0a93d23ddfca0934250d82bdbd892f2c84b`.

This atom implements the deterministic control that sits **between** the external independent review (#26) and the sole semantic admission owner (#24). It does not perform the independent review and cannot self-emit final C01 admission.

## State Machine

```text
PROFILE_V2_SUBJECT_BOUND
  -> CONVERGENCE_CONTROL_VERIFIED
  -> BLOCKED_BY_INDEPENDENT_RECEIPT
  -> INDEPENDENT_RECEIPT_VALIDATED
  -> C01_DECISION_CANDIDATE_BOUND
  -> #24 C01_ADMITTED | HOLD | REJECT
```

The checked-in state stops at `BLOCKED_BY_INDEPENDENT_RECEIPT`.

## DAG

```text
C01 contract b63589e5a16e
       |
       +------ Kotlin cf589a0990aa -----+
       +------ Swift  039827061f54 -----+--> #26 external independent receipt
       +------ TS     3ed9f0307df0 -----+              |
       |                                               v
       +--> PR #61 profile-v2 dispatch 2998b0a93d23 --> Issue #62 validator
                                                       |
                                                       v
                                                candidate decision
                                                       |
                                                       v
                                                Issue #24 only
                                                       |
                                              C01_ADMITTED|HOLD|REJECT
```

#26 is a process/evidence dependency, not a Git parent. #62 is a true child of PR #61 because it consumes the profile-v2 dispatch contract.

## Directory ownership and data flow

| Path | Owner | Input | Output | Evidence ceiling |
|---|---|---|---|---|
| `convergence-registry.json` | #62 | exact PR #61/C01/Worker subjects | frozen convergence input registry | public/static |
| `independent-review.contract.json` | #62 | PR #61 review schema/registry | exact receipt expectations | public/static |
| `check_convergence.py` | #62 | registry + optional external receipt | refusal or candidate decision | deterministic control |
| `selftest.py` | #62 | planted mutations | 14/14 refusal denominator | deterministic control |
| `admission-decision.schema.json` | #62 | candidate decision | machine output contract | schema only |
| `phase-status.json` | #62 | current evidence | fail-closed state | public/static |
| `prompts/convergence-owner.md` | #62 | validated external receipt | zero-context #24 packet | routing only |

## Decision law

A candidate `C01_ADMITTED` can be derived only when all are true:

1. receipt schema is `actiongate-c01-independent-review-receipt/v2`;
2. it is not a template;
3. reviewer is a separate read-only context and did not build/repair the audited subjects or dispatch;
4. contract/common evidence and all three Worker subjects match the registry exactly;
5. the full 33-falsifier ID set is present exactly once;
6. independent verdict is `ELIGIBLE_FOR_C01_CONVERGENCE`;
7. every falsifier is `PASS`;
8. evidence ceiling remains C01 contract/language only.

Even then this atom returns a **candidate decision**. Issue #24 remains the sole semantic owner.

## Hard boundaries

```text
candidate C01_ADMITTED != automatic K01 start
C01 contract PASS       != Android/iOS hardware PASS
C01 contract PASS       != MCP enforcement PASS
same-context Shadow     != independent #26
schema-valid receipt    != trustworthy external reviewer
mergeable Draft         != merge/release/production
```

`k01_start_authorized`, `merge_authorized`, `release_authorized`, and `production_authorized` are fixed false in this atom.

## Current state

```text
structural convergence control   IMPLEMENTED_CANDIDATE
independent review #26            NOT_EXERCISED
C01 decision                      BLOCKED
C01_ADMITTED                      ABSENT
K01                               BLOCKED_BY_C01_ADMISSION
```
