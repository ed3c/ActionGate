# Contracts

Owner: `C01` / Issue #4.

`contracts/v1/` is the language-neutral ActionGate contract plane. It freezes the canonicalization profile, required security envelopes, hash/signature binding rules, compatibility policy, and positive/mutation vectors before K01/A01–A04 implementation begins.

```text
tool arguments
  -> ActionGate restricted JCS profile
  -> arguments_hash
  -> ActionEnvelope
  -> action_digest
  -> AuthorizationChallenge
  -> hardware signing input
  -> HardwareSignatureProof + ApplicationIntegrityProof
  -> VerificationResult
  -> one-time ExecutionGrant
  -> protected side effect
  -> AuditReceipt
```

The contract plane does not implement HTTP, persistence, MCP, Android, iOS, or business logic.

Current evidence ceiling: contract design + Python reference vectors only. Kotlin/Swift/TypeScript reproduction, JSON-Schema execution, hardware/platform behavior, integration, and physical-device lanes remain independently unexercised until receipts exist.
