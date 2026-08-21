package actiongate.c01

private const val ARGUMENTS_HASH = "aDAZpSSDV7-lNqYY5ViQqqUTcU8J6m-qPpFu4QjfTUk"
private const val ACTION_DIGEST = "XD8ngJ-f1tD-cwVWTuqFWCCPuwTjAVyzV63rtNgW89c"
private const val SIGNING_HASH = "8sC8JA9BcBFHT9swpU81Y5EuI3bvTxzxQKYVIWTFdkw"

private fun expectRejected(id: String, block: () -> Unit) {
    try {
        block()
        error("$id: expected rejection")
    } catch (_: CanonicalizationException) {
        println("NEGATIVE $id PASS")
    }
}

private fun expectAccepted(id: String, block: () -> Unit) {
    block()
    println("POSITIVE $id PASS")
}

fun main() {
    val argumentsA = linkedMapOf<String, Any?>(
        "environment" to "production",
        "image" to "registry.example/actiongate/demo:v1",
        "service" to "payments-api",
    )
    val argumentsB = linkedMapOf<String, Any?>(
        "service" to "payments-api",
        "environment" to "production",
        "image" to "registry.example/actiongate/demo:v1",
    )
    val expectedArguments = "{\"environment\":\"production\",\"image\":\"registry.example/actiongate/demo:v1\",\"service\":\"payments-api\"}"
    check(ActionGateCanonical.canonicalString(argumentsA) == expectedArguments)
    check(ActionGateCanonical.canonicalString(argumentsB) == expectedArguments)
    check(ActionGateCanonical.digestBase64Url("ActionGate-Arguments-v1\u0000", argumentsA) == ARGUMENTS_HASH)
    println("POSITIVE arguments_hash PASS")
    println("NEGATIVE ordering PASS")

    val envelope = linkedMapOf<String, Any?>(
        "version" to "actiongate/v1",
        "action_id" to "act_demo_01",
        "agent_id" to "agent_demo",
        "subject_id" to "user_demo",
        "tool" to "deploy.production",
        "arguments_hash" to ARGUMENTS_HASH,
        "context_hash" to null,
        "risk_tier" to "R3",
        "audience" to "mcp://production-deployer",
        "policy_version" to "2026-08-21.1",
        "issued_at_ms" to 1_787_234_400_000L,
        "expires_at_ms" to 1_787_234_460_000L,
        "nonce" to "n_demo_01",
    )
    check(ActionGateCanonical.digestBase64Url("ActionGate-ActionEnvelope-v1\u0000", envelope) == ACTION_DIGEST)
    println("POSITIVE action_digest PASS")

    val challenge = linkedMapOf<String, Any?>(
        "version" to "actiongate/v1",
        "challenge_id" to "chl_demo_01",
        "action_digest" to ACTION_DIGEST,
        "subject_id" to "user_demo",
        "device_id" to "device_demo",
        "audience" to "mcp://production-deployer",
        "policy_version" to "2026-08-21.1",
        "nonce" to "c_demo_01",
        "issued_at_ms" to 1_787_234_401_000L,
        "expires_at_ms" to 1_787_234_461_000L,
    )
    check(ActionGateCanonical.sha256Base64Url(ActionGateCanonical.authorizationSigningInput(challenge)) == SIGNING_HASH)
    println("POSITIVE authorization_signing_input_sha256 PASS")

    expectRejected("float_rejected") { ActionGateCanonical.canonicalBytes(mapOf("timeout" to 1.5)) }
    expectRejected("unsafe_integer_rejected") { ActionGateCanonical.canonicalBytes(mapOf("n" to Long.MAX_VALUE)) }
    expectRejected("invalid_key_rejected") { ActionGateCanonical.canonicalBytes(mapOf("é" to 1)) }
    expectRejected("unsupported_value_rejected") { ActionGateCanonical.canonicalBytes(mapOf("bytes" to byteArrayOf(1))) }
    expectRejected("duplicate_key_control") {
        ActionGateCanonical.assertNoDuplicateKeys("{\"tool\":\"deploy.production\",\"tool\":\"delete.production\"}")
    }
    expectRejected("escaped_duplicate_key_control") {
        ActionGateCanonical.assertNoDuplicateKeys("{\"a\":1,\"\\u0061\":2}")
    }
    expectRejected("lone_surrogate") { ActionGateCanonical.canonicalBytes(mapOf("v" to "\uD800")) }
    expectRejected("raw_lone_surrogate") { ActionGateCanonical.assertNoDuplicateKeys("{\"\\uD800\":1}") }
    expectRejected("non_ascii_domain_rejected") {
        ActionGateCanonical.digestBase64Url("ActionGate-Arguménts-v1\u0000", argumentsA)
    }
    expectRejected("missing_domain_nul_rejected") {
        ActionGateCanonical.digestBase64Url("ActionGate-Arguments-v1", argumentsA)
    }

    val cycle = mutableListOf<Any?>()
    cycle.add(cycle)
    expectRejected("cyclic_container_rejected") { ActionGateCanonical.canonicalBytes(cycle) }

    expectAccepted("raw_surrogate_pair_accepted") {
        ActionGateCanonical.assertNoDuplicateKeys("{\"\\uD83D\\uDE00\":1}")
    }

    val composed = ActionGateCanonical.canonicalBytes(mapOf("v" to "\u00E9"))
    val decomposed = ActionGateCanonical.canonicalBytes(mapOf("v" to "e\u0301"))
    check(!composed.contentEquals(decomposed))
    check(String(composed, Charsets.UTF_8).contains("é"))
    check(String(decomposed, Charsets.UTF_8).contains("e\u0301"))
    println("NEGATIVE unicode_no_normalization PASS")

    println("C01 Kotlin canonical vectors + Shadow hardening: PASS")
}
