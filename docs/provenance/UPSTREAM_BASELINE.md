# Upstream Baseline

## Current disposition

```text
UPSTREAM_SELECTION_REQUIRED
NO_IMPORTS_ADMITTED
```

ActionGate does not currently assert a GitHub Fork relationship or selected product upstream.

## Required baseline

Before source is copied, modified, generated from a specification, or consumed as a dependency, record:

```text
public HTTPS repository URL
exact commit SHA
exact tree SHA
tag or ABSENT
relationship class
SPDX license expression
SHA-256 of the exact LICENSE file
one or more intended source boundaries
excluded paths
timezone-aware observation timestamp
```

Source boundaries are scoped per upstream. Two different repositories may both have a `src/` boundary; overlap is prohibited only within one upstream or in ActionGate target paths.

## Relationship decision

```text
copied/modified code          → DERIVED_SOURCE
package/library use           → DEPENDENCY
read-only compatibility study → REFERENCE_IMPLEMENTATION
public specification only     → SPECIFICATION_ONLY
build/test tool               → BUILD_TOOLING
```

A `REFERENCE_IMPLEMENTATION` relationship does not authorize copying. Copying later requires a new `DERIVED_SOURCE` or `DEPENDENCY` admission and path mapping.

## Fork rule

For a true derivative, preserve GitHub Fork lineage when practical. If the existing ActionGate repository is not a Fork, do not rewrite history to simulate one. Use an exact baseline record and source-to-target mapping instead.

## Observation receipt

`PV-LH-001` must independently read back the commit, tree and exact license bytes. A mutable tag, branch name, release page or repository badge is not sufficient.

## Safe public statement

> ActionGate uses only enumerated public sources and public specifications under a documented source-boundary process. Exact revisions, licenses, path mappings and patch lineage are retained. Employer/private source and resources are forbidden inputs. Employment/IP, business-overlap and release decisions remain separately Human-reviewed.

Do not claim that an employer does not use a given upstream without authorized objective evidence.
