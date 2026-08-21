# C01 Independent Shadow Dispatch

State: `C01_INDEPENDENT_SHADOW_DISPATCH_CANDIDATE`

This stacked atom refreshes the historical PR #41 launch preparation with the exact Shadow-hardened Kotlin, Swift and TypeScript subjects. It prepares a separate read-only reviewer to execute Issue #26. It does **not** perform that independent review.

## Stack relation

```text
PR #38 execution control
        ↓
PR #41 historical launch preparation
        ↓ true child
Issue #58 / this dispatch atom
        ├── read-only side input: PR #34 Kotlin
        ├── read-only side input: PR #35 Swift
        └── read-only side input: PR #36 TypeScript
        ↓
Issue #26 independent read-only reviewer
        ↓
Issue #24 sole C01 convergence owner
```

The three language PRs are routing siblings, not Git parents of this branch and not parents of one another.

## State Machine

```text
EXACT_SUBJECTS_BOUND
→ DISPATCH_CONTRACT_COMPILED
→ MUTATION_DENOMINATOR_PASS
→ EXACT_HEAD_HOSTED_PASS
→ EXTERNAL_INDEPENDENT_SESSION_READY
→ #26 ELIGIBLE_FOR_C01_CONVERGENCE | HOLD | REJECT
→ #24 C01_ADMITTED | HOLD | REJECT
```

This atom stops at `EXTERNAL_INDEPENDENT_SESSION_READY`.

## Exact immutable inputs

```text
C01 contract       b63589e5a16e82fda1a9554227f2ebbb55398c8a
execution control  9f41038240837ea2dd9dcdb9befd13e6ba81a78e
historical packet  98c9545c0dd2bbfdabdaf27c8a992822a78b3840

Kotlin current     511b26ad10389e0d0076f463f59f3a9c0e8a1b6e / tree 92d6e5affe027df8c6ea4a03cf0e49b756248ee3
Swift current      48bc9cf00105f40d5444542ddcdad85106f3c1d5 / tree 91458fe771874c3798edeedcaa2a3bde777bd14c
TypeScript current 6a99c61150d00be56c7eddf70eb9e3f423cfb7fa / tree 5c392c2e72bef44732617c13fd3d698fc4955594
```

Full source, metadata-receipt, tree and blob identities are in `dispatch-registry.json`.

## Data flow

```text
exact contract + common receipt gate
             ↓
three Shadow-hardened language subjects
             ↓
exact commit/tree/blob registry
             ↓
structural checker + planted mutation suite
             ↓
zero-placeholder independent-review prompt
             ↓
external Issue #26 receipt
             ↓
Issue #24 convergence
```

## Commands

```bash
python3 .actiongate/c01-shadow-dispatch/check_dispatch.py
python3 .actiongate/c01-shadow-dispatch/selftest.py
```

An external reviewer validates its completed receipt with:

```bash
python3 .actiongate/c01-shadow-dispatch/check_dispatch.py --review-receipt /absolute/path/to/review-receipt.json
```

## Evidence ceiling

A green dispatch checker proves only that the public packet is internally consistent and fail-closed on the exact declared subjects. It cannot prove reviewer independence, implementation correctness beyond the bound receipts, C01 admission, hardware/MCP behavior, legal clearance, merge, release or production.
