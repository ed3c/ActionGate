# AGENTS.md — C01 Swift Vector Worker

Scope: `contracts/impl/swift/**` for Issue #19 only.

## Exact dispatch

```text
repository  ed3c/ActionGate
base        ag/C01-action-contracts@b63589e5a16e82fda1a9554227f2ebbb55398c8a
branch      ag/C01-swift-vectors
lease       contracts/impl/swift/**
relation    SIBLING_AFTER_SCHEMA_FREEZE
evidence    local-deterministic canonicalization only
```

## Read order

1. root `AGENTS.md`
2. `contracts/AGENTS.md`
3. `contracts/v1/PROFILE.md`
4. `contracts/v1/DECISIONS.md`
5. `contracts/v1/actiongate-contracts.schema.json`
6. `contracts/v1/vectors.json`
7. Issue #19 and PR #17 exact head
8. `TASK_PACKET.json`
9. `SHADOW_PREFLIGHT.json`

## Hard laws

- `contracts/v1/**` is immutable input. Any disagreement is `BLOCKED_CONTRACT_DIVERGENCE` and returns to #4.
- Write only inside this directory.
- Reject floating point, out-of-range integers, invalid object keys, lone surrogates and unsupported values before canonicalization.
- Do not rely on Swift `Dictionary` iteration order.
- Preserve the distinction between JSON booleans and numeric `NSNumber` values when using Foundation.
- Encode strings explicitly as UTF-8 and do not normalize Unicode values.
- Prefer Swift standard library, Foundation and CryptoKit; no third-party package without exact rights admission.
- Do not implement Secure Enclave, LocalAuthentication, App Attest, MCP, persistence or product logic.
- Toolchain presence and `swift test` exit zero do not prove another evidence lane.

## Shadow checkpoints

```text
toolchain capability
Foundation number/bool model selected
first canonical byte match
first hash match
first negative-control green
parser/Unicode discrepancy
before Draft PR update
```

Block oracle edits, lease widening, package downloads, silent Unicode normalization, float acceptance, bool/number confusion, stale base use or evidence promotion.

## Stop conditions

```text
wrong base SHA
overlapping writer
missing exact Issue/task packet
Swift toolchain unavailable
contract divergence
unadmitted dependency
failed positive vector
negative control missing from denominator
private/employer context contamination
Human-owned operation
```

Merge, release, semantic contract changes and security/legal acceptance remain Human-owned.
