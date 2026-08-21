# Problem Closure Matrix

## Purpose

This matrix compares the uploaded article/PDF claims and the repository's technical objectives with the highest evidence actually earned.

Source presence does not prove a claim. A rejected overclaim may be closed at the **source-disposition** lane while its underlying technical problem remains open.

## Evidence ladder

```text
SOURCE_DISPOSITION
-> CONTRACT_DEFINED
-> LOCAL_DETERMINISTIC_VERIFIED
-> INTEGRATION_VERIFIED
-> LIVE_PHYSICAL_VERIFIED
-> INDEPENDENT_SECURITY_ADMITTED
-> USER_OBSERVED
-> PAID_OBSERVED
-> HUMAN_RELEASE_ADMITTED
```

No cheaper rung substitutes for a later rung.

## Matrix

| ID | Source problem or claim | Repository disposition | Owning mechanism / Issue | Highest earned evidence | Closure |
|---|---|---|---|---|---|
| `PC-001` | Mobile UI/VLM coordinate error causes unreliable actions | Valid source problem but outside ActionGate V0's authorization boundary; structured OS/tool APIs are preferred where available | future UI/action adapter, not currently owned | source statement only | `OPEN / OUT_OF_SCOPE_FOR_V0` |
| `PC-002` | Continuous screen/audio context creates PII leakage risk | Valid concern; public/private documentation controls do not implement runtime PII minimization | future edge/context component; E01 privacy controls | governance only | `OPEN` |
| `PC-003` | Cloud-only model use creates cost/latency dependence | Product architecture hypothesis; on-device inference is optional and deferred for V0 | optional Phase-2 runtime adapters | source/candidate only | `OPEN / DEFERRED` |
| `PC-004` | Planner compromise must not grant protected execution authority | Admitted security requirement | #4, #5, #9, #11 | C01 Draft preparation | `OPEN` |
| `PC-005` | R3 approval must bind exact parameters, subject, audience, policy, nonce and expiry | Admitted contract requirement | #4 / PR #17 | Draft schema/profile preparation; parity not run | `OPEN` |
| `PC-006` | Authentication, authorization, hardware signing, integrity and user presence are different controls | Admitted design law | #4, #7, #8, #10 | source + Draft contract separation | `OPEN` |
| `PC-007` | A fully stateless MCP gateway is sufficient | Rejected architecture contradiction; authoritative replay/device/policy/audit state is required | #5/#6/#9/#10 | design requirement only | `REJECTED_CLAIM`; mechanism open |
| `PC-008` | `llama.cpp + GGUF + KMP` is the universal/YC-standard best practice | Rejected as a universal claim; optional candidate only | S01 candidate ledger | merged source disposition | `CLOSED_AS_REJECTED_OVERCLAIM` |
| `PC-009` | Shared GGUF guarantees 100% identical cross-platform output | Unsupported absolute claim; exact serializer/model/runtime evidence would be required | future inference eval | no implementation evidence | `OPEN / UNVERIFIED` |
| `PC-010` | Hardware gates neutralize 100% of unauthorized prompt-injected actions | Rejected absolute claim; only a narrow compliant-path invariant is testable | #10/#11 | no E2E implementation | `CLOSED_AS_REJECTED_OVERCLAIM`; invariant open |
| `PC-011` | 40% TTFT improvement, 35+ tokens/sec, 85% device coverage, or similar figures | Unsupported in the supplied source for this repository; no benchmark subject/environment | future benchmark owner | absent | `OPEN / EXCLUDED_FROM_CLAIMS` |
| `PC-012` | Agentic coding tools raise productivity by 60–80% | Unsupported generalization; no controlled experiment | Productization evidence lane, not ActionGate core | absent | `OPEN / EXCLUDED_FROM_CLAIMS` |
| `PC-013` | ActionGate is an uncontested blue ocean and has no competitors | Unsupported market claim; public technical repo does not own market truth | private Productization market/user lanes | absent | `OPEN / REJECTED_AS_FACT` |
| `PC-014` | Emulator/simulator proves StrongBox, Secure Enclave, Play Integrity or App Attest | Rejected evidence substitution | #7/#8/#13 | physical lanes not exercised | `CLOSED_AS_REJECTED_INFERENCE`; physical proof open |
| `PC-015` | Private keys should enter NDK/C++/KMP memory for portability | Rejected boundary; platform key stores retain private keys | #7/#8 | design requirement only | `CLOSED_AS_REJECTED_DESIGN`; adapters open |
| `PC-016` | Permissive OSS automatically clears employer IP, patent, confidentiality and legal risk | Rejected; clean-room provenance and Human legal admission remain separate | #3/#13 and clean-room handoffs | source/rights procedure merged | `CLOSED_AS_REJECTED_OVERCLAIM`; legal lane open |
| `PC-017` | Exact dependency license and commercial suitability are known from repository reputation/latest branch | Rejected; exact revision, LICENSE/NOTICE, SBOM and replacement path required | #3 | candidates only; none admitted | `OPEN` |
| `PC-018` | Cross-language ActionEnvelope/Challenge bytes and hashes are reproducible | Required C01 exit condition | #18/#19/#20/#23/#24 | Worker preparation only | `OPEN` |
| `PC-019` | Replay, duplicate requests and unknown commit state cannot cause duplicate effects | Required distributed-system invariant | #5/#6/#10/#11 | not implemented | `OPEN` |
| `PC-020` | MCP protected tool cannot be called directly or with altered/replayed grant | Required enforcement invariant | #9/#10/#11 | not implemented | `OPEN` |
| `PC-021` | Android hardware signing, biometric and Play Integrity work on real devices | Required physical evidence | #7/#13 | not exercised | `OPEN` |
| `PC-022` | iOS Secure Enclave, LocalAuthentication and App Attest work on real devices | Required physical evidence | #8/#13 | not exercised | `OPEN` |
| `PC-023` | The implementation is independently secure and clean-room/legal admissible | Separate independent/Human evidence | #13 plus #26 for C01 | not exercised / Human required | `OPEN` |
| `PC-024` | The product creates user value, payment and repeatable commercial demand | External Productization evidence, not technical inference | skills-shared Productization + ActionGate #21 | not exercised | `OPEN` |

## Closed at this checkpoint

Only these classes are closed:

```text
unsupported claim rejected
evidence-substitution rejected
universal stack claim rejected
private/public authority boundary established
source/rights/candidate routing established
prompt/handoff contract established
```

## Not closed

```text
C01 cross-language admission
K01 domain core
A01-A04 adapters
E01 adversarial evidence
X01 E2E canary
physical Android/iOS
independent security
clean-room/legal admission
user value
payment
release
production
```

## Reopen law

Any new source, platform revision, dependency revision, contract epoch, benchmark environment or exact implementation subject may reopen the relevant row. Historical dispositions are retained rather than rewritten.
