# Contributing to ActionGate

## Public-source and clean-room requirement

Before contributing source-bearing code, read `docs/provenance/AGENTS.md` and `docs/provenance/README.md`.

Each contribution must identify one relationship:

- original clean-room work;
- derived public upstream;
- public dependency;
- reference implementation;
- pinned public specification;
- build tooling.

Copied or modified public source must be represented in `.provenance/upstreams.lock.json` and `.provenance/imported-paths.json`.

## DCO

Human contributors sign their own commits with:

```bash
git commit -s
```

The sign-off certifies the contributor's right to submit that patch under the project license. An Agent or automation must not invent a Human identity or `Signed-off-by` line. Machine-prepared changes remain unadmitted until the accountable Human reviews and signs or adopts them according to repository policy.

## Required PR evidence

- exact base and head;
- source relationship;
- upstream lock and path-lineage delta, or original-authorship receipt;
- clean-room Session receipt for source-bearing work;
- LICENSE, NOTICE and SPDX impact;
- deterministic checks and negative controls;
- evidence ceiling and unresolved Human decisions.

Merge, release, production, repository visibility, employment/IP and legal or security admission remain Human-owned.
