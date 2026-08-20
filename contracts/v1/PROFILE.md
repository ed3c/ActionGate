# ActionGate v1 Canonical Contract Profile

Status: C01 candidate for Draft review.

## 1. Selection

V1 selects **RFC 8785 JCS with a stricter ActionGate data profile** rather than deterministic CBOR as the default wire-signing representation.

Reason: ActionGate V0 already crosses JSON/MCP boundaries. A restricted JCS profile keeps the first contract reviewable while removing floating-point and dynamic non-ASCII-key ambiguity. RFC 8949 deterministic CBOR remains a documented alternative, not a V1 dependency.

This is a design decision, not evidence that JCS is universally superior.

## 2. Canonical value profile

Before canonicalization, reject values outside:

```text
null
boolean
integer in [-9007199254740991, 9007199254740991]
valid Unicode string
array of canonical values
object:
  keys match ^[A-Za-z0-9_.:-]+$
  values are canonical values
```

Additional rules:

```text
duplicate object key      -> REJECT
float / exponent number   -> REJECT
NaN / Infinity            -> REJECT
lone surrogate            -> REJECT
Unicode normalization     -> FORBIDDEN
unknown schema field      -> REJECT where additionalProperties=false
```

The ASCII-key restriction is ActionGate-specific. String **values** may contain Unicode and are preserved without normalization.

## 3. Hash domains

All domain labels are exact ASCII bytes including the trailing NUL.

```text
arguments_hash =
  base64url_no_pad(
    SHA-256(
      "ActionGate-Arguments-v1\0" ||
      JCS_PROFILE(tool_arguments)
    )
  )

action_digest =
  base64url_no_pad(
    SHA-256(
      "ActionGate-ActionEnvelope-v1\0" ||
      JCS_PROFILE(ActionEnvelope)
    )
  )

authorization_signing_input =
  "ActionGate-AuthorizationChallenge-v1\0" ||
  JCS_PROFILE(AuthorizationChallenge)
```

Reference fixture values:

```text
arguments_hash  = aDAZpSSDV7-lNqYY5ViQqqUTcU8J6m-qPpFu4QjfTUk
action_digest   = XD8ngJ-f1tD-cwVWTuqFWCCPuwTjAVyzV63rtNgW89c
sha256(signing_input) = 8sC8JA9BcBFHT9swpU81Y5EuI3bvTxzxQKYVIWTFdkw
```

`sha256(signing_input)` is published only as a test vector. A platform API that accepts message bytes must sign `authorization_signing_input` and perform SHA-256 exactly once as part of ES256. A digest-signing API must sign exactly `SHA-256(authorization_signing_input)`. Do not hash twice.

## 4. Hardware signature profile

```text
curve             P-256 / secp256r1
signature alg     ES256 (ECDSA with SHA-256)
wire format       IEEE-P1363
wire bytes        R(32) || S(32)
text encoding     base64url without padding
```

Android providers that return ASN.1 DER ECDSA convert DER -> P1363 inside the Android adapter after signing. iOS adapters expose the equivalent 64-byte representation. The private key is never exported for conversion.

## 5. Separation of controls

```text
HardwareSignatureProof
  proves possession/use of enrolled signing key under adapter policy

ApplicationIntegrityProof
  carries provider-specific app/device integrity evidence

VerificationResult
  records authoritative server decision over both lanes

ExecutionGrant
  binds the verified exact action to the protected tool
```

A schema-valid proof is not a cryptographically valid proof. Provider verification remains an adapter responsibility.

## 6. ExecutionGrant authenticity

The V1 grant schema freezes claims and one-time identity, but intentionally does **not** select JWT/JWS/PASETO or another token container.

A04/A01 must authenticate the grant at the protected boundary through either:

- a cryptographically authenticated grant container bound to these claims; or
- a mutually authenticated/trusted internal channel that resolves `grant_id` to authoritative server state.

Raw JSON matching the schema is never sufficient authorization.

## 7. Time and freshness

Time fields are Unix epoch milliseconds encoded as integers within the profile range.

Semantic laws, enforced outside JSON Schema:

```text
expires_at_ms > issued_at_ms
challenge/action/grant TTL is policy bounded
policy_version must equal the active accepted version at verification
nonce/grant IDs are single-use under their owning state machines
```

## 8. Compatibility

`version = "actiongate/v1"` is required on every public envelope.

Unknown fields are rejected in V1. A new security-relevant field or semantic change requires a new explicit profile/version. Readers must not silently reinterpret a V1 document under a newer policy.

## 9. Evidence boundary

The Python reference under `reference/verify_vectors.py` proves only the frozen restricted profile fixtures and negative controls on that runtime. It does not prove:

```text
full generic RFC 8785 implementation
Kotlin/Swift/TypeScript parity
JSON-Schema engine parity
Android Keystore / StrongBox
Apple Secure Enclave
Play Integrity / App Attest
server signature verification
MCP integration
```

Those lanes must close separately.
