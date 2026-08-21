# AGENTS.md — Provenance and Clean-Room Scope

These instructions govern `docs/provenance/**`, `.provenance/**`, `LICENSES/**`, `sbom/**`, the provenance checker/workflow and every source-bearing change.

## Mandatory read order

1. root `AGENTS.md`
2. `docs/provenance/README.md`
3. `docs/provenance/UPSTREAM_BASELINE.md`
4. `docs/provenance/SOURCE_BOUNDARY.md`
5. `docs/provenance/PATCH_LINEAGE.md`
6. `docs/provenance/LICENSE_OBLIGATIONS.md`
7. `.provenance/policy.json`
8. `.provenance/upstreams.lock.json`
9. `.provenance/imported-paths.json`
10. `.provenance/patch-lineage.json`
11. `.provenance/local-handoff-queue.json`
12. exact Issue, PR base/head/tree, changed-path denominator, workflows, review threads and receipts

Do not reconstruct an exact source boundary from chat history.

## Source allowlist law

An implementation Session may consume only:

- public upstreams enumerated at exact revision in `.provenance/upstreams.lock.json`;
- pinned public specifications admitted by the project source ledger;
- files already present in the exact ActionGate subject;
- synthetic fixtures created within the isolated Session.

Forbidden inputs include employer source, private documents/protocols/test vectors, customer data, credentials, internal CI/artifacts/devices/registries, remembered non-public implementation details, and private CodexDoc content or locators.

## Upstream law

Before source is copied, modified or consumed:

```text
public HTTPS repository
+ exact commit
+ exact tree
+ exact LICENSE digest
+ SPDX expression
+ relationship
+ source boundary
+ excluded boundary
+ observation time
```

must be present.

A public Fork proves repository lineage only. It does not prove license compliance, independent development, employer non-overlap, ownership, patent clearance, legal admission, release or production readiness.

Never claim that an employer does not use an upstream unless an authorized objective inventory supports that statement. Public evidence is limited to the sources and resources this implementation actually used.

## Path and patch law

Repository paths are exact POSIX-relative paths. Reject:

```text
absolute paths
`.` or `..`
backslashes
control characters
double slash
drive/URI colon
glob syntax
duplicate or nested target leases
```

Every imported target has one mapping and one compatible patch-lineage record. Every non-original patch must carry exact upstream ID, source path and blob. An `ORIGINAL_PATCH` must not claim upstream source.

## Clean-room law

Each source-bearing Session records:

```text
starting subject
output commit/tree
time range
runtime
typed permitted sources
complete forbidden-source classes
personal device/account assertions
employer source/resource/time assertions
changed paths
DCO state and evidence
```

An Agent validates the receipt structure; it cannot make Human employment/IP assertions, invent a sign-off or grant legal clearance.

## DCO and history law

DCO is checked per source-bearing commit against the source inventory visible in that commit. Adding source and deleting it later does not erase history.

A machine must not fabricate a Human `Signed-off-by` trailer.

## Independent review law

Independent review requires a separate reviewer who did not implement the candidate. The receipt binds:

```text
base SHA
candidate SHA/tree
changed-path denominator
workflow run/job
source-lock/import/lineage/SBOM digests
fixed falsifier IDs
verdict and dissent
```

Same-context Shadow always records `INDEPENDENCE_NOT_CLAIMED`.

## Release successor law

The release candidate is frozen first. Independent, private-review, SBOM and release-admission artifacts are then added in a successor commit. Only the allowlisted admission paths may differ from candidate to successor.

`RELEASE_ELIGIBLE` requires all of:

```text
clean-room receipts covering every source-bearing target
independent ADMIT_STATIC_PROVENANCE
complete redacted outside-project Human admission
exact-candidate SPDX SBOM
verified notices
digest-bound Human release receipt
```

## Shadow monitor

Classify:

```text
SOURCE_DELTA
LICENSE_DELTA
PATH_LINEAGE_DELTA
AUTHORSHIP_DELTA
PRIVATE_SOURCE_DELTA
EMPLOYMENT_IP_DELTA
SBOM_DELTA
LIFECYCLE_DELTA
RELEASE_AUTHORITY_DELTA
EVIDENCE_DELTA
```

Use `L3 BLOCK` for placeholder baselines, private/internal source, unknown license, unexplained similarity, path escape, denominator shrinkage, history laundering, stale subject, fabricated DCO/Human review, fake SBOM or release without exact receipts.

## Stop conditions

Stop and issue a typed blocker when:

- the intended upstream or relationship is unknown;
- repository, commit, tree, source blob, license or digest is unknown;
- a target lacks an exact mapping or compatible lineage;
- a forbidden source may have influenced implementation;
- DCO or Human assertions would need to be fabricated;
- LICENSE/NOTICE/SBOM obligations are incomplete;
- the independent denominator is incomplete;
- a receipt tries to bind itself;
- candidate-to-successor changes exceed the admission allowlist;
- merge, release, production or visibility authority is absent.

## Current ceiling

```text
PROVENANCE_CONTROL_PLANE_IMPLEMENTED
UPSTREAM_SELECTION_REQUIRED
NO_IMPORTS_ADMITTED
CLEAN_ROOM_SESSION_NOT_EXERCISED
INDEPENDENT_REVIEW_NOT_EXERCISED
HUMAN_LEGAL_ADMIT_REQUIRED
RELEASE_BLOCKED
```
