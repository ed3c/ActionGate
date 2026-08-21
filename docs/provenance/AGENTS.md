# AGENTS.md — Provenance scope

## Scope

These instructions govern:

```text
.provenance/**
docs/provenance/**
LICENSES/**
sbom/**
scripts/check_provenance.py
tests/provenance/**
.github/workflows/provenance-guard.yml
.github/pull_request_template.md
CONTRIBUTING.md
PROVENANCE.md
```

## Read before mutation

1. root `AGENTS.md`
2. root `PROVENANCE.md`
3. Issue #48
4. exact base/head/tree and current open writers
5. `.provenance/upstreams.lock.json`
6. `.provenance/imported-paths.json`
7. `.provenance/release-gate.json`
8. `sbom/actiongate.spdx.json`

## Writer law

One writer owns this scope. Do not modify C01 contracts, language implementations, packages, adapters, or another atom's receipts. A later upstream-admission worker may update only the selected upstream entry, exact license copies, imported-path map, SBOM and its own receipt.

## Independent-source law

Never infer an upstream. Select one only from an explicit Human/task contract. A source relationship is one of:

```text
DEPENDENCY_ONLY
DERIVED_PUBLIC_UPSTREAM
VENDOR_IMPORT
CLEAN_ROOM_REIMPLEMENTATION
```

Every derived/vendor relationship binds exact commit, tree, license digest, source paths and local paths. An original implementation from public contracts must not be falsely labeled as a Fork.

## Clean-room law

Implementation sessions may consume only sources listed in the active task and public lock. Stop when any employer/private source, confidential implementation detail, private prompt context, credential, customer data, internal test vector, company resource or unexplained similarity appears.

An Agent may prepare a declaration template. It may not assert the Human facts in that declaration.

## Evidence ceiling

Structural PASS proves only that the public control files are internally consistent and fail closed. It does not prove the declaration is true, an upstream license is legally sufficient, employment ownership is resolved, independent review ran, or release is authorized.

## Shadow blockers

```text
UNPINNED_UPSTREAM
UNLOCKED_IMPORT
LICENSE_DIGEST_MISMATCH
SBOM_DRIFT
DCO_MISSING
PRIVATE_LOCATOR_OR_SECRET
EMPLOYER_DETAIL_IN_PUBLIC_RECEIPT
SELF_REVIEW_AS_INDEPENDENT
PERMISSIVE_LICENSE_AS_LEGAL_CLEARANCE
RELEASE_WITH_BLOCKERS
```
