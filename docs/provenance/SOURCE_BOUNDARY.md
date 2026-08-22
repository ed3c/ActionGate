# Source Boundary

## Permitted sources

- exact public Git subjects admitted in `.provenance/upstreams.lock.json`;
- pinned public specifications admitted by the source ledger;
- exact ActionGate repository subjects;
- synthetic fixtures created inside the isolated Session.

Each clean-room receipt classifies every permitted source as:

```text
PUBLIC_GIT
PUBLIC_SPEC
ACTIONGATE_SUBJECT
SYNTHETIC_FIXTURE
```

Git subjects require exact commit/tree. Synthetic fixtures must not claim a Git subject.

## Forbidden sources

```text
EMPLOYER_SOURCE
EMPLOYER_PRIVATE_DOCUMENT
EMPLOYER_PROTOCOL
EMPLOYER_TEST_VECTOR
CUSTOMER_DATA
EMPLOYER_CREDENTIAL
EMPLOYER_BUILD_ARTIFACT
NON_PUBLIC_REMEMBERED_IMPLEMENTATION
```

The actual policy may add stricter classes but cannot remove this denominator.

## Path safety

All source, target, receipt and changed paths are POSIX-relative and exact. Reject absolute paths, parent traversal, backslashes, control characters, double slashes, URI/drive colons and glob syntax.

An import target must exist in the candidate tree. Duplicate or nested target paths are rejected because they create ambiguous ownership.

## Environment separation

A clean-room Session uses a personal device/account, isolated directory/worktree, personal credentials, public inputs and a frozen source allowlist. It records start/end time, runtime, exact output commit/tree, changed paths and DCO evidence.

The Session must record:

```text
employer_source_accessed = false
employer_resources_used = false
employer_time_used = false
private_urls_echoed = false
```

These are development-process assertions, not a legal conclusion.

## History boundary

The verifier scans the final tree and every changed commit in the declared base-to-head range. Adding a private locator or source-bearing file and deleting it later does not remove the violation from public history.

## Private review boundary

Employment agreement, invention assignment, confidentiality, moonlighting, conflicts, business overlap, written notice and counsel analysis stay private. Public Git receives only a redacted receipt conforming to the outside-project review schema.
