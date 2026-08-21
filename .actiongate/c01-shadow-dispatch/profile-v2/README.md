# C01 Profile-Hardened Independent Shadow Dispatch

State: `C01_PROFILE_HARDENED_SHADOW_DISPATCH_READY_FOR_EXTERNAL_REVIEW`

This directory supersedes the Issue #58 / PR #59 independent-review packet after Issue #57 moved all three audited language subjects. The old packet remains historical provenance and is not rewritten or reused.

## Immutable graph

```text
C01 contract b63589e5...
        │
        ├── Kotlin PR #34 @ cf589a09...
        ├── Swift PR #35 @ 03982706...
        └── TypeScript PR #36 @ 3ed9f030...
                    │
                    ▼
Issue #60 profile-v2 dispatch
                    │
                    ▼
external separate read-only Issue #26 reviewer
                    │
                    ▼
Issue #24 C01 convergence
```

The three language candidates are path-disjoint siblings. The dispatch branch is a child of PR #59; it is not a parent of any language implementation.

## State Machine

```text
STALE_DISPATCH_DETECTED
→ PROFILE_SUBJECTS_BOUND
→ VERSIONED_DISPATCH_COMPILED
→ MUTATION_DENOMINATOR_PASS
→ EXACT_HEAD_HOSTED_PASS
→ EXTERNAL_INDEPENDENT_SESSION_READY
→ #26 ELIGIBLE_FOR_C01_CONVERGENCE | HOLD | REJECT
→ #24 C01_ADMITTED | HOLD | REJECT
```

The dispatch and hosted validation are complete. Current state ends before independent review.

## Data flow

```text
Issue #57 exact commits/trees/blobs
        ↓
dispatch-registry.json
        ↓
check_dispatch.py + selftest.py
        ↓
exact-head GitHub workflow
        ↓
DISPATCH_RECEIPT.json
        ↓
external independent-review prompt + fail-closed template
        ↓
Issue #26 public-safe receipt
        ↓
Issue #24 convergence
```

## Falsifier denominator

The packet retains all Issue #58 controls and adds profile-hardening controls for:

```text
registered domain allowlist
unknown/embedded-NUL domain rejection
raw ASCII key profile
fraction/exponent rejection
positive/negative unsafe integer rejection
safe integer boundaries
negative-zero acceptance
```

## Deterministic checks

```bash
python3 .actiongate/c01-shadow-dispatch/profile-v2/check_dispatch.py
python3 .actiongate/c01-shadow-dispatch/profile-v2/selftest.py
python3 .actiongate/c01-shadow-dispatch/profile-v2/check_ready_binding.py
```

These commands prove dispatch consistency only. They do not execute Issue #26, emit `C01_ADMITTED`, start K01, or authorize merge/release.
