# ActionGate v1 Contract Plane

Read `PROFILE.md` first. Machine contract definitions live in `actiongate-contracts.schema.json`; frozen positive/mutation fixtures live in `vectors.json`; `reference/verify_vectors.py` is a dependency-free restricted-profile checker.

## State Machine ownership

```text
SOURCE_CONSTRAINTS_READ
-> PROFILE_FROZEN
-> SCHEMA_FROZEN
-> REFERENCE_VECTORS_FROZEN
-> MUTATION_CONTROLS_FROZEN
-> DRAFT_PUBLISHED
-> CROSS_LANGUAGE_REPRODUCED
-> C01_ADMITTED
```

The current C01 preparation target ends at `DRAFT_PUBLISHED`. `C01_ADMITTED` requires independent Kotlin/Swift/TypeScript reproduction and owning assertions on the exact subject.

## DAG

```text
S01 exact source/rights subject
        |
        v
C01 schema/profile owner
        |
        +--> Kotlin serializer/vector worker
        +--> Swift serializer/vector worker
        +--> TypeScript serializer/vector worker
        +--> Python reference checker
                  |
                  v
        one C01 convergence/readback
                  |
                  +--> K01 deterministic core
                  +--> A02 Android adapter
                  +--> A03 iOS adapter
```

Language workers are siblings after the profile is frozen. They may not redefine the canonical contract.
