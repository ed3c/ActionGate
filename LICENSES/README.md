# Third-party license copies

No third-party upstream or dependency is admitted by this directory alone.

When an upstream is admitted, store the exact LICENSE and NOTICE bytes under a stable path such as:

```text
LICENSES/<upstream-id>/LICENSE
LICENSES/<upstream-id>/NOTICE
```

`.provenance/upstreams.lock.json` must record the exact repository, commit, tree, relationship, SPDX identifier, file path and SHA-256 digest. The provenance guard recomputes the digest. A copied license does not by itself establish compatibility, patent clearance, employment ownership, or release permission.
