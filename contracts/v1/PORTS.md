# Contract-to-Implementation Ports

C01 defines data and semantic obligations, not concrete frameworks.

```text
Canonicalizer
  canonical_bytes(value)
  hash_arguments(value)
  hash_action(ActionEnvelope)
  challenge_signing_input(AuthorizationChallenge)

Clock
  now_ms()

NonceSource
  next_nonce()

PolicyPort
  classify(action)
  current_policy_version()

HardwareSigner (platform adapter)
  key_id()
  sign_challenge(signing_input) -> P1363 signature

IntegrityProvider (platform adapter)
  produce_integrity_proof(challenge) -> ApplicationIntegrityProof

ProofVerifier (server adapter)
  verify_hardware(proof, challenge)
  verify_integrity(proof, challenge)

DeviceKeyRegistry
  resolve(device_id, key_id)

ChallengeRepository
  issue / consume / expire

GrantRepository
  mint / consume / replay-check

IdempotencyRepository
  reserve / commit / reconcile

AuditOutbox
  append receipt event

ProtectedActionExecutor
  execute(action_id, idempotency_key, grant)
```

## Ownership split

| Port | First owner |
|---|---|
| Canonicalizer / semantic validators | K01 with C01 vectors |
| PolicyPort | K01 |
| registries/repositories/verifier/outbox | A01 |
| Android HardwareSigner / IntegrityProvider | A02 |
| iOS HardwareSigner / IntegrityProvider | A03 |
| protected MCP boundary / grant presentation | A04 |
| falsifiers for every port | E01 |

No adapter may widen C01 semantics. If a platform requires a different wire representation, conversion stays inside that adapter and the canonical contract remains unchanged or C01 is explicitly versioned.
