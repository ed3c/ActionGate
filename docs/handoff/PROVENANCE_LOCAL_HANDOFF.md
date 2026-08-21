# Provenance Local Handoff

Machine authority: `.provenance/local-handoff-queue.json`.

## Active item — `PV-LH-001`

A Human or Tech Lead must identify the intended public upstream and relationship before any source import. Once bound, a trusted clean host reads back the exact commit and tree and hashes the exact LICENSE file.

Do not run the command template with placeholders. Do not inspect employer source to compare implementations. The comparison denominator consists only of enumerated public upstream material, ActionGate's exact public subject and synthetic fixtures.

## Success output

```text
repository URL
commit SHA
tree SHA
tag or ABSENT
SPDX expression
LICENSE SHA-256
relationship class
imported and excluded path boundary
exact observation receipt
```

## Subsequent items

```text
PV-LH-002 public-input-only clean-room Session
PV-LH-003 independent read-only provenance review
PV-LH-004 private Human employment/IP/business review
PV-LH-005 Human release eligibility
```

No item auto-merges, releases or promotes to production.
