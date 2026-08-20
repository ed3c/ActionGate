# Source Manifest

This manifest records technical-source locations and evidence classes. Source presence does not prove a claim, capability, implementation, or production behavior.

## Source classes

```text
PRIMARY_SPEC
PRIMARY_PLATFORM_DOC
PRIMARY_REPOSITORY
PRIVATE_SOURCE_BUNDLE
SECONDARY_ARTICLE
MEASURED_REPOSITORY_EVIDENCE
```

Private source URLs are resolved only through the ignored private-context binding. Public files use opaque private source IDs.

## Canonical procedure sources

| ID | Class | Locator | Use | State |
|---|---|---|---|---|
| `SRC-SKILL-TL` | PRIMARY_REPOSITORY | https://github.com/ed3c/skills-shared/tree/main/skills/agentic-tech-lead-orchestration | task contract, true DAG, workers, verification, convergence, handoff | `READ` |
| `SRC-SKILL-SHADOW` | PRIMARY_REPOSITORY | https://github.com/ed3c/skills-shared/tree/main/skills/procedural-shadow-runtime | procedure delta, side-effect gate, receipt closure | `READ` |
| `SRC-SKILL-SPATIAL` | PRIMARY_REPOSITORY | https://github.com/ed3c/skills-shared/tree/main/skills/spatial-loop-systems-engineering | constraints, state, failure, evidence and Shadow monitor | `READ` |
| `SRC-SKILL-STACK` | PRIMARY_REPOSITORY | https://github.com/ed3c/skills-shared/tree/main/skills/git-town-stacked-pr-worker | molecular branch/PR graph and path leases | `READ` |

## Protocol and platform sources

| ID | Class | Locator | Technical scope | Admission |
|---|---|---|---|---|
| `SRC-MCP-SPEC` | PRIMARY_SPEC | https://modelcontextprotocol.io/specification/2025-11-25 | MCP lifecycle, JSON-RPC messages and current transport | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-MCP-AUTH` | PRIMARY_SPEC | https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization | remote authorization/resource binding | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-JCS-8785` | PRIMARY_SPEC | https://www.rfc-editor.org/rfc/rfc8785.html | JSON Canonicalization Scheme (JCS), I-JSON constraints, deterministic property sorting and cryptographic canonical bytes | `READ_FOR_P2_CANDIDATE`; exact ActionGate profile still requires P2 decision and vectors |
| `SRC-CBOR-8949` | PRIMARY_SPEC | https://www.rfc-editor.org/rfc/rfc8949.html#section-4.2 | CBOR core deterministic encoding requirements; alternative binary canonicalization basis | `READ_AS_P2_ALTERNATIVE`; not selected by source admission alone |
| `SRC-ANDROID-PI` | PRIMARY_PLATFORM_DOC | https://developer.android.com/google/play/integrity/standard | request hash/content binding and integrity tokens | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-ANDROID-KEY` | PRIMARY_PLATFORM_DOC | https://developer.android.com/privacy-and-security/keystore | Android Keystore and hardware-backed key behavior | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-ANDROID-ATTEST` | PRIMARY_PLATFORM_DOC | https://developer.android.com/privacy-and-security/security-key-attestation | key attestation and verification constraints | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-ANDROID-BIO` | PRIMARY_PLATFORM_DOC | https://developer.android.com/identity/sign-in/biometric-auth | BiometricPrompt user-presence flow | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-APPLE-SEP` | PRIMARY_PLATFORM_DOC | https://developer.apple.com/documentation/cryptokit/secureenclave | Secure Enclave signing API | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-APPLE-LA` | PRIMARY_PLATFORM_DOC | https://developer.apple.com/documentation/localauthentication | LocalAuthentication lifecycle | `VERIFY_AT_IMPLEMENTATION` |
| `SRC-APPLE-ATTEST` | PRIMARY_PLATFORM_DOC | https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server | App Attest enrollment/challenge/assertion | `VERIFY_AT_IMPLEMENTATION` |

`SRC-JCS-8785` and `SRC-CBOR-8949` are source candidates, not a P2 architecture decision. P2 must state why one canonical representation is selected, define any stricter ActionGate profile, and preserve cross-language falsifiers. RFC 8785 is informational rather than IETF Standards Track; source classification does not upgrade its status.

## Private source bundle

| ID | Class | Public locator | Use | State |
|---|---|---|---|---|
| `PRIVATE-SOURCE-001` | PRIVATE_SOURCE_BUNDLE | resolved by private CodexDoc binding | original discussion, uploaded PDF, private URLs, market/career/business context and candidate technical proposals | `PRIVATE_ONLY` |

Technical statements derived from `PRIVATE-SOURCE-001` enter the public repository only as redacted claims with explicit evidence class. The private source cannot directly close a public implementation state.

## Freshness rule

Mutable external sources must be re-read at the exact implementation/release checkpoint. A URL or prior summary is not an immutable receipt. When a source changes, bind the observed revision/date/digest and rerun affected assertions.
