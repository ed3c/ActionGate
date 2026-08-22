# Patch Lineage

Every source-bearing ActionGate target must have exactly one explainable classification:

```text
ORIGINAL_PATCH
DERIVED_PATCH
MECHANICAL_TRANSFORM
UNCHANGED_IMPORT
GENERATED_FROM_PUBLIC_SPEC
```

## Required fields

All records contain:

```text
change_id
target_path
authorship
receipt
```

`ORIGINAL_PATCH`:

```text
upstream_id   = null
source_path   = null
upstream_blob = null
```

Every non-original record contains:

```text
exact upstream_id
exact source_path
exact upstream_blob
```

and must match an entry in `.provenance/imported-paths.json`.

## Compatibility matrix

| Import mode | Allowed patch lineage |
|---|---|
| `UNCHANGED_IMPORT` | `UNCHANGED_IMPORT` |
| `MODIFIED_DERIVATIVE` | `DERIVED_PATCH` or `MECHANICAL_TRANSFORM` |
| `GENERATED_FROM_PUBLIC_SPEC` | `GENERATED_FROM_PUBLIC_SPEC` |

Copied or modified code requires an upstream relationship of `DERIVED_SOURCE` or `DEPENDENCY`. `GENERATED_FROM_PUBLIC_SPEC` requires `SPECIFICATION_ONLY`.

A reference implementation cannot silently become copied code.

## Review procedure

```text
exact upstream baseline
→ exact imported-path mapping
→ source blob and target candidate
→ authorship classification
→ clean-room receipt
→ DCO check
→ independent similarity/provenance review
```

Chronology, filename similarity, model output, a permissive license or a Fork badge does not establish authorship. Unexplained similarity, missing source blob, missing mapping or mismatched import mode is a blocker.

Current state: `BASELINE_ONLY`; no source-bearing patch records are admitted.
