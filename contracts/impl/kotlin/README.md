# C01 Kotlin Canonicalization Worker

Status: `PROFILE_HARDENED_CANDIDATE_LOCAL_DETERMINISTIC`; independent Shadow and C01 convergence remain separate.

## Exact candidate

```text
base contract  b63589e5a16e82fda1a9554227f2ebbb55398c8a
source head    0247eb1fc7201b51aded66f2c2311aa42f9ca83c
source tree    15a27f2d9dbaacdfbea57dc1cd37e4af284b09dc
issue          #18 / #47 / #49 / #57
lease          contracts/impl/kotlin/**
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
structured Kotlin/JDK value
        ↓
restricted value validation + cycle detection
        ↓
explicit ASCII-key sorting + UTF-8 JSON
        ↓
exact registered domain label + SHA-256
        ↓
three frozen hashes

raw JSON bytes
        ↓
assertCanonicalJsonInput
        ├─ duplicate and ASCII-key validation
        ├─ Unicode/surrogate validation
        └─ integer-only syntax + ±(2^53−1) bound
        ↓
approved generic JSON parsing boundary
```

## Verification

```bash
bash contracts/impl/kotlin/run.sh
```

Observed controls include the frozen 3-positive/7-negative denominator plus unknown/embedded-NUL domain rejection, raw non-ASCII-key rejection, fraction/exponent rejection, unsafe raw-integer rejection, safe boundary acceptance, cycle rejection and raw Unicode controls.

No Android, JNI, NDK, hardware key, MCP, persistence or product implementation is present. Same-context Shadow is not independent review. Merge, release and security/legal acceptance remain Human-owned.
