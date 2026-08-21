import Foundation

private let argumentsHash = "aDAZpSSDV7-lNqYY5ViQqqUTcU8J6m-qPpFu4QjfTUk"
private let actionDigest = "XD8ngJ-f1tD-cwVWTuqFWCCPuwTjAVyzV63rtNgW89c"
private let signingHash = "8sC8JA9BcBFHT9swpU81Y5EuI3bvTxzxQKYVIWTFdkw"

func expectRejected(_ id: String, _ body: () throws -> Void) throws {
    do {
        try body()
        fatalError("\(id): expected rejection")
    } catch is CanonicalizationError {
        print("NEGATIVE \(id) PASS")
    }
}

func expectAccepted(_ id: String, _ body: () throws -> Void) throws {
    try body()
    print("POSITIVE \(id) PASS")
}

let argumentsA: [String: Any?] = [
    "environment": "production",
    "image": "registry.example/actiongate/demo:v1",
    "service": "payments-api",
]
let argumentsB: [String: Any?] = [
    "service": "payments-api",
    "environment": "production",
    "image": "registry.example/actiongate/demo:v1",
]
let expectedArguments = "{\"environment\":\"production\",\"image\":\"registry.example/actiongate/demo:v1\",\"service\":\"payments-api\"}"
let canonicalArgumentsA = try ActionGateCanonical.canonicalString(argumentsA)
let canonicalArgumentsB = try ActionGateCanonical.canonicalString(argumentsB)
let computedArgumentsHash = try ActionGateCanonical.digestBase64URL(domain: "ActionGate-Arguments-v1\0", value: argumentsA)
precondition(canonicalArgumentsA == expectedArguments)
precondition(canonicalArgumentsB == expectedArguments)
precondition(computedArgumentsHash == argumentsHash)
print("POSITIVE arguments_hash PASS")
print("NEGATIVE ordering PASS")

let envelope: [String: Any?] = [
    "version": "actiongate/v1",
    "action_id": "act_demo_01",
    "agent_id": "agent_demo",
    "subject_id": "user_demo",
    "tool": "deploy.production",
    "arguments_hash": argumentsHash,
    "context_hash": nil,
    "risk_tier": "R3",
    "audience": "mcp://production-deployer",
    "policy_version": "2026-08-21.1",
    "issued_at_ms": Int64(1_787_234_400_000),
    "expires_at_ms": Int64(1_787_234_460_000),
    "nonce": "n_demo_01",
]
let computedActionDigest = try ActionGateCanonical.digestBase64URL(domain: "ActionGate-ActionEnvelope-v1\0", value: envelope)
precondition(computedActionDigest == actionDigest)
print("POSITIVE action_digest PASS")

let challenge: [String: Any?] = [
    "version": "actiongate/v1",
    "challenge_id": "chl_demo_01",
    "action_digest": actionDigest,
    "subject_id": "user_demo",
    "device_id": "device_demo",
    "audience": "mcp://production-deployer",
    "policy_version": "2026-08-21.1",
    "nonce": "c_demo_01",
    "issued_at_ms": Int64(1_787_234_401_000),
    "expires_at_ms": Int64(1_787_234_461_000),
]
let signingInput = try ActionGateCanonical.authorizationSigningInput(challenge)
precondition(ActionGateCanonical.sha256Base64URL(signingInput) == signingHash)
print("POSITIVE authorization_signing_input_sha256 PASS")

