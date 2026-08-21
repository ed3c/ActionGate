# C01 TypeScript Canonicalization Worker

Status: `SHADOW_HARDENED_LOCAL_DETERMINISTIC`; independent Shadow #26 and C01 convergence #24 remain separate.

## State Machine

```text
C01_CONTRACT_BOUND
→ LANGUAGE_IMPLEMENTED
→ FROZEN_VECTORS_PASS
→ COMMON_NEGATIVE_DENOMINATOR_PASS
→ SHADOW_HARDENING_REPAIRED
→ SUCCESSOR_RECEIPT
→ INDEPENDENT_SHADOW_PENDING
```

## Data flow

```text
frozen C01 profile/schema/vectors
        ↓
restricted TypeScript value adapter
        ↓
canonical UTF-8 JSON + exact ASCII domain bytes
        ↓
SHA-256 / base64url vectors
        ↓
common 3-positive + 7-negative receipt
        ↓
extra Shadow hardening controls
        ↓
Issue #26 independent review
        ↓
Issue #24 C01 convergence
```

## Hardened surface

```text
src/actionGateCanonical.ts, tests/test.ts
```

Hardening under Issue #49 adds:

- escaped duplicate-key equivalence
- raw surrogate-pair acceptance
- raw lone-surrogate rejection
- non-ASCII domain rejection
- missing-NUL rejection
- cyclic-container rejection
- sparse-array rejection
- accessor rejection
- symbol-key rejection
- leading-zero grammar rejection

Run:

```bash
./run.sh
```

The exact hardened source/test blobs are recorded in `SHADOW_IMPLEMENTATION.receipt.json`. The final `RECEIPT.json` is a successor evidence commit that binds the immediately preceding implementation metadata subject.

No Android/iOS hardware, MCP, persistence, independent-security, merge or release claim is made.
