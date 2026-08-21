# C01 TypeScript Canonicalization Worker

Status: `IMPLEMENTATION_CANDIDATE_LOCAL_DETERMINISTIC`; independent Shadow and C01 convergence remain separate.

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

The implementation wave reached `SHADOW_READBACK` on the local deterministic lane. The durable receipt is added in a successor evidence commit and binds the implementation candidate subject immediately before that receipt commit.

## Data flow

```text
read-only C01 profile/schema/vectors
        ↓
restricted TypeScript value validator
        ↓
explicit key sorting + UTF-8 JSON encoding
        ↓
Node built-in SHA-256 + base64url
        ↓
positive vectors + negative controls
        ↓
RECEIPT.json
        ↓
Issue #26 independent Shadow
        ↓
Issue #24 C01 convergence
```

## Implementation surface

```text
src/actionGateCanonical.ts
  restricted validation, canonical JSON, hashing, raw duplicate-key parser

tests/test.ts
  three positive hashes, ordering, float/range/key/type/duplicate/surrogate/Unicode controls

tsconfig.json + run.sh
  no-download TypeScript compile and Node test lane
```

## Deterministic command

```bash
./run.sh
```

No MCP SDK, protected-tool middleware, mobile, persistence or product implementation is present. A local green run is not independent review, C01 admission, hardware, integration, security, merge or release evidence.
