# AGENTS.md — C01 TypeScript Vector Worker

Scope: `contracts/impl/typescript/**` for Issue #20 only.

## Exact dispatch

```text
repository  ed3c/ActionGate
base        ag/C01-action-contracts@b63589e5a16e82fda1a9554227f2ebbb55398c8a
branch      ag/C01-typescript-vectors
lease       contracts/impl/typescript/**
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
7. Issue #20 and PR #17 exact head
8. `TASK_PACKET.json`
9. `SHADOW_PREFLIGHT.json`

## Hard laws

- `contracts/v1/**` is immutable input. Any disagreement is `BLOCKED_CONTRACT_DIVERGENCE` and returns to #4.
- Write only inside this directory.
- Reject floats and non-safe integers before canonicalization; do not trust generic JavaScript `number` values.
- Sort object keys explicitly; never rely on insertion order or default `JSON.stringify` semantics.
- Encode strings explicitly as UTF-8 and do not normalize Unicode values.
- `JSON.parse` discards duplicate-key evidence. Implement a raw-token check or keep that control unclosed with a reason; never report it PASS by inference.
- Prefer Node and TypeScript runtime built-ins. No `npm install`, `npx` download or third-party package without exact rights admission.
- Do not implement MCP middleware, mobile, persistence or product logic.
- Toolchain presence and process exit zero prove neither vector parity nor another evidence lane.

## Shadow checkpoints

```text
toolchain capability
raw JSON duplicate-key strategy
first canonical byte match
first hash match
first negative-control green
number/Unicode discrepancy
before Draft PR update
```

Block oracle edits, lease widening, hidden downloads, float/unsafe-integer acceptance, duplicate-key evidence laundering, stale base use or evidence promotion.

## Stop conditions

```text
wrong base SHA
overlapping writer
missing exact Issue/task packet
node or tsc unavailable
contract divergence
unadmitted dependency
failed positive vector
negative control missing from denominator
private/employer context contamination
Human-owned operation
```

Merge, release, semantic contract changes and security/legal acceptance remain Human-owned.
