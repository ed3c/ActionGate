# C01 Kotlin Canonicalization Worker

Status: `PREIMPLEMENTATION_READY`; implementation and runtime evidence are `NOT_EXERCISED`.

## State Machine

```text
DISPATCH_BOUND
→ TOOLCHAIN_PROBED
→ IMPLEMENTATION_PLAN_FROZEN
→ CANONICALIZER_IMPLEMENTED
→ POSITIVE_VECTORS_VERIFIED
→ NEGATIVE_CONTROLS_VERIFIED
→ SHADOW_READBACK
→ DRAFT_CANDIDATE
```

A later state requires its own exact-subject receipt.

## Data flow

```text
read-only contracts/v1 profile/schema/vectors
        ↓
restricted Kotlin value model + validator
        ↓
explicit key sort + UTF-8 canonical bytes
        ↓
SHA-256 + base64url domain hashes
        ↓
positive and negative vector runner
        ↓
contracts/impl/kotlin/receipt.json
        ↓
Issue #24 C01 convergence
```

## DAG relation

This branch is a path-disjoint sibling of Swift and TypeScript. It consumes the same immutable C01 subject and never consumes their unmerged bytes.

## Toolchain gate

Capability-only commands:

```bash
kotlinc -version
java -version
```

Absence is `BLOCKED_ABSENT_EXECUTABLE`. No installer or dependency download is authorized. Exact compile/test commands are frozen by the Worker before first implementation green and recorded in the receipt.

## Expected implementation surface

```text
src/                 Kotlin restricted canonicalizer and vector runner
tests/               owned positive/negative controls
run.sh               deterministic no-download command lane
receipt.json         exact-subject result after execution
```

Preparation files do not count as implementation evidence.
