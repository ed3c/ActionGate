declare const Buffer: any;
declare const process: any;

import {
  CanonicalizationError,
  assertCanonicalJsonInput,
  assertNoDuplicateKeys,
  authorizationSigningInput,
  canonicalBytes,
  canonicalString,
  digestBase64Url,
  sha256Base64Url,
} from "../src/actionGateCanonical";

const ARGUMENTS_HASH = "aDAZpSSDV7-lNqYY5ViQqqUTcU8J6m-qPpFu4QjfTUk";
const ACTION_DIGEST = "XD8ngJ-f1tD-cwVWTuqFWCCPuwTjAVyzV63rtNgW89c";
const SIGNING_HASH = "8sC8JA9BcBFHT9swpU81Y5EuI3bvTxzxQKYVIWTFdkw";

function check(condition: boolean, message: string): void {
  if (!condition) throw new Error(message);
}

function expectRejected(id: string, body: () => void): void {
  try {
    body();
    throw new Error(`${id}: expected rejection`);
  } catch (error) {
    if (!(error instanceof CanonicalizationError)) throw error;
    console.log(`NEGATIVE ${id} PASS`);
  }
}

function expectAccepted(id: string, body: () => void): void {
  body();
  console.log(`POSITIVE ${id} PASS`);
}

const argumentsA = {
  environment: "production",
  image: "registry.example/actiongate/demo:v1",
  service: "payments-api",
};
const argumentsB = {
  service: "payments-api",
  environment: "production",
  image: "registry.example/actiongate/demo:v1",
};
const expectedArguments = '{"environment":"production","image":"registry.example/actiongate/demo:v1","service":"payments-api"}';
check(canonicalString(argumentsA) === expectedArguments, "arguments canonical bytes A");
check(canonicalString(argumentsB) === expectedArguments, "arguments canonical bytes B");
check(digestBase64Url("ActionGate-Arguments-v1\0", argumentsA) === ARGUMENTS_HASH, "arguments hash");
console.log("POSITIVE arguments_hash PASS");
console.log("NEGATIVE ordering PASS");

const envelope = {
  version: "actiongate/v1",
  action_id: "act_demo_01",
  agent_id: "agent_demo",
  subject_id: "user_demo",
  tool: "deploy.production",
  arguments_hash: ARGUMENTS_HASH,
  context_hash: null,
  risk_tier: "R3",
  audience: "mcp://production-deployer",
  policy_version: "2026-08-21.1",
  issued_at_ms: 1_787_234_400_000,
  expires_at_ms: 1_787_234_460_000,
  nonce: "n_demo_01",
};
check(digestBase64Url("ActionGate-ActionEnvelope-v1\0", envelope) === ACTION_DIGEST, "action digest");
console.log("POSITIVE action_digest PASS");

const challenge = {
  version: "actiongate/v1",
  challenge_id: "chl_demo_01",
  action_digest: ACTION_DIGEST,
  subject_id: "user_demo",
  device_id: "device_demo",
  audience: "mcp://production-deployer",
  policy_version: "2026-08-21.1",
  nonce: "c_demo_01",
  issued_at_ms: 1_787_234_401_000,
  expires_at_ms: 1_787_234_461_000,
};
check(sha256Base64Url(authorizationSigningInput(challenge)) === SIGNING_HASH, "signing input hash");
console.log("POSITIVE authorization_signing_input_sha256 PASS");

expectRejected("float_rejected", () => canonicalBytes({ timeout: 1.5 }));
expectRejected("unsafe_integer_rejected", () => canonicalBytes({ n: Number.MAX_SAFE_INTEGER + 1 }));
expectRejected("invalid_key_rejected", () => canonicalBytes({ "é": 1 }));
expectRejected("unsupported_value_rejected", () => canonicalBytes({ bytes: new Uint8Array([1]) }));
expectRejected("duplicate_key_control", () =>
  assertNoDuplicateKeys('{"tool":"deploy.production","tool":"delete.production"}'),
);
expectRejected("escaped_duplicate_key_control", () =>
  assertCanonicalJsonInput('{"a":1,"\\u0061":2}'),
);
expectRejected("lone_surrogate", () => canonicalBytes({ v: "\ud800" }));
expectRejected("raw_lone_surrogate", () => assertCanonicalJsonInput('{"v":"\\uD800"}'));
expectRejected("non_ascii_domain_rejected", () => digestBase64Url("ActionGate-Arguménts-v1\0", argumentsA));
expectRejected("missing_domain_nul_rejected", () => digestBase64Url("ActionGate-Arguments-v1", argumentsA));
expectRejected("unknown_domain_rejected", () => digestBase64Url("ActionGate-Unregistered-v1\0", argumentsA));
expectRejected("embedded_nul_domain_rejected", () =>
  digestBase64Url("ActionGate-Arguments-v1\0suffix\0", argumentsA),
);

const cyclic: unknown[] = [];
cyclic.push(cyclic);
expectRejected("cyclic_container_rejected", () => canonicalBytes(cyclic));

const sparse: unknown[] = [];
sparse.length = 1;
expectRejected("sparse_array_rejected", () => canonicalBytes(sparse));
const accessorObject: Record<string, unknown> = {};
Object.defineProperty(accessorObject, "value", { enumerable: true, get: () => 1 });
expectRejected("accessor_rejected", () => canonicalBytes(accessorObject));
const symbolObject: Record<string | symbol, unknown> = { value: 1 };
symbolObject[Symbol("hidden")] = 2;
expectRejected("symbol_key_rejected", () => canonicalBytes(symbolObject));

expectAccepted("raw_surrogate_pair_accepted", () =>
  assertCanonicalJsonInput('{"v":"\\uD83D\\uDE00"}'),
);
expectRejected("raw_non_ascii_key_rejected", () => assertCanonicalJsonInput('{"é":1}'));
expectRejected("raw_fraction_rejected", () => assertCanonicalJsonInput('{"n":1.0}'));
expectRejected("raw_exponent_rejected", () => assertCanonicalJsonInput('{"n":1e3}'));
expectRejected("raw_positive_unsafe_integer_rejected", () =>
  assertCanonicalJsonInput('{"n":9007199254740992}'),
);
expectRejected("raw_negative_unsafe_integer_rejected", () =>
  assertCanonicalJsonInput('{"n":-9007199254740992}'),
);
expectAccepted("raw_integer_boundaries_accepted", () =>
  assertCanonicalJsonInput('{"max":9007199254740991,"min":-9007199254740991,"zero":-0}'),
);

const composed = Buffer.from(canonicalBytes({ v: "\u00e9" })).toString("hex");
const decomposed = Buffer.from(canonicalBytes({ v: "e\u0301" })).toString("hex");
check(composed !== decomposed, "Unicode normalization was applied");
console.log("NEGATIVE unicode_no_normalization PASS");

console.log("C01 TypeScript canonical vectors + profile hardening: PASS");
process.exitCode = 0;
