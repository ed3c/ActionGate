# Problem Closure Matrix

## Purpose

This matrix compares the article/PDF/repository architecture claims with the highest evidence ActionGate has actually earned.

A rejected overclaim can be closed at the source-disposition lane while the underlying engineering problem remains open.

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

| ID | Problem / claim | Current repository disposition | Owner | Highest earned evidence | Closure |
|---|---|---|---|---|---|
| `PC-001` | Mobile UI/VLM coordinate error causes unreliable actions | Valid source problem; structured OS/tool APIs preferred; not ActionGate V0 authorization core | future UI/action adapter | source disposition | `OPEN / OUT_OF_SCOPE_FOR_V0` |
| `PC-002` | Continuous mobile context can leak PII | Valid; public/private repo controls do not implement runtime PII minimization | future context/privacy lane + E01 | governance only | `OPEN` |
| `PC-003` | Cloud-only LLM creates cost/latency dependence | Product architecture hypothesis; on-device inference remains optional/deferred for V0 | optional later runtime | source/candidate | `OPEN / DEFERRED` |
| `PC-004` | Planner compromise must not grant protected execution | Core invariant admitted | #4/#5/#9/#11 | contract defined; enforcement not implemented | `OPEN` |
| `PC-005` | R3 action must bind parameters/subject/audience/policy/nonce/expiry | Contract requirement admitted | #4/#18-#20/#24 | cross-language local-deterministic profile verified; independent admission pending | `PARTIAL / #26+#24 OPEN` |
| `PC-006` | Authentication, authorization, hardware signing, integrity, user presence are distinct | Design law admitted | #4/#7/#8/#10 | contract separation | `PARTIAL`; adapters open |
| `PC-007` | Fully stateless MCP gateway is sufficient | Rejected contradiction; replay/device/policy/audit state is authoritative | #5/#6/#9/#10 | design requirement | `CLOSED_AS_REJECTED_CLAIM`; mechanism open |
| `PC-008` | `llama.cpp + GGUF + KMP` is universal/YC-standard best practice | Unsupported universal claim; optional candidate only | source ledger | merged source disposition | `CLOSED_AS_REJECTED_OVERCLAIM` |
| `PC-009` | Shared GGUF guarantees identical cross-platform model output | Unsupported absolute claim | future inference eval | none | `OPEN / UNVERIFIED` |
| `PC-010` | Hardware gate prevents 100% of prompt-injected unauthorized actions | Absolute claim rejected; narrow compliant-path invariant remains testable | #10/#11 | no E2E enforcement evidence | `CLOSED_AS_REJECTED_OVERCLAIM`; invariant open |
| `PC-011` | Fixed TTFT/tokens-sec/device-coverage numbers | Unsupported for current exact benchmark subject/environment | benchmark owner | absent | `OPEN / EXCLUDED_FROM_CLAIMS` |
| `PC-012` | Agentic coding improves productivity by 60–80% | Unsupported generalization | productization evidence | absent | `OPEN / EXCLUDED_FROM_CLAIMS` |
| `PC-013` | ActionGate is uncontested blue ocean | Unsupported market fact; private market/user lane owns this | productization | absent | `OPEN / REJECTED_AS_FACT` |
| `PC-014` | Emulator/simulator proves StrongBox/Secure Enclave/Play Integrity/App Attest | Evidence substitution rejected | #7/#8/#13 | physical lanes absent | `CLOSED_AS_REJECTED_INFERENCE`; physical proof open |
| `PC-015` | Private keys should enter NDK/C++/KMP memory for portability | Rejected boundary; platform stores retain private key | #7/#8 | contract/design law | `CLOSED_AS_REJECTED_DESIGN`; adapter proof open |
| `PC-016` | Permissive OSS automatically clears employer/IP/legal risk | Rejected; provenance + private Human/legal admission separate | PRV01/#13 | public fail-closed provenance control candidate | `CLOSED_AS_REJECTED_OVERCLAIM`; legal lane open |
| `PC-017` | Dependency commercial suitability is known from repo reputation/latest | Rejected; exact revision/LICENSE/NOTICE/SBOM/replacement path required | #3/#51/PRV01 | source candidate + control plane | `OPEN` |
| `PC-018` | Cross-language ActionEnvelope/Challenge bytes and hashes are reproducible | Implemented in Kotlin/Swift/TypeScript and profile-hardened | #18/#19/#20/#23/#26/#24 | `LOCAL_DETERMINISTIC_VERIFIED`; 3/3 hashes + fixed denominator per language | `PARTIAL`; independent #26 and admission #24 open |
| `PC-019` | Raw canonical input has one consistent key/number/domain profile | Exact domain allowlist, ASCII raw keys, integer-only safe range, duplicate/Unicode/container controls implemented | #49/#57 + PR #34/#35/#36 | local-deterministic profile hardening | `CLOSED_AT_LOCAL_DETERMINISTIC_CEILING`; independent admission open |
| `PC-020` | Stale green review packets cannot be reused after subject movement | Old #59 packet quarantined; #60/#61 superseding profile-v2 epoch binds current subjects | #60/#61 | hosted exact-head dispatch verification | `CLOSED_FOR_DISPATCH_MECHANISM`; independent review itself open |
| `PC-021` | C01 convergence must fail closed without an independent receipt | #62/#63 validator/control implemented; `C01_ADMITTED` impossible without valid #26 receipt | #62/#63/#24 | hosted deterministic control | `CLOSED_FOR_CONTROL_MECHANISM`; #26/#24 open |
| `PC-022` | Replay, duplicate requests and unknown commit state cannot cause duplicate effects | Required distributed invariant | #5/#6/#10/#11 | not implemented | `OPEN` |
| `PC-023` | MCP protected tool resists direct bypass/altered/replayed grant | Required enforcement invariant | #9/#10/#11 | not implemented | `OPEN` |
| `PC-024` | Android hardware signing, biometric, Play Integrity work on real devices | Required physical lane | #7/#13 | not exercised | `OPEN` |
| `PC-025` | iOS Secure Enclave, LocalAuthentication, App Attest work on real devices | Required physical lane | #8/#13 | not exercised | `OPEN` |
| `PC-026` | C01 implementation is independently reviewed | profile-v2 packet and 33-falsifier denominator ready | #26 / PR #61 | dispatch hosted-green, review absent | `OPEN / ACTIVE_EXTERNAL_HANDOFF` |
| `PC-027` | Public upstream/source relationships are fail-closed and auditable | PRV01 control candidate implemented with hosted deterministic tests | #53/#54/#55/#56 | static provenance control candidate | `PARTIAL`; independent #55 + merge open |
| `PC-028` | Future product code is independently clean-room/legal admissible | Separate public provenance and private Human/legal lanes required | #13/#51/#55 | not independently admitted | `OPEN` |
| `PC-029` | Product creates user value, payment, repeatable demand | External productization evidence, not technical inference | ActionGate #21 + skills-shared productization | not exercised | `OPEN` |
| `PC-030` | Release/production is justified by technical green checks | Rejected substitution; exact release candidate, independent/security/legal/Human gates required | #12/#13 | not reached | `OPEN / HUMAN_ADMIT_REQUIRED` |

## Closed or materially advanced

Closed only at the stated lane:

```text
unsupported universal/performance/market claims rejected
evidence-substitution claims rejected
public/private authority boundary established
source/right/candidate routing established
cross-language canonicalization implemented and locally reproduced
exact domain/raw-key/raw-number profile hardened
stale dispatch reuse blocked by explicit superseding epoch
convergence controller fails closed without external receipt
public provenance control candidate implemented
```

## Still open on the critical path

```text
#26 independent C01 review
#24 C01 semantic admission
#5 K01 deterministic risk/challenge/grant/replay/audit core
#6 A01 persistence/idempotency/outbox/reconciliation
#7 Android hardware/integrity adapter + physical proof
#8 iOS hardware/integrity adapter + physical proof
#9 MCP protected-tool enforcement
#10 adversarial/fault/concurrency/observability harness
#11 prompt-injected-planner DevOps E2E canary
#55 independent provenance review
#51 exact upstream/dependency admission
#13 independent security + legal/Human + physical lanes
user value / paid demand
release / production
```

## Reopen law

A new source, platform revision, dependency revision, contract epoch, Worker subject, independent finding, benchmark environment, or release candidate can reopen the relevant row. Preserve the historical disposition instead of silently rewriting evidence.
