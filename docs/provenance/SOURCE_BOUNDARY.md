# Source Boundary

## Permitted sources

- exact public upstream revisions admitted in `.provenance/upstreams.lock.json`;
- pinned public specifications admitted by the source ledger;
- exact ActionGate repository files;
- synthetic data produced inside the isolated Session.

## Forbidden sources

```text
employer source or generated artifacts
private employer documentation or protocol details
private test vectors or hardware allowlists
customer data
credentials and API keys
internal CI, registries or device farms
non-public implementation details recalled from employment
private CodexDoc material in a public implementation Session
```

## Environment separation

A clean-room Session uses a personal account, personal device, isolated directory/worktree, personal credentials, public inputs and a frozen source allowlist. It records the runtime, exact subject and changed paths without exposing machine-local secrets or private URLs.

Environment separation is evidence about the development process; it is not a legal conclusion.

## Private review boundary

Employment agreement, invention assignment, confidentiality, moonlighting, conflict, business-overlap and counsel analysis stay private. Public Git receives only the redacted receipt contract in `.provenance/schemas/outside-project-review-receipt.schema.json`.
