# Provenance Local Handoff

Machine authority: `.provenance/local-handoff-queue.json`.

Exactly one item is active. Queue order is process routing, not Git ancestry. No item auto-merges, releases or promotes to production.

## `PV-LH-001` — exact public upstream baseline

**State:** `ACTIVE_INPUT_COLLECTION`

Human/Tech Lead supplies:

```text
public repository URL
exact commit or immutable tag to resolve
relationship class
intended source/dependency paths
excluded paths
license path
```

Before execution every placeholder is replaced with an exact argv value. The trusted clean host independently reads back:

```text
repository
commit
tree
tag or ABSENT
SPDX expression
LICENSE SHA-256
relationship
source/excluded boundaries
observation timestamp
```

Do not inspect employer source to compare implementations.

## `PV-LH-002` — clean-room implementation

**State:** `BLOCKED_BY_PV_LH_001`

A public-input-only Session binds the exact starting subject, typed permitted sources, complete forbidden-source denominator, personal environment assertions, output commit/tree, changed paths and real DCO evidence.

The Agent cannot answer Human employment/resource assertions on the Human's behalf.

## `PV-LH-003` — independent provenance review

**State:** `BLOCKED_BY_PV_LH_002`

A separate read-only reviewer binds base/candidate subjects, complete changed-path denominator, hosted workflow run/job, source-lock/import/lineage/SBOM digests and the fixed falsifier set.

Output:

```text
ADMIT_STATIC_PROVENANCE
BLOCK
REPLAN
```

Same-context Shadow cannot satisfy this item.

## `PV-LH-004` — private outside-project review

**State:** `HUMAN_ADMIT_REQUIRED`

Employment/IP, invention assignment, confidentiality, moonlighting/conflict, business overlap, written notice and counsel facts are reviewed privately. Only the redacted public receipt may enter Git.

## `PV-LH-005` — release eligibility

**State:** `BLOCKED_BY_PV_LH_003_AND_PV_LH_004`

Freeze a candidate commit/tree first. Add exact SBOM, independent receipt, redacted outside-project receipt, lock admission and Human release receipt in a successor commit. The checker rejects unrelated successor changes.

Human-owned:

```text
merge
release
production
visibility
legal/security acceptance
```

## Evidence ceiling

A well-formed queue proves only that work is typed and reviewable. It does not prove an upstream was selected, a clean-room Session ran, independent review passed, legal ownership is clear, an SBOM is complete, or release is authorized.
