# C01 Swift Canonicalization Worker

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
restricted Swift value model + validator
        ↓
explicit ASCII-key sort + UTF-8 canonical bytes
        ↓
SHA-256 + base64url domain hashes
        ↓
positive and negative vector tests
        ↓
contracts/impl/swift/receipt.json
        ↓
Issue #24 C01 convergence
```

## DAG relation

This branch is a path-disjoint sibling of Kotlin and TypeScript. It consumes the same immutable C01 subject and never consumes their unmerged bytes.

## Toolchain gate

Capability-only command:

```bash
swift --version
```

Absence is `BLOCKED_ABSENT_EXECUTABLE`. No installer or package download is authorized. Exact build/test commands are frozen before first implementation green and recorded in the receipt.

## Expected implementation surface

```text
Package.swift
Sources/ActionGateC01/
Tests/ActionGateC01Tests/
receipt.json
```

The Swift package must declare no external dependency unless separately admitted. Preparation files do not count as implementation evidence.
