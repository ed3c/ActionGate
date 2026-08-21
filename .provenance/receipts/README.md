# Provenance receipts

This directory stores redacted receipts bound to exact predecessor subjects.

Allowed receipt classes:

- upstream baseline observation;
- clean-room Session;
- imported-path verification;
- independent provenance review;
- redacted outside-project review;
- release admission;
- control-plane hosted-verification successor receipt.

## Non-self-reference law

A tracked receipt cannot truthfully identify the commit/tree that contains itself. Use:

```text
implementation candidate commit/tree
→ external/read-only evidence
→ successor receipt commit
```

The receipt records the predecessor candidate. The checker proves the candidate is an ancestor of the receipt head and limits successor changes according to the applicable gate.

## Forbidden content

Never store a private document locator, employment agreement, legal memo, company/product comparison, customer identity, credential, device identifier, secret, private reasoning or employer-confidential detail.

## Current state

Only control-plane verification receipts may exist before source selection. No product upstream, source import, clean-room product Session, independent provenance admission, outside-project legal admission or release eligibility is implied.
