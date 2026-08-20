# C01 Execution Preparation Control Plane

Issue: #37. Base: `ag/C01-action-contracts@b63589e5a16e82fda1a9554227f2ebbb55398c8a`.

## State Machine

```text
C01_CONTRACT_EPOCH_BOUND
→ HOSTED_CAPABILITY_OBSERVED
→ SCHEMA_ENGINE_OBSERVED
→ COMMON_RECEIPT_GATE_PREPARED
→ CLEAN_ROOM_HUMAN_GATE_BOUND
→ SESSION_DISPATCH_PACKETS_BOUND
→ INDEPENDENT_SHADOW_PACKET_BOUND
→ CONVERGENCE_PACKET_BOUND
→ K01_BLOCKED_HANDOFF_BOUND
→ C01_EXECUTION_CONTROL_PLANE_READY
```

This state machine prepares execution. It does not run Kotlin, Swift or TypeScript Workers and does not close P2.

## DAG and data flow

```text
C01 PR #17 @ b63589e...
        │
        ├─ C01 execution-preflight / #37 (this branch)
        │    ├─ hosted toolchain capability receipt / #22
        │    ├─ schema-engine receipt / #23
        │    ├─ common receipt schema + checker / #30
        │    ├─ clean-room Human gate / #29
        │    ├─ zero-context handoff / #27
        │    ├─ independent Shadow packet / #26
        │    ├─ convergence packet / #24
        │    └─ blocked K01 handoff / #25/#28
        │
        ├─ Kotlin PR #34 / contracts/impl/kotlin/**
        ├─ Swift PR #35 / contracts/impl/swift/**
        └─ TypeScript PR #36 / contracts/impl/typescript/**
                  │
                  ▼
             Issue #24 convergence
                  │
             C01_ADMITTED only
                  │
                  ▼
             K01 may start
```

## Current evidence

```text
hosted toolchain presence        OBSERVED_CURRENT_EPHEMERAL_LANE
schema-engine parity             PASS_EXACT_C01_SCHEMA_BLOBS
language implementation          NOT_IMPLEMENTED
language vector execution        NOT_EXERCISED
clean-room Human attestation     HUMAN_REVIEW_REQUIRED
independent Shadow               NOT_EXERCISED
C01 convergence                  BLOCKED_BY_WORKERS
K01                              BLOCKED_BY_C01_ADMISSION
merge/release                    HUMAN_ADMIT_REQUIRED
```

## Data boundary

Public packets contain exact GitHub subjects, commands, versions, checks and evidence ceilings. They contain no private CodexDoc locator, employer identity, credentials, stable host identifier or hidden reasoning.
