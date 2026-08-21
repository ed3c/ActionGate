# AGENTS.md — C01 Kotlin Vector Worker

Scope: `contracts/impl/kotlin/**` for Issue #18 only.

## Exact dispatch

```text
repository  ed3c/ActionGate
base        ag/C01-action-contracts@b63589e5a16e82fda1a9554227f2ebbb55398c8a
branch      ag/C01-kotlin-vectors
lease       contracts/impl/kotlin/**
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
7. Issue #18 and PR #17 exact head
8. `TASK_PACKET.json`
9. `SHADOW_PREFLIGHT.json`

## Hard laws

- `contracts/v1/**` is immutable input. Any disagreement is `BLOCKED_CONTRACT_DIVERGENCE` and returns to #4.
- Write only inside this directory.
- Reject floating point, out-of-range integers, invalid object keys, lone surrogates and unsupported values before canonicalization.
- Sort object keys explicitly; never rely on map iteration order.
- Encode strings explicitly as UTF-8 and do not normalize Unicode values.
- Prefer Kotlin/JDK built-ins; no dependency download or package addition without exact rights admission.
- Do not implement Android Keystore, JNI/NDK, MCP, persistence, product logic or private-key handling.
- A toolchain or process exit proves neither vector parity nor another evidence lane.

## Shadow checkpoints

```text
toolchain capability
first canonical byte match
first hash match
first negative-control green
parser/number/Unicode discrepancy
before Draft PR update
```

Block oracle edits, lease widening, hidden dependency downloads, silent Unicode normalization, float acceptance, stale base use or evidence promotion.

## Stop conditions

```text
wrong base SHA
overlapping writer
missing exact Issue/task packet
kotlinc or JVM unavailable
contract divergence
unadmitted dependency
failed positive vector
negative control missing from denominator
private/employer context contamination
Human-owned operation
```

Merge, release, semantic contract changes and security/legal acceptance remain Human-owned.
