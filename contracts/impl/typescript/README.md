# C01 TypeScript Canonicalization Worker

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

## Data flow

```text
read-only contracts/v1 profile/schema/vectors
        ↓
restricted TypeScript value model + validator
        ↓
explicit key sort + UTF-8 canonical bytes
        ↓
Node built-in SHA-256 + base64url hashes
        ↓
positive and negative vector runner
        ↓
contracts/impl/typescript/receipt.json
        ↓
Issue #24 C01 convergence
```

## DAG relation

This branch is a path-disjoint sibling of Kotlin and Swift. It consumes the same immutable C01 subject and never consumes their unmerged bytes.

## Toolchain gate

Capability-only commands:

```bash
node --version
tsc --version
```

Absence is `BLOCKED_ABSENT_EXECUTABLE`. No `npm install`, `npx` download or other installer is authorized. Exact compile/test commands are frozen before first implementation green and recorded in the receipt.

## Expected implementation surface

```text
package.json          scripts only; no external dependency
tsconfig.json
src/
tests/
receipt.json
```

Preparation files do not count as implementation evidence.
