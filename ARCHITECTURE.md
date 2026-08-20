# ActionGate Technical Architecture

## 1. Objective

Separate probabilistic agent planning from deterministic authority to execute protected actions.

The architecture is evaluated against one narrow invariant:

> An `R3` protected tool cannot execute through the compliant path without a fresh authorization proof bound to the exact canonical action, intended audience, current policy, enrolled subject/device, and single-use execution state.

This does not claim to eliminate prompt injection or prove that a user understood an action.

## 2. Trust and authority realms

| Realm | Owner | Trusted inputs | Untrusted inputs | State | Authority | Failure blast radius |
|---|---|---|---|---|---|---|
| Planner | agent runtime | model/tool schemas | retrieved content, prompts, model output | plan/session | propose only | malformed or malicious action proposal |
| Policy core | ActionGate domain core | canonical action and versioned policy | planner metadata | risk decision | classify, never execute | incorrect tier or policy mismatch |
| Challenge gateway | ActionGate service | policy result and registry | network/device response | challenge, nonce, TTL | issue challenge | replay or orphaned challenge |
| Mobile approval endpoint | enrolled app/device | server challenge, human presence | compromised UI/app environment | key handle and approval state | sign exact digest only | invalid user-presence ceremony or device compromise |
| Verification plane | ActionGate verifier | canonical contract, enrolled public key, integrity verifier | proof envelope | verification result | mint eligibility only | false acceptance or false denial |
| Grant plane | ActionGate core/persistence | verified result and replay state | duplicate/concurrent calls | one-time grant | authorize exact tool/audience | duplicate or stale grant |
| Protected tool | business service | valid ExecutionGrant | direct calls, planner tokens | idempotency/result | perform side effect | protected business mutation |
| Audit/outbox | durable persistence | action/grant/tool result | tampered or missing events | append-only receipt state | evidence publication | incomplete or misleading audit trail |

## 3. Boundary crossings

For every crossing, duplication, reordering, delay, loss, replay, partial success, timeout after unknown completion, and version mismatch are first-class states.

```text
Planner proposal
-> canonical ActionEnvelope
-> policy classification
-> challenge
-> user-presence hardware proof + integrity evidence
-> verification
-> one-time ExecutionGrant
-> protected side effect
-> durable audit receipt
```

Authentication, authorization, hardware signing, and application/device integrity are separate controls.

## 4. Domain state machine

```text
PROPOSED
-> CLASSIFIED
-> CHALLENGE_REQUIRED | DIRECTLY_SCOPED

CHALLENGE_REQUIRED
-> CHALLENGE_ISSUED
-> APPROVED | DENIED | EXPIRED | CANCELLED

APPROVED
-> PROOF_VERIFIED
-> GRANT_MINTED
-> GRANT_CONSUMED
-> SIDE_EFFECT_PENDING
-> SIDE_EFFECT_COMMITTED | COMMIT_UNKNOWN | SIDE_EFFECT_FAILED
-> RECEIPT_RECORDED

COMMIT_UNKNOWN
-> RECONCILING
-> SIDE_EFFECT_COMMITTED | SIDE_EFFECT_FAILED | MANUAL_REVIEW_REQUIRED
```

Illegal transitions fail closed. A retry never creates a second irreversible side effect for the same `action_id`.

## 5. Canonical contracts

The P2 contract atom will version at least:

```text
ActionEnvelope
AuthorizationChallenge
HardwareSignatureProof
ApplicationIntegrityProof
VerificationResult
ExecutionGrant
AuditReceipt
LocalHandoffPacket
```

Raw ambiguous JSON is never signed. Canonicalization, hash algorithm, field presence, audience, subject, agent, tool, parameters hash, policy version, nonce, issued time, and expiry are explicit and covered by cross-language vectors.

## 6. Persistence and consistency

Gateway process memory is not the source of truth.

Authoritative persisted state includes:

```text
device/key registry
policy versions
challenge/nonce TTL
consumed grant IDs
idempotency records
side-effect reconciliation state
transactional audit outbox
```

The selected storage/queue technology remains a candidate until exact revision, license, operational semantics, and failure tests are admitted.

## 7. Adapter boundaries

```text
Core ports
├── ProofVerifier
├── IntegrityVerifier
├── ChallengeRepository
├── GrantRepository
├── PolicyRepository
├── IdempotencyRepository
├── AuditOutbox
└── ProtectedActionExecutor
```

Android, iOS, MCP, HTTP, persistence, and business-service implementations are adapters. Platform private keys never cross into shared C++/KMP/native heaps.

## 8. Failure obligations

At minimum verify:

```text
modified parameters after approval
wrong audience/resource/tenant
stale policy
expired challenge
nonce replay
grant replay
concurrent duplicate request
direct protected-tool bypass
cancelled biometric
key invalidation/rotation
attestation/verifier outage
process crash before/after side effect
process crash before/after outbox commit
audit tampering or loss
secret leakage into logs/traces
```

## 9. Evidence ladder

```text
L0 source claim
L1 static reasoning
L2 deterministic unit/property proof
L3 local integration evidence
L4 real substrate/device evidence
L5 adversarial/security evidence
L6 production observation
```

No evidence promotes itself across subject, revision, environment, or lane.

## 10. Technology-selection law

A technology candidate is admitted only after the repository records:

```text
exact repository and revision
license and NOTICE obligations
commercial-use compatibility
security/update posture
owned invariants versus delegated invariants
failure/operational burden
replacement/exit path
reproducible verification
```

Library presence is not capability. A permissive license is not proof of employer-IP clearance, security correctness, or production fitness.