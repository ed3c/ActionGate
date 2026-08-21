# Patch Lineage

Every source-bearing target path must be explainable as one of:

```text
ORIGINAL_PATCH
DERIVED_PATCH
MECHANICAL_TRANSFORM
UNCHANGED_IMPORT
GENERATED_FROM_PUBLIC_SPEC
```

For imported or derived code, record the exact upstream ID, source path and source blob. For original code, record the clean-room Session receipt and changed path.

## Review procedure

```text
upstream baseline
→ imported path map
→ candidate patch
→ source/blob comparison
→ authorship classification
→ DCO and receipt check
→ independent provenance review
```

Chronology, filename similarity, a model statement or a permissive license does not establish authorship. Unexplained similarity is a blocker.

Current state: `BASELINE_ONLY`; no source-bearing patch records have been admitted.
