# C01 Swift Canonicalization Worker

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
restricted Swift/Foundation value model
        ↓
explicit ASCII-key sorting + UTF-8 JSON encoding
        ↓
pure Swift SHA-256 + Foundation base64url
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
src/ActionGateCanonical.swift
  restricted conversion, canonical JSON, pure Swift SHA-256, duplicate-key parser

tests/main.swift
  three positive hashes, ordering, NSNumber bool/number, float/range/key/type/duplicate/Unicode controls

run.sh
  no-download Swift compile and test lane
```

## Deterministic command

```bash
./run.sh
```

No Secure Enclave, LocalAuthentication, App Attest, hardware key, MCP, persistence or product implementation is present. A local green run is not independent review, C01 admission, hardware, integration, security, merge or release evidence.
