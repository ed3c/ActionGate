## Source relationship

Select exactly one primary relationship:

- [ ] Original clean-room work
- [ ] Derived public upstream
- [ ] Public dependency
- [ ] Reference implementation only
- [ ] Pinned public specification
- [ ] Build tooling
- [ ] Documentation/control-plane only

## Exact provenance

- Base SHA:
- Candidate SHA/tree:
- Successor receipt SHA/tree, or `NOT_APPLICABLE`:
- Upstream ID and exact repository/commit/tree, or `NOT_APPLICABLE`:
- LICENSE SPDX and SHA-256, or `NOT_APPLICABLE`:
- Imported source path / source blob / target path / mode, or `NONE`:
- Patch-lineage record(s), or `NONE`:
- Clean-room receipt(s), or reason not applicable:
- Exact changed-path denominator:
- SPDX/NOTICE impact:
- Evidence ceiling:

## Required assertions

- [ ] The declared base is an ancestor of the candidate.
- [ ] No employer source, private documentation, protocol, test vector, customer data, credential, artifact, time or internal infrastructure was used.
- [ ] No private CodexDoc locator or content is included, including in earlier commits.
- [ ] Every non-original target is mapped to an exact public source path/blob and compatible patch-lineage record.
- [ ] Every original patch has a clean-room receipt and does not claim upstream source.
- [ ] LICENSE and NOTICE obligations are preserved or the PR remains blocked.
- [ ] The exact-candidate SPDX SBOM is updated, or this PR truthfully remains pre-SBOM and non-releaseable.
- [ ] Required source-bearing commits carry a real contributor DCO; automation did not invent a Human sign-off.
- [ ] This PR does not claim employer non-use, non-overlap, legal clearance, independent review, release or production readiness without the owning receipts.
- [ ] Any admission receipt uses the predecessor/successor pattern rather than self-referencing its own commit.

## Independent review

- Reviewer did not implement this candidate: `YES | NO | NOT_EXERCISED`
- Read-only: `YES | NO | NOT_EXERCISED`
- Base/candidate/denominator:
- Hosted workflow run/job:
- Falsifier denominator:
- Verdict: `ADMIT_STATIC_PROVENANCE | BLOCK | REPLAN | NOT_EXERCISED`
- Dissent:

## Shadow / rollback

- Same-context Shadow verdict:
- Independence claimed: `NO` unless produced by a separate reviewer
- Negative controls:
- Rollback identity:
- Human-owned operations:
