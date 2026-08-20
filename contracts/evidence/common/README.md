# Common C01 Language-Worker Receipt Gate

Issue #30.

```text
Worker command/runtime evidence
→ language receipt
→ JSON Schema shape validation
→ semantic checker
→ exact receipt digest
→ independent Shadow
→ Issue #24 convergence
```

## Required denominator

```text
positive (3)
  arguments_hash
  action_digest
  authorization_signing_input_sha256

negative (7)
  ordering
  float_rejected
  unsafe_integer_rejected
  invalid_key_rejected
  unsupported_value_rejected
  duplicate_key_control
  unicode_no_normalization
```

Run deterministic fixture controls:

```bash
python3 contracts/evidence/common/selftest.py
python3 -m py_compile \
  contracts/evidence/common/check_language_worker_receipt.py \
  contracts/evidence/common/selftest.py
```

A checker PASS proves the receipt is internally admissible. It does not prove that the named commands executed or that the implementation is correct.
