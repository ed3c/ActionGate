# AGENTS.md — ActionGate Contract Plane

Scope: `contracts/**` for `P2 / C01` only.

## Read order

1. root `AGENTS.md`
2. root `ARCHITECTURE.md`
3. `docs/sources/SOURCE_MANIFEST.md`
4. `docs/sources/CLAIM_LEDGER.md`
5. Issue #4
6. this file
7. `v1/PROFILE.md`
8. `v1/actiongate-contracts.schema.json`
9. `v1/vectors.json`

## Authority

C01 owns language-neutral wire/domain contracts and deterministic vectors. It does not own HTTP, persistence, MCP SDK code, Android/iOS APIs, business actions, or aggregate repository indexes.

The contract plane may narrow RFC 8785 with an ActionGate profile. It must not claim that an RFC, schema file, or Python reference proves Kotlin/Swift/TypeScript interoperability. Cross-language reproduction is a separate evidence lane.

## Hard laws

- Never sign ambiguous raw JSON.
- Security-critical field names are ASCII and exact.
- V1 canonical values use null, boolean, signed integers within ±(2^53-1), strings, arrays, and objects whose keys match the profile. Floating-point values are forbidden.
- Unicode string values are preserved byte-for-byte after valid Unicode decoding; do not normalize.
- Duplicate JSON object keys and lone surrogates are rejected.
- Hashes use SHA-256 and base64url without padding.
- Domain separation is mandatory for arguments, ActionEnvelope, and AuthorizationChallenge signing input.
- ES256 wire signatures are IEEE-P1363 `R || S` (64 bytes). Platform adapters may convert DER locally, but private keys never leave the platform keystore.
- Authentication, authorization, hardware signing, and application/device integrity are separate contracts.
- ExecutionGrant authenticity is an adapter/trust-channel requirement; raw grant JSON is never trusted merely because it matches schema.
- Queue/handoff contracts do not authorize merge, release, production, or physical claims.

## Writer law

One C01 schema/interface owner freezes the profile. Serializer/vector workers may start only after that subject is readable. They own language-local implementations and may not mutate this contract plane without a new C01 revision.

## Exit

C01 preparation is stage-complete when the combined schema, profile, reference vectors, mutation controls, task contract, and same-context Shadow preflight are published on an exact Draft PR head. P2 itself remains incomplete until independent cross-language reproduction and owning assertions close the required evidence.
