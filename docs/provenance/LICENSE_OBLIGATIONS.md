# License, Notice and SBOM Obligations

Source transparency and legal permission are separate checks.

For every admitted upstream:

1. pin the exact repository, commit and tree;
2. read exact LICENSE and NOTICE bytes at that revision;
3. record the SPDX expression and LICENSE SHA-256;
4. preserve required copyright and notice text;
5. classify attribution, source-disclosure and patent clauses;
6. verify compatibility with the intended distribution mode;
7. update an exact-candidate SPDX 2.3 SBOM;
8. retain a replacement or removal path.

A permissive label is not employer-IP, patent, trademark, export-control or legal clearance.

## Exact SBOM minimum

The release SBOM must include:

```text
SPDX-2.3
CC0-1.0 data license
public unique document namespace
timezone-aware creationInfo
non-empty creators
non-empty packages
documentDescribes pointing to an existing root package
root package versionInfo equal to the frozen candidate SHA
non-NOASSERTION declared/concluded licenses
relationships array
```

An empty placeholder or README is not a release SBOM.

## Successor-evidence release pattern

```text
candidate source commit/tree
→ generate exact SBOM and independent/private receipts
→ successor admission commit
→ verify candidate is ancestor
→ permit only lock, receipt and SBOM paths to differ
→ Human release receipt binds digests of all evidence
```

The admission commit does not rewrite product code. Any unrelated candidate-to-successor path invalidates release eligibility.

Current state:

```text
NO_UPSTREAM_LICENSE_ADMITTED
NO_THIRD_PARTY_NOTICE_ADMITTED
SBOM_PENDING_EXACT_SOURCE_GRAPH
RELEASE_BLOCKED
```