try expectRejected("float_rejected") { _ = try ActionGateCanonical.canonicalData(["timeout": 1.5]) }
try expectRejected("unsafe_integer_rejected") { _ = try ActionGateCanonical.canonicalData(["n": Int64.max]) }
try expectRejected("invalid_key_rejected") { _ = try ActionGateCanonical.canonicalData(["é": 1]) }
try expectRejected("unsupported_value_rejected") { _ = try ActionGateCanonical.canonicalData(["data": Data([1])]) }
try expectRejected("duplicate_key_control") {
    try ActionGateCanonical.assertNoDuplicateKeys("{\"tool\":\"deploy.production\",\"tool\":\"delete.production\"}")
}
try expectRejected("escaped_duplicate_key_control") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"a\":1,\"\\u0061\":2}")
}
try expectRejected("raw_lone_high_surrogate") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"v\":\"\\uD800\"}")
}
try expectRejected("raw_lone_low_surrogate") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"v\":\"\\uDC00\"}")
}
try expectRejected("non_ascii_domain_rejected") {
    _ = try ActionGateCanonical.digestBase64URL(domain: "ActionGate-Arguménts-v1\0", value: argumentsA)
}
try expectRejected("missing_domain_nul_rejected") {
    _ = try ActionGateCanonical.digestBase64URL(domain: "ActionGate-Arguments-v1", value: argumentsA)
}
try expectRejected("unknown_domain_rejected") {
    _ = try ActionGateCanonical.digestBase64URL(domain: "ActionGate-Unregistered-v1\0", value: argumentsA)
}
try expectRejected("embedded_nul_domain_rejected") {
    _ = try ActionGateCanonical.digestBase64URL(domain: "ActionGate-Arguments-v1\0suffix\0", value: argumentsA)
}
try expectAccepted("raw_surrogate_pair_accepted") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"v\":\"\\uD83D\\uDE00\"}")
}

let cycleArray = NSMutableArray()
cycleArray.add(cycleArray)
try expectRejected("cyclic_array_rejected") { _ = try ActionGateCanonical.canonicalData(cycleArray) }
let cycleDictionary = NSMutableDictionary()
cycleDictionary["self"] = cycleDictionary
try expectRejected("cyclic_dictionary_rejected") { _ = try ActionGateCanonical.canonicalData(cycleDictionary) }

try expectRejected("raw_non_ascii_key_rejected") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"é\":1}")
}
try expectRejected("raw_fraction_rejected") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"n\":1.0}")
}
try expectRejected("raw_exponent_rejected") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"n\":1e3}")
}
try expectRejected("raw_positive_unsafe_integer_rejected") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"n\":9007199254740992}")
}
try expectRejected("raw_negative_unsafe_integer_rejected") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"n\":-9007199254740992}")
}
try expectAccepted("raw_integer_boundaries_accepted") {
    try ActionGateCanonical.assertCanonicalJsonInput("{\"max\":9007199254740991,\"min\":-9007199254740991,\"zero\":-0}")
}

let numberBool = NSNumber(value: true)
let numberInt = NSNumber(value: 1)
let canonicalNumberBool = try ActionGateCanonical.canonicalString(["v": numberBool])
let canonicalNumberInt = try ActionGateCanonical.canonicalString(["v": numberInt])
precondition(canonicalNumberBool == "{\"v\":true}")
precondition(canonicalNumberInt == "{\"v\":1}")
print("NEGATIVE NSNumber_boolean_number_distinction PASS")

precondition(ActionGateCanonical.sha256Base64URL([]) == "47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU")
precondition(ActionGateCanonical.sha256Base64URL(Array("abc".utf8)) == "ungWv48Bz-pBQUDeXa4iI7ADYaOWF3qctBD_YfIAFa0")
precondition(ActionGateCanonical.sha256Base64URL(Array(repeating: Character("a"), count: 64).flatMap { String($0).utf8 }) == "_-BU_nrgy23GXDr5th1SCfQ5hR20PQulmXM33xVGaOs")
print("POSITIVE sha256_known_vectors PASS")

let composed = try ActionGateCanonical.canonicalData(["v": "\u{00E9}"])
let decomposed = try ActionGateCanonical.canonicalData(["v": "e\u{0301}"])
precondition(composed != decomposed)
print("NEGATIVE unicode_no_normalization PASS")

print("C01 Swift canonical vectors + profile hardening: PASS")
