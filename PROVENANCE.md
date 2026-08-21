# ActionGate Independent-Source and Clean-Room Provenance

## Current terminal

```text
PROVENANCE_CONTROL_PLANE = IMPLEMENTED_CANDIDATE
DERIVED_UPSTREAM         = NOT_SELECTED
IMPORTED_PATHS           = NONE_ADMITTED
PRIVATE_EMPLOYMENT_REVIEW= HUMAN_INPUT_REQUIRED
INDEPENDENT_REVIEW       = NOT_EXERCISED
RELEASE                  = BLOCKED
```

This repository may be developed from original public contracts, admitted public dependencies, or an exact public upstream. A Fork or `Derived from` statement is useful source-lineage evidence, but it is not legal clearance and does not prove business non-overlap.

## Authority split

| Evidence | Public repository authority | Human/private authority |
|---|---|---|
| Public upstream identity | exact repository, commit, tree, release/tag and source path | selection approval where required |
| License compliance | exact LICENSE/NOTICE copy, digest, SPDX state and SBOM | legal interpretation and patent/employment review |
| Clean-room implementation | permitted-source list, environment declaration, changed paths and DCO | truthfulness of personal/employment declarations |
| Patch lineage | Git parentage, imported-path map and commit history | dispute resolution |
| Release | technical gate result | legal/security/merge/release admission |

## Mandatory read route

1. `AGENTS.md`
2. this file
3. `docs/provenance/AGENTS.md`
4. `.provenance/upstreams.lock.json`
5. `.provenance/imported-paths.json`
6. `.provenance/release-gate.json`
7. `sbom/actiongate.spdx.json`
8. exact owning Issue/PR and receipts

## Provenance State Machine

```text
SOURCE_MODE_CLASSIFIED
-> UPSTREAM_SELECTED
-> UPSTREAM_SHA_TREE_LICENSE_BOUND
-> IMPORT_PATHS_BOUND
-> CLEAN_ROOM_SESSION_BOUND
-> PATCHES_DCO_BOUND
-> LICENSE_NOTICE_SBOM_VERIFIED
-> INDEPENDENT_PROVENANCE_REVIEWED
-> PRIVATE_EMPLOYMENT_IP_REVIEWED
-> HUMAN_LEGAL_ADMITTED
-> RELEASE_ELIGIBLE
```

The current state intentionally stops before `UPSTREAM_SELECTED`. No third-party project has been named as the derived-source baseline, so ActionGate must not fabricate a Fork/derived relationship.

## Source modes

| Mode | Meaning | Required evidence |
|---|---|---|
| `ORIGINAL_PUBLIC_CONTRACT_IMPLEMENTATION` | independently written from public specifications/contracts | exact public specifications, clean-room receipt and patch lineage |
| `DEPENDENCY_ONLY` | upstream consumed as an exact dependency, not copied | revision/license/NOTICE/SBOM and package lock |
| `DERIVED_PUBLIC_UPSTREAM` | source or architecture is materially derived | exact upstream commit/tree, imported path mapping, original notices and patch lineage |
| `VENDOR_IMPORT` | selected upstream files imported into this repository | per-file source mapping, source blob/digest, license and modification record |
| `CLEAN_ROOM_REIMPLEMENTATION` | behavior reimplemented from public contract without source copy | frozen public contract, independent implementation receipt and similarity stop gate |

## Data flow

```text
Public upstream / public specification
        |
        v
upstreams.lock.json
        |
        +--> imported-paths.json
        |          |
        |          v
        |     patch / source boundary
        |
        +--> LICENSES + NOTICE + SPDX SBOM
                   |
                   v
Clean-room Session receipt
        |
        v
DCO-signed patch
        |
        v
Independent provenance review
        |
        v
Private employment/IP review
        |
        v
Human legal/release admission
```

## Fail-closed laws

- No `Fork`, `Derived from`, vendor-import, or upstream-source claim without exact 40-hex commit and tree.
- No imported local path without one admitted upstream mapping.
- No license claim from repository reputation, a mutable branch, or “latest”.
- No dependency is admitted without exact license/NOTICE read-back and SBOM mapping.
- No employer source, private protocol, internal test vector, customer data, credential, company device, company CI, or private prompt context may enter an implementation Session.
- A permissive license is necessary where selected; it is not sufficient for invention assignment, confidentiality, patent, trademark, export-control, employment, or business-overlap clearance.
- A self-authored clean-room receipt is technical evidence, not independent legal review.
- Merge, release, production and public/private-boundary changes remain Human-owned.

## Commands

Structural gate:

```bash
python3 scripts/check_provenance.py --root .
python3 -m unittest discover -s tests/provenance -p 'test_*.py'
```

PR commit DCO gate:

```bash
python3 scripts/check_provenance.py --root . --commit-range '<base>..<head>'
```

Release gate intentionally fails until all required states are admitted:

```bash
python3 scripts/check_provenance.py --root . --release-gate
```

## Local Handoff

Machine queue: `.provenance/local-handoff-queue.json`.

The first blocked transition requires a Human-selected public upstream. The packet must identify the exact upstream URL, commit, tree, release/tag, relationship, license/NOTICE locations and expected imported paths. Private employment agreement, business-overlap and legal analysis stay outside public Git; only a redacted admission state may return.

## Non-claims

The control plane does not claim:

- a selected or admitted upstream;
- that the employer does not use a named project;
- business non-overlap;
- ownership under an employment agreement;
- patent or legal clearance;
- independent security/provenance review;
- merge, release or production eligibility.
