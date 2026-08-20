# Rights and Clean-Room Procedure

## Purpose

Ensure ActionGate is independently implemented from public standards, permissive dependencies, and newly written code without copying employer-confidential or otherwise restricted material.

This document is a technical governance control, not legal advice or legal clearance.

## Allowed provenance

```text
public platform documentation
public standards and RFCs
public repository code under an admitted license
independently written implementation from frozen public contracts
generic professional skill and publicly documented API knowledge
new test vectors generated from public specifications
```

## Forbidden provenance

```text
company source code, binaries, SDKs or copied structure
internal GitHub/GitLab/Drive/Wiki material
private protocols, packet formats or unpublished algorithms
internal test vectors, credentials, customer data or incident logs
non-public chip/vendor workarounds
patented or trade-secret implementation recalled from confidential work
code generated using private company context
company devices, accounts, CI, API keys or paid resources without authorization
```

## Clean-room state machine

```text
SOURCE_IDENTIFIED
-> RIGHTS_CLASSIFIED
-> PUBLIC_CONTRACT_EXTRACTED
-> PRIVATE_DETAILS_EXCLUDED
-> INDEPENDENT_IMPLEMENTATION_ASSIGNED
-> PROVENANCE_REVIEWED
-> LICENSE/SBOM_VERIFIED
-> HUMAN_LEGAL_ADMIT | BLOCKED
```

## Required repository evidence

For each dependency/source:

```text
exact locator and revision
license/NOTICE read-back
source classification
what was learned
what was not copied
implementation author/session/device boundary
changed paths
SBOM/transitive review
open restrictions or unknowns
```

## Separation rules

- Build only on personal equipment/accounts and authorized time.
- Do not open employer repositories or documents in the same agent session used to implement ActionGate.
- Do not paste internal content into prompts, issues, commits, test fixtures or CodexDoc.
- If a design is suspiciously identical to a confidential implementation, stop and seek independent review.
- A permissive dependency does not clear invention-assignment, confidentiality, patent, trademark, export-control or employment restrictions.
- Legal/security acceptance is a separate `HUMAN_ADMIT_REQUIRED` lane.

## Negative test

Before release, a reviewer must be able to answer from repository evidence:

```text
Which public specification required this behavior?
Which independently written contract preceded implementation?
Which dependency revision/license applies?
Which confidential information was explicitly excluded?
Can the implementation be replaced without private knowledge?
```

An unanswerable item blocks release.