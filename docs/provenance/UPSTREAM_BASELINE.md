# Upstream Baseline

## Current disposition

```text
UPSTREAM_SELECTION_REQUIRED
NO_IMPORTS_ADMITTED
```

ActionGate currently does not assert a GitHub Fork relationship or a selected product upstream.

## Required baseline

Before code is copied, modified or consumed as a dependency, record:

```text
public repository URL
exact commit SHA
exact tree SHA
tag or ABSENT
relationship class
SPDX license expression
SHA-256 of the observed LICENSE file
imported paths
excluded paths
observation timestamp
```

For a true derivative, preserve the Fork relationship when possible. When the existing repository cannot or should not be converted into a GitHub Fork, create a dedicated baseline commit and lock the exact source metadata above. Do not rewrite old history to simulate a Fork.

## Safe public statement

> ActionGate is developed from enumerated public upstream sources and public specifications under a documented clean-room process. Exact revisions, licenses, imported paths and original patches are preserved. Employer source code, private documentation, credentials, customer data, build artifacts and development infrastructure are forbidden inputs. Employment/IP, business-overlap and release decisions remain separately Human-reviewed.

Do not claim that an employer does not use a given upstream without an authorized objective inventory.
