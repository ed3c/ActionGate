# C01 Worker Session Launch Packets

State: `C01_WORKER_SESSION_LAUNCH_PACKETS_READY`

This directory converts the generic C01 Worker prompt into exact, zero-placeholder packets. It does not launch a Session or implement code.

## Immutable inputs

```text
C01 contract       b63589e5a16e82fda1a9554227f2ebbb55398c8a
execution control  9f41038240837ea2dd9dcdb9befd13e6ba81a78e
Kotlin prep        0136936e7d63ba0c538d2cb40db60409107ababc
Swift prep         76b10b5a05898410ed361761626b381158edb306
TypeScript prep    c62e24ffa0ceb2224fe6931929bfaeeceabe3c39
```

## State Machine

```text
PACKETS_BOUND
→ FRESH_SESSION_CREATED
→ HUMAN_CLEAN_ROOM_DECLARED
→ SESSION_RUNTIME_REPROBED
→ EXACT_BRANCH_HEAD_VERIFIED
→ WORKER_IMPLEMENTATION_ALLOWED
→ FIRST_RECEIPT_EMITTED
```

Current state ends at `PACKETS_BOUND`.

## DAG

```text
PR #38 execution-control exact subject
        |
        v
Issue #39 launch packet compiler
        |
        +--> Kotlin fresh Session  ----\
        +--> Swift fresh Session    ----+--> Issue #26 independent Shadow --> Issue #24 convergence
        +--> TypeScript fresh Session --/
```

The language Sessions are siblings. Queue order never creates Git ancestry.

## Active Local Handoff

`CLH-001` is ACTIVE:

1. Human creates a fresh public-input-only Session.
2. Human completes `clean-room-attestation.template.json` for that lane.
3. The new Session re-probes its own runtime.
4. The new Session verifies the exact Worker branch/head/tree.
5. Only then may it write inside its lease.

## Why this conversation stops before implementation

This conversation includes private strategic context. Reusing it as an implementation Session would make the clean-room declaration false. The safe continuation is a fresh Session using only one compiled prompt and the public GitHub subjects named there.

## Validation

```text
python3 .actiongate/c01-launch/check_launch_packets.py
python3 .actiongate/c01-launch/selftest.py
```

Validation proves packet consistency only. It does not prove Session execution, Human attestation, code correctness, independent review or C01 admission.
