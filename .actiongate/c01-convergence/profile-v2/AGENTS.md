# AGENTS.md — C01 Profile-v2 Convergence Control

## Scope

This file governs only `.actiongate/c01-convergence/profile-v2/**` and the dedicated workflow `.github/workflows/c01-convergence-control.yml` when Issue #62 is active.

## Mandatory read route

1. root `AGENTS.md`;
2. Issue #62;
3. Issue #24 (sole C01 semantic convergence authority);
4. Issue #26 (independent read-only evidence owner);
5. Issue #60 / Draft PR #61 exact profile-v2 dispatch subject;
6. this directory `README.md`, `convergence-registry.json`, `independent-review.contract.json`, `phase-status.json`;
7. exact Worker PR #34/#35/#36 heads/trees and receipts named in the registry.

## Authority

This atom may implement and verify a **convergence-control mechanism**. It may validate a receipt created by a separate Issue #26 reviewer and derive a candidate decision packet for Issue #24.

It must never:

- act as the Issue #26 independent reviewer;
- fabricate or infer an external review receipt;
- emit the final Issue #24 verdict on its own authority;
- mutate `contracts/v1/**` or any language Worker implementation;
- start K01 merely because a decision candidate is `C01_ADMITTED`;
- claim Android/iOS hardware, MCP, security/legal, merge, release or production evidence.

## Exact bound subjects

```text
base / PR #61     2998b0a93d23ddfca0934250d82bdbd892f2c84b
base tree         e535e6fa031c84697d9b0b5cb96ee90a64286a08
contract epoch    b63589e5a16e82fda1a9554227f2ebbb55398c8a
common evidence   9f41038240837ea2dd9dcdb9befd13e6ba81a78e
Kotlin            cf589a0990aaaa6422be9c649b52b44230d570f6
Swift             039827061f54aa72e2b81365a4c904d25833f83e
TypeScript        3ed9f0307df0937028bbf52fe8fbd2a6621acafe
```

Any subject drift is a typed blocker. Do not silently rebind.

## State Machine

```text
PROFILE_V2_SUBJECT_BOUND
→ CONVERGENCE_CONTROL_VERIFIED
→ BLOCKED_BY_INDEPENDENT_RECEIPT
→ INDEPENDENT_RECEIPT_VALIDATED
→ C01_DECISION_CANDIDATE_BOUND
→ Issue #24 final decision
```

This Builder context stops at `BLOCKED_BY_INDEPENDENT_RECEIPT` unless a genuine external Issue #26 receipt exists.

## Receipt law

A valid external receipt must:

- use `actiongate-c01-independent-review-receipt/v2`;
- set `template=false`;
- bind Issue #26, dispatch Issue #60 / PR #61, and dispatch epoch `23ee1763bea2703f732482952b6312d751faf8cb`;
- prove separate-context, read-only reviewer status with no audited-subject implementation/repair participation;
- bind the exact contract/common/Worker subjects;
- contain exactly the required 33 unique falsifiers;
- use only `PASS | FAIL | NOT_EXERCISED`;
- contain 33/33 `PASS` before `ELIGIBLE_FOR_C01_CONVERGENCE` can be accepted;
- preserve the exact evidence ceiling and Human-owned merge boundary.

A schema-shaped or same-context receipt is not sufficient.

## Admission law

The controller may derive:

```text
ELIGIBLE_FOR_C01_CONVERGENCE -> candidate C01_ADMITTED
HOLD                         -> candidate HOLD
REJECT                       -> candidate REJECT
```

Only Issue #24 owns the semantic decision. Even an admitted C01 only makes K01 completion work eligible; it does not authorize K01 start, merge, release or production.

## Shadow monitor

The same-context Shadow is read-only and records `INDEPENDENCE_NOT_CLAIMED`. It blocks:

```text
missing independent receipt
same-context review
review subject drift
wrong contract/worker subject
falsifier denominator shrinkage
NOT_EXERCISED promoted to admission
HOLD/REJECT promoted to C01_ADMITTED
private locator/secret-shaped content
evidence widening to hardware/MCP/security/legal
implicit K01 start
implicit merge/release/production
stale profile dispatch reuse
```

## Stop conditions

Stop and return a typed blocker on any drift, malformed receipt, missing evidence, private locator, semantic conflict, authority widening, or Human-owned operation.
