# C01 TypeScript Canonicalization Worker

Status: `PROFILE_HARDENED_CANDIDATE_LOCAL_DETERMINISTIC`; independent Shadow and C01 convergence remain separate.

## Exact candidate

```text
base contract  b63589e5a16e82fda1a9554227f2ebbb55398c8a
source head    dbdcfdcd8f100c3135730bc828700ffc8239994e
source tree    39a40aab9f13fdcae04d3164669667aa7322029c
issue          #20 / #47 / #49 / #57
lease          contracts/impl/typescript/**
```

## State Machine

```text
DISPATCH_BOUND
→ TOOLCHAIN_PROBED
→ CANONICALIZER_IMPLEMENTED
→ POSITIVE_VECTORS_VERIFIED
→ NEGATIVE_CONTROLS_VERIFIED
→ SHADOW_HARDENED
→ RAW_PROFILE_HARDENED
→ DRAFT_CANDIDATE
```

The current local-deterministic lane reached `RAW_PROFILE_HARDENED`. A successor receipt binds the metadata candidate immediately before the receipt commit.

## Data flow

```text
structured Node/TypeScript value
        ↓
restricted descriptor/prototype/cycle validation
        ↓
explicit ASCII-key sorting + UTF-8 JSON
        ↓
exact registered domain label + Node SHA-256
        ↓
three frozen hashes

raw JSON bytes
        ↓
assertCanonicalJsonInput
        ├─ duplicate and ASCII-key validation
        ├─ surrogate validation
        └─ integer-only syntax + ±(2^53−1) bound
        ↓
approved generic JSON parsing boundary
```

## Verification

```bash
bash contracts/impl/typescript/run.sh
```

Observed controls include the frozen 3-positive/7-negative denominator plus exact-domain, raw non-ASCII-key, fraction/exponent, unsafe raw-integer and safe-boundary controls. Existing cycle, sparse-array, accessor, symbol-key and Unicode controls remain active.

No npm install, npx, MCP SDK, mobile, persistence or product implementation is present. Same-context Shadow is not independent review. Merge, release and security/legal acceptance remain Human-owned.
