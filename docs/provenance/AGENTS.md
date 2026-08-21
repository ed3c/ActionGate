# AGENTS.md — Provenance and Clean-Room Scope

These instructions apply to `docs/provenance/**`, `.provenance/**`, `LICENSES/**`, `sbom/**`, provenance checks and any source-import change.

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
11. the exact Issue, PR base/head, checks and receipts

## Source allowlist law

An implementation Session may consume only:

- public upstreams enumerated by exact revision in `.provenance/upstreams.lock.json`;
- pinned public specifications already admitted by the project source ledger;
- files already present in the exact ActionGate subject;
- synthetic test data created in the clean-room Session.

Forbidden:

- employer source, private documents, protocols or test vectors;
- employer/customer data, credentials, CI, artifacts, devices or internal registries;
- remembered non-public implementation details;
- private CodexDoc content or URLs;
- guessed upstream versions, licenses, hashes or company dependency claims.

## Independent-source law

A public Fork or upstream attribution proves source lineage only. It does not prove license compliance, independent development, employer non-overlap, ownership, patent clearance, legal admission, security, release or production readiness.

Never write “the employer does not use this upstream” unless an authorized, objective inventory proves it. The public claim is limited to which sources this implementation Session did or did not access.

## Contribution law

Every source-bearing contribution must:

1. bind an enumerated upstream or declare original authorship;
2. map every imported source path and source blob;
3. preserve copyright, LICENSE and NOTICE obligations;
4. update patch lineage and the exact-subject SPDX SBOM;
5. produce a clean-room Session receipt;
6. carry a real contributor DCO sign-off when policy requires it;
7. stop on license, patent, confidentiality, employer-IP, business-overlap or unexplained-similarity ambiguity.

An Agent must never invent a Human `Signed-off-by` trailer.

## Shadow monitor

Read-only Shadow classifies:

```text
SOURCE_DELTA
LICENSE_DELTA
PATH_LINEAGE_DELTA
AUTHORSHIP_DELTA
PRIVATE_SOURCE_DELTA
EMPLOYMENT_IP_DELTA
SBOM_DELTA
RELEASE_AUTHORITY_DELTA
EVIDENCE_DELTA
```

Use `L3 BLOCK` on any forbidden source, placeholder baseline, unknown license, missing notice, unregistered imported path, false legal admission, private URL leak, unexplained source similarity or release without exact receipts.

Same-context Shadow must state `INDEPENDENCE_NOT_CLAIMED`.

## Stop conditions

Stop and issue a typed blocker when:

- the intended upstream is not selected;
- repository, commit, tree, license or digest is unknown;
- a copied path lacks an exact upstream blob;
- a private/employer source may have influenced the implementation;
- DCO would need to be fabricated;
- exact notice/SBOM obligations are unresolved;
- independent or Human review is required;
- release/production is requested without admission.

## Current ceiling

`PROVENANCE_CONTROL_PLANE_IMPLEMENTED`; no upstream/import/clean-room/legal/release evidence has yet been earned.
