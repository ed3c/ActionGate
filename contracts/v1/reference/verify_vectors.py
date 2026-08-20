#!/usr/bin/env python3
"""Dependency-free checker for ActionGate C01 restricted V1 fixtures.

This is not a full generic RFC 8785 implementation. It proves only the frozen
ActionGate restricted fixture profile on this runtime.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_INT = 9007199254740991
KEY_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")


class ContractError(ValueError):
    pass


def no_dupes(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ContractError(f"duplicate key: {key}")
        out[key] = value
    return out


def loads(raw):
    return json.loads(raw, object_pairs_hook=no_dupes)


def validate(value, path="$"):
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int) and not isinstance(value, bool):
        if not -MAX_INT <= value <= MAX_INT:
            raise ContractError(f"integer range {path}")
        return
    if isinstance(value, float):
        raise ContractError(f"float forbidden {path}")
    if isinstance(value, str):
        if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
            raise ContractError(f"surrogate {path}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            validate(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not KEY_RE.fullmatch(key):
                raise ContractError(f"key profile {path}.{key!r}")
            validate(item, f"{path}.{key}")
        return
    raise ContractError(f"unsupported type {path}")


def canonical(value):
    validate(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(domain, value):
    return base64.urlsafe_b64encode(
        hashlib.sha256(domain + canonical(value)).digest()
    ).decode("ascii").rstrip("=")


def require(obj, names):
    missing = [name for name in names if name not in obj]
    if missing:
        raise ContractError("missing: " + ",".join(missing))


def main():
    data = json.loads((ROOT / "vectors.json").read_text(encoding="utf-8"))
    positive = data["positive"]
    negative = data["negative"]

    arguments_hash = digest(b"ActionGate-Arguments-v1\x00", positive["arguments"])
    assert arguments_hash == positive["arguments_hash"]

    envelope = positive["action_envelope"]
    require(envelope, [
        "version", "action_id", "agent_id", "subject_id", "tool",
        "arguments_hash", "context_hash", "risk_tier", "audience",
        "policy_version", "issued_at_ms", "expires_at_ms", "nonce",
    ])
    assert envelope["expires_at_ms"] > envelope["issued_at_ms"]
    action_digest = digest(b"ActionGate-ActionEnvelope-v1\x00", envelope)
    assert action_digest == positive["action_digest"]

    challenge = positive["authorization_challenge"]
    require(challenge, [
        "version", "challenge_id", "action_digest", "subject_id", "device_id",
        "audience", "policy_version", "nonce", "issued_at_ms", "expires_at_ms",
    ])
    assert challenge["expires_at_ms"] > challenge["issued_at_ms"]
    signing_hash = digest(b"ActionGate-AuthorizationChallenge-v1\x00", challenge)
    assert signing_hash == positive["authorization_signing_input_sha256"]

    assert digest(
        b"ActionGate-Arguments-v1\x00", negative["arguments_image_changed"]
    ) != arguments_hash
    assert digest(
        b"ActionGate-ActionEnvelope-v1\x00", negative["action_wrong_audience"]
    ) != action_digest

    try:
        require(negative["action_missing_policy_version"], ["policy_version"])
        raise AssertionError("missing field accepted")
    except ContractError:
        pass

    bad_expiry = negative["challenge_invalid_expiry"]
    assert bad_expiry["expires_at_ms"] <= bad_expiry["issued_at_ms"]

    try:
        loads(negative["duplicate_key_raw"])
        raise AssertionError("duplicate key accepted")
    except ContractError:
        pass

    try:
        canonical(loads(negative["float_raw"]))
        raise AssertionError("float accepted")
    except ContractError:
        pass

    print("C01 restricted canonicalization/reference vectors: PASS")
    print("JSON-Schema engine parity: NOT_EXERCISED")
    print("Kotlin/Swift/TypeScript parity: NOT_EXERCISED")
    print("hardware/provider/integration lanes: NOT_EXERCISED")


if __name__ == "__main__":
    main()
