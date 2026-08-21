# C01 Swift Canonicalization Worker

Status: `PROFILE_HARDENED_CANDIDATE_LOCAL_DETERMINISTIC`; independent Shadow and C01 convergence remain separate.

## Exact candidate

```text
base contract  b63589e5a16e82fda1a9554227f2ebbb55398c8a
source head    2f089d45056fd783f57f3458dc739f33a49304c7
source tree    684275693783c379b134bd499a7dcddeb1f0b34c
issue          #19 / #47 / #49 / #57
lease          contracts/impl/swift/**
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
structured Swift/Foundation value
        ↓
restricted conversion + mutable-container boundary
        ↓
explicit ASCII-key sorting + UTF-8 JSON
        ↓
exact registered domain label + reference SHA-256
        ↓
three frozen hashes

raw JSON bytes
        ↓
assertCanonicalJsonInput
        ├─ duplicate and ASCII-key validation
        ├─ escaped-surrogate validation
        └─ integer-only syntax + ±(2^53−1) bound
        ↓
approved generic JSON parsing boundary
```

## Verification

```bash
bash contracts/impl/swift/run.sh
```

Observed controls include the frozen 3-positive/7-negative denominator, SHA-256 known-answer vectors, exact-domain rejection, raw non-ASCII-key rejection, fraction/exponent rejection, unsafe raw-integer rejection, safe boundary acceptance and existing mutable-container/Unicode controls.

No Secure Enclave, LocalAuthentication, App Attest, hardware key, MCP, persistence or product implementation is present. The pure-Swift SHA-256 is a C01 reference lane, not a production provider selection. Same-context Shadow is not independent review.
