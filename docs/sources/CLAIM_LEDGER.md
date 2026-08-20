# Technical Claim Ledger

## Claim classes

```text
FACT
SOURCE_STATEMENT
DESIGN_REQUIREMENT
DESIGN_PROPOSAL
INFERENCE
HYPOTHESIS
ASSUMPTION
CONTRADICTION
UNKNOWN
REJECTED_OVERCLAIM
```

A source statement is not a measured fact. A proposed architecture is not implementation. A library or API is not an exercised capability.

## Current claims

| ID | Claim | Class | Required evidence | Current disposition |
|---|---|---|---|---|
| `CLM-001` | The planner is outside the trusted authorization boundary. | DESIGN_REQUIREMENT | architecture contract + bypass tests | `ADMITTED_AS_REQUIREMENT` |
| `CLM-002` | An R3 proof must bind exact canonical action parameters, audience, subject, policy version, nonce and expiry. | DESIGN_REQUIREMENT | P2 schemas + cross-language mutation vectors | `BLOCKED_ON_C01` |
| `CLM-003` | Authentication, authorization, hardware signing and app/device integrity are separate controls. | DESIGN_REQUIREMENT | contract separation + negative integration tests | `BLOCKED_ON_C01/E01` |
| `CLM-004` | Gateway processes may be stateless while replay/device/key/policy/audit state remains persisted. | DESIGN_PROPOSAL | restart, replay and reconciliation tests | `BLOCKED_ON_A01/E01` |
| `CLM-005` | A compromised planner can generate a syntactically valid tool call but cannot execute a protected tool without a valid grant. | HYPOTHESIS | direct-bypass and compromised-planner E2E canary | `BLOCKED_ON_X01` |
| `CLM-006` | Android StrongBox/TEE, biometric and Play Integrity behavior is proven by emulator/static tests. | CONTRADICTION | physical-device receipt | `REJECTED` |
| `CLM-007` | iOS Secure Enclave, Face ID/Touch ID and App Attest behavior is proven by simulator/static tests. | CONTRADICTION | physical-device receipt | `REJECTED` |
| `CLM-008` | Private signing keys should be exported into NDK/C++/KMP memory to simplify portability. | CONTRADICTION | platform key-boundary review | `REJECTED` |
| `CLM-009` | A fully stateless MCP authorization gateway needs no nonce/grant/device registry. | CONTRADICTION | replay/restart test | `REJECTED` |
| `CLM-010` | ActionGate prevents all prompt injection. | REJECTED_OVERCLAIM | impossible under declared scope; only narrow execution invariant is testable | `REJECTED` |
| `CLM-011` | Hardware signing proves the user understood the displayed action. | REJECTED_OVERCLAIM | human-factors evidence would still not create semantic certainty | `REJECTED` |
| `CLM-012` | `llama.cpp + GGUF + KMP` is the universal best implementation choice. | REJECTED_OVERCLAIM | per-platform capability/performance/coverage evaluation | `REJECTED_AS_UNIVERSAL`; optional candidate only |
| `CLM-013` | Permissive open-source licensing alone clears employer-IP, confidentiality and patent risk. | CONTRADICTION | clean-room/legal review | `REJECTED` |
| `CLM-014` | A green CI run proves physical-device, security, legal, user-value or production acceptance. | CONTRADICTION | own-lane receipts | `REJECTED` |
| `CLM-015` | The technical MVP can begin without an on-device SLM. | DESIGN_PROPOSAL | protected-action canary acceptance | `ADMITTED_FOR_V0` |
| `CLM-016` | The first E2E should use a non-financial protected DevOps action. | DESIGN_PROPOSAL | Issue #11 acceptance | `ADMITTED_FOR_V0` |

## Negative controls

The source-admission worker must reject or preserve as unverified:

```text
title/snippet-only evidence
multiple citations that share one origin
unsupported latency, throughput or accuracy numbers
unsupported market-scarcity or “blue ocean” claims
unsupported 60%-80% productivity claims
license inferred from reputation, package index text or repository description
latest-branch license treated as a pinned release license
“open source” treated as equivalent to permissive/commercially unrestricted
```

## Closure rule

Each admitted claim binds:

```text
claim ID
exact wording
class
source locator/digest/freshness
subject/revision/environment
falsifier or oracle
evidence lane
terminal disposition
```

Claims not required for the technical implementation remain private or excluded.