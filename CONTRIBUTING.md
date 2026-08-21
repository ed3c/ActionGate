# Contributing to ActionGate

## Developer Certificate of Origin

Every commit must carry a DCO sign-off:

```bash
git commit -s
```

The `Signed-off-by:` identity must match the actual contributor identity. Do not sign for another person.

## Provenance declaration

Every PR must classify each changed source path as one of:

```text
ORIGINAL_AUTHORSHIP
PUBLIC_CONTRACT_REIMPLEMENTATION
DEPENDENCY_ONLY
DERIVED_PUBLIC_UPSTREAM
VENDOR_IMPORT
GENERATED_FROM_PUBLIC_CONTRACT
```

Derived/vendor work requires an admitted entry in `.provenance/upstreams.lock.json` and a mapping in `.provenance/imported-paths.json`.

## Clean-room boundary

Do not use employer source, internal documents, private protocols, internal test vectors, customer data, credentials, company devices/CI, or private prompt context. Stop on suspicious similarity and request independent review.

## Dependency and license changes

A dependency or upstream change must include:

- exact repository and revision;
- LICENSE/NOTICE read-back and digest;
- SPDX/SBOM update;
- transitive and replacement-path review;
- explicit evidence ceiling.

## Human-owned gates

Legal/security acceptance, employment-IP review, merge, release and production are not granted by a green technical check.
