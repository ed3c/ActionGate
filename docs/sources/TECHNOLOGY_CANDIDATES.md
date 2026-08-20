# Technology Candidates — Commercial / Permissive Review

This is a candidate ledger, not an approved dependency manifest. Before adoption, pin an exact revision/release, re-read `LICENSE` and `NOTICE`, generate an SBOM, inspect transitive dependencies, and record replacement/exit behavior.

## Default selection laws

- Prefer standard platform APIs and permissive licenses.
- Do not make ActionGate's security invariant depend on a hosted vendor.
- Avoid AGPL/copyleft/source-available dependencies in the default closed-service path unless separately reviewed and isolated.
- Cryptographic primitives use platform APIs or widely reviewed libraries; do not invent new primitives.
- The domain core remains transport, persistence, mobile-platform and inference-engine neutral.
- A technology candidate does not become `ADMITTED` until the owning atom proves required semantics.

## V0 core candidates

| Capability | Candidate | Repository / source | Observed license evidence | Status / concern |
|---|---|---|---|---|
| MCP Python middleware | MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk | MIT `LICENSE` blob `3d48435454b105021b4f777c11b6b07d8d2ffea3` | `CANDIDATE`; pin release and transitive set |
| MCP TypeScript middleware | MCP TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk | repository is in MIT→Apache-2.0 transition; docs may be CC-BY-4.0 | `REVIEW_REQUIRED`; file/revision-level license mapping |
| HTTP service | FastAPI | https://github.com/fastapi/fastapi | MIT `LICENSE` blob `3e92463e6bd522a2a21e5f0a80d8089d6c4be20d` | `CANDIDATE` |
| Schemas/validation | Pydantic | https://github.com/pydantic/pydantic | permissive; exact release license must be read | `CANDIDATE_UNPINNED` |
| Server cryptography | Google Tink | https://github.com/tink-crypto/tink | Apache-2.0 `LICENSE` blob `d645695673349e3947e8e5ae42332d0ac3164cd7` | `CANDIDATE`; confirm supported P-256/JWS/serialization design |
| iOS portable crypto helpers | Swift Crypto | https://github.com/apple/swift-crypto | Apache-2.0 `LICENSE.txt` blob `d645695673349e3947e8e5ae42332d0ac3164cd7` | `OPTIONAL`; Secure Enclave key lifecycle remains platform API |
| SQL source of truth | PostgreSQL | https://www.postgresql.org/about/licence/ | PostgreSQL License | `CANDIDATE`; migrations/reconciliation still ours |
| TTL/replay cache | Valkey | https://github.com/valkey-io/valkey | BSD-3-Clause `COPYING` blob `a2782ea7ba8784d1116974c91df9706499eda3d7` | `CANDIDATE`; persistence/eviction failure semantics require tests |
| Local embedded DB | SQLite | https://www.sqlite.org/copyright.html | public-domain dedication | `CANDIDATE`; extensions reviewed separately |
| Local vector extension | sqlite-vec | https://github.com/asg017/sqlite-vec | MIT `LICENSE-MIT` blob `9c106bc48c760f7ed9f5b8255dea7adeef029cbe` | `OPTIONAL_PHASE_2` |
| Telemetry | OpenTelemetry | https://github.com/open-telemetry | generally Apache-2.0; exact language SDK/exporter release required | `CANDIDATE_UNPINNED` |
| Native crypto utility | libsodium | https://github.com/jedisct1/libsodium | ISC; exact release and bundled licenses required | `OPTIONAL`; not a replacement for Keystore/SEP |
| Python crypto/X.509 | pyca/cryptography | https://github.com/pyca/cryptography | Apache-2.0/BSD dual licensing; exact release required | `CANDIDATE_UNPINNED` |

## Platform primitives

These are platform APIs, not third-party application dependencies:

```text
Android Keystore / KeyMint / StrongBox
AndroidX Biometric / BiometricPrompt
Google Play Integrity and key attestation services
iOS Secure Enclave / Security.framework / CryptoKit
LocalAuthentication
App Attest / DeviceCheck
```

Their availability, policy, quotas, device coverage, lifecycle and service behavior still require current official documentation and real-device evidence.

## Optional on-device inference candidates

On-device inference is not required for V0 authorization closure.

| Candidate | Repository | Observed license evidence | Intended use | Status |
|---|---|---|---|---|
| llama.cpp | https://github.com/ggml-org/llama.cpp | MIT `LICENSE` blob `e7dca554bcb802f98408383a864404e3aa4eacca` | portable optional SLM/inference adapter | `OPTIONAL_PHASE_2`; not universal default |
| LiteRT | https://github.com/google-ai-edge/LiteRT | Apache-2.0 `LICENSE` blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | Android/iOS custom-model runtime candidate | `OPTIONAL_PHASE_2` |
| ExecuTorch | https://github.com/pytorch/executorch | permissive PyTorch-family license; exact release required | custom PyTorch edge runtime | `OPTIONAL_UNPINNED` |
| ONNX Runtime | https://github.com/microsoft/onnxruntime | MIT; exact release required | VAD/classifier/runtime adapter | `OPTIONAL_UNPINNED` |
| MLX / MLX Swift | https://github.com/ml-explore/mlx and https://github.com/ml-explore/mlx-swift | permissive; exact release required | Apple custom inference experiments | `OPTIONAL_UNPINNED` |

## Not selected as a default

| Candidate/category | Reason |
|---|---|
| Redis-branded server without exact license review | current licensing/options require product and deployment-specific review; Valkey is the initial permissive candidate |
| AGPL service embedded in the default hosted control plane | may impose network-copyleft obligations; requires explicit architecture/legal isolation |
| custom cryptographic primitives | unacceptable verification and maintenance burden |
| cross-platform export of platform private keys | violates the trust-boundary design |
| one inference engine hard-coded into domain contracts | couples authorization correctness to unrelated device/runtime selection |

## Admission packet

Every selected dependency must add:

```yaml
name: ...
repository: ...
revision_or_release: ...
license_files: []
notice_files: []
transitive_sbom: ...
commercial_use_review: ...
security_update_owner: ...
invariants_delegated: []
invariants_retained: []
failure_modes: []
replacement_path: ...
verification_receipt: ...
```

Until that packet exists, the state remains `CANDIDATE`.