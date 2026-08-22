# Contributing to ActionGate

## Public-source and clean-room requirement

Before changing source, dependency manifests, imported paths or provenance state, read:

```text
AGENTS.md
→ docs/provenance/AGENTS.md
→ docs/provenance/README.md
→ exact Issue / PR / receipt
```

Each contribution declares one primary relationship:

```text
ORIGINAL CLEAN-ROOM WORK
DERIVED_SOURCE
DEPENDENCY
REFERENCE_IMPLEMENTATION
SPECIFICATION_ONLY
BUILD_TOOLING
DOCUMENTATION / CONTROL PLANE
```

Copied or modified public source must be represented by exact upstream lock, imported-path mapping and compatible patch-lineage record. A reference implementation or specification-only relationship does not authorize copying.

## Clean-room receipt

Source-bearing work records:

```text
starting subject
output commit/tree
typed public inputs
complete forbidden-source set
personal environment assertions
employer source/resource/time assertions
exact changed paths
DCO state and evidence
```

Private employment or business facts do not enter public Git.

## DCO

Human contributors sign their own source-bearing commits:

```bash
git commit -s
```

The sign-off certifies the contributor's right to submit that patch under the project license. An Agent or automation must never invent a Human identity or `Signed-off-by` line.

DCO is evaluated per source-bearing commit, including source that is later removed. It does not replace license, employer/IP, patent, confidentiality or legal review.

## Required PR evidence

- exact base, candidate commit/tree and changed-path denominator;
- source relationship and upstream revision;
- source path/blob to target mapping;
- patch-lineage and clean-room receipts;
- LICENSE/NOTICE and exact-candidate SPDX impact;
- hosted/local checks and fixed negative-control denominator;
- same-context Shadow with independence not claimed;
- independent receipt when required;
- evidence ceiling, rollback and unresolved Human decisions.

## Admission receipts

A repository receipt cannot bind the commit that contains itself. Freeze the candidate first, then add evidence in a successor commit. The checker permits only admission metadata, exact SBOM, receipts and lock-state changes in that successor.

Merge, release, production, repository visibility, employment/IP, legal and security admission remain Human-owned.
