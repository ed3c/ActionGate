# C01 Decisions and Deferred Choices

## Selected for V1

- Canonical representation: RFC 8785 JCS narrowed by `PROFILE.md`.
- Canonical numeric profile: signed integers only, ±(2^53-1); floating point rejected.
- Dynamic canonical object keys: ASCII profile `^[A-Za-z0-9_.:-]+$`.
- Digest: SHA-256, base64url without padding.
- Hardware signature: P-256 / ES256.
- Portable signature wire encoding: IEEE-P1363 64-byte `R || S`.
- Security controls remain separate: signature proof, application/device integrity proof, verification result, execution grant.

## Explicitly deferred

- JWT/JWS/PASETO or other ExecutionGrant container.
- Specific JSON-Schema runtime/library.
- Kotlin/Swift/TypeScript canonicalizer package choice.
- Android DER-to-P1363 implementation library versus minimal adapter conversion.
- iOS signature conversion helper.
- MCP SDK release pin.
- Persistence and replay technology.
- On-device model runtime.

Deferred choices may not be silently decided by downstream workers. The owning issue must either consume the frozen port or reopen/version C01.

## Rejected as V1 defaults

- Raw non-canonical JSON signing.
- Floating-point values in security-bound canonical inputs.
- Cross-platform private-key export.
- Treating schema validity as cryptographic authorization.
- Treating deterministic CBOR as an implied dependency merely because RFC 8949 is an admitted alternative source.
