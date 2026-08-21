# Public / Private Authority Contract

## Public ActionGate authority

The public repository may contain only technical material required to build, verify, review, reproduce, or hand off ActionGate:

```text
code and build configuration
protocols, schemas and test vectors
technical architecture and threat model
technical ADRs
Issues, branches, PR topology and checks
source-claim states and public locators
license, NOTICE, SBOM and dependency evidence
benchmarks with reproducible environment
failure, security and observability receipts
technical prompts and task packets
```

## Private CodexDoc authority

Private CodexDoc owns material that must not be projected into the public repository:

```text
original private intent and prioritization
business model, pricing, GTM and customer strategy
career/job-search analysis
private source URLs and full private-source archive
non-public roadmap and commercial hypotheses
employer-confidential constraints or legal review notes
private outreach, customer and design-partner information
```

## Conflict rules

- GitHub exact-subject read-back wins for technical implementation/completion.
- Private CodexDoc wins for private intent and private strategic context.
- A Google Doc/Sheet cell cannot mark a GitHub task complete.
- A GitHub technical document cannot infer or expose private strategy.
- Proposed changes from private context enter GitHub as a technical Issue/contract with private content removed.
- Public technical evidence may be projected into CodexDoc, but the projection must retain its exact SHA/Issue/PR locator and evidence state.

## Multi-hop binding

The public repository stores only a binding shape. The actual private URLs exist in an ignored local file, environment, or connected-source configuration.

```text
AGENTS.md
-> private binding resolver
-> private Doc/Sheet read, when authorized
-> derive technical delta
-> redact private material
-> GitHub Issue/task packet
-> public implementation and exact-subject verification
```

When the private lane is absent, the Agent records `PRIVATE_CONTEXT_UNAVAILABLE` and cannot invent the missing intent.

## Clean-room boundary

No contributor may copy or reconstruct employer-confidential code, SDKs, packet formats, proprietary algorithms, internal documentation, test vectors, customer data, unpublished chip workarounds, or non-public architecture into ActionGate.

Public standards knowledge and independently written code are admissible only when provenance is recorded and contractual restrictions are respected. Permissive open-source licensing does not override employment, invention-assignment, confidentiality, patent, export-control, or trade-secret obligations.

## Leak check

Before publication or convergence, inspect the full tree, Issue/PR bodies, logs, fixtures, screenshots, and receipts for:

```text
docs.google.com or drive.google.com private URLs
private folder/document IDs
customer/company internal names
API keys, access tokens or credentials
private roadmap dates and priorities
pricing/GTM/career text
employer code or internal terminology
machine-local paths containing identity or secrets
```

Any finding is an `L3 BLOCK` until removed and read back from the exact published subject.