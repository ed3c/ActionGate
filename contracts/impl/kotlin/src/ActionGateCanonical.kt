package actiongate.c01

import java.io.ByteArrayOutputStream
import java.nio.charset.StandardCharsets
import java.security.MessageDigest
import java.util.Base64

private const val MAX_SAFE_INTEGER: Long = 9_007_199_254_740_991L
private val KEY_PATTERN = Regex("^[A-Za-z0-9_.:-]+$")

class CanonicalizationException(message: String) : IllegalArgumentException(message)

sealed interface CanonicalValue {
    data object Null : CanonicalValue
    data class Bool(val value: Boolean) : CanonicalValue
    data class Integer(val value: Long) : CanonicalValue
    data class Text(val value: String) : CanonicalValue
    data class ArrayValue(val values: List<CanonicalValue>) : CanonicalValue
    data class ObjectValue(val values: Map<String, CanonicalValue>) : CanonicalValue
}

object ActionGateCanonical {
    fun canonicalBytes(value: Any?): ByteArray = encode(fromAny(value)).toByteArray(StandardCharsets.UTF_8)

    fun canonicalString(value: Any?): String = encode(fromAny(value))

    fun digestBase64Url(domain: String, value: Any?): String {
        require(domain.endsWith('\u0000')) { "domain must end with NUL" }
        val digest = MessageDigest.getInstance("SHA-256")
        digest.update(domain.toByteArray(StandardCharsets.US_ASCII))
        digest.update(canonicalBytes(value))
        return Base64.getUrlEncoder().withoutPadding().encodeToString(digest.digest())
    }

    fun sha256Base64Url(bytes: ByteArray): String = Base64.getUrlEncoder()
        .withoutPadding()
        .encodeToString(MessageDigest.getInstance("SHA-256").digest(bytes))

    fun authorizationSigningInput(challenge: Any?): ByteArray {
        val out = ByteArrayOutputStream()
        out.write("ActionGate-AuthorizationChallenge-v1\u0000".toByteArray(StandardCharsets.US_ASCII))
        out.write(canonicalBytes(challenge))
        return out.toByteArray()
    }

    fun assertNoDuplicateKeys(raw: String) {
        DuplicateKeyParser(raw).parseDocument()
    }

    private fun fromAny(value: Any?): CanonicalValue = when (value) {
        null -> CanonicalValue.Null
        is Boolean -> CanonicalValue.Bool(value)
        is Byte -> integer(value.toLong())
        is Short -> integer(value.toLong())
        is Int -> integer(value.toLong())
        is Long -> integer(value)
        is Float, is Double -> throw CanonicalizationException("floating point is forbidden")
        is String -> {
            validateUnicode(value)
            CanonicalValue.Text(value)
        }
        is List<*> -> CanonicalValue.ArrayValue(value.map(::fromAny))
        is Map<*, *> -> {
            val converted = LinkedHashMap<String, CanonicalValue>()
            for ((key, item) in value) {
                if (key !is String || !KEY_PATTERN.matches(key)) {
                    throw CanonicalizationException("invalid object key: $key")
                }
                if (converted.containsKey(key)) {
                    throw CanonicalizationException("duplicate object key: $key")
                }
                converted[key] = fromAny(item)
            }
            CanonicalValue.ObjectValue(converted)
        }
        else -> throw CanonicalizationException("unsupported value type: ${value::class.qualifiedName}")
    }

    private fun integer(value: Long): CanonicalValue.Integer {
        if (value < -MAX_SAFE_INTEGER || value > MAX_SAFE_INTEGER) {
            throw CanonicalizationException("integer outside safe range")
        }
        return CanonicalValue.Integer(value)
    }

    private fun encode(value: CanonicalValue): String = when (value) {
        CanonicalValue.Null -> "null"
        is CanonicalValue.Bool -> if (value.value) "true" else "false"
        is CanonicalValue.Integer -> value.value.toString()
        is CanonicalValue.Text -> quote(value.value)
        is CanonicalValue.ArrayValue -> value.values.joinToString(prefix = "[", postfix = "]", separator = ",") { encode(it) }
        is CanonicalValue.ObjectValue -> value.values.keys.sorted().joinToString(prefix = "{", postfix = "}", separator = ",") { key ->
            quote(key) + ":" + encode(value.values.getValue(key))
        }
    }

    private fun quote(value: String): String {
        validateUnicode(value)
        val out = StringBuilder(value.length + 2)
        out.append('"')
        var index = 0
        while (index < value.length) {
            val ch = value[index]
            when (ch) {
                '"' -> out.append("\\\"")
                '\\' -> out.append("\\\\")
                '\b' -> out.append("\\b")
                '\t' -> out.append("\\t")
                '\n' -> out.append("\\n")
                '\u000C' -> out.append("\\f")
                '\r' -> out.append("\\r")
                else -> {
                    if (ch.code < 0x20) {
                        out.append("\\u")
                        out.append(ch.code.toString(16).padStart(4, '0'))
                    } else if (Character.isHighSurrogate(ch)) {
                        out.append(ch)
                        out.append(value[index + 1])
                        index += 1
                    } else {
                        out.append(ch)
                    }
                }
            }
            index += 1
        }
        out.append('"')
        return out.toString()
    }

    private fun validateUnicode(value: String) {
        var index = 0
        while (index < value.length) {
            val ch = value[index]
            when {
                Character.isHighSurrogate(ch) -> {
                    if (index + 1 >= value.length || !Character.isLowSurrogate(value[index + 1])) {
                        throw CanonicalizationException("lone high surrogate")
                    }
                    index += 2
                }
                Character.isLowSurrogate(ch) -> throw CanonicalizationException("lone low surrogate")
                else -> index += 1
            }
        }
    }
}

private class DuplicateKeyParser(private val source: String) {
    private var index = 0

    fun parseDocument() {
        skipWhitespace()
        parseValue()
        skipWhitespace()
        if (index != source.length) fail("trailing data")
    }

    private fun parseValue() {
        skipWhitespace()
        if (index >= source.length) fail("unexpected end")
        when (source[index]) {
            '{' -> parseObject()
            '[' -> parseArray()
            '"' -> parseString()
            't' -> expectLiteral("true")
            'f' -> expectLiteral("false")
            'n' -> expectLiteral("null")
            '-', in '0'..'9' -> parseNumber()
            else -> fail("invalid value")
        }
    }

    private fun parseObject() {
        expect('{')
        skipWhitespace()
        val keys = mutableSetOf<String>()
        if (consume('}')) return
        while (true) {
            skipWhitespace()
            val key = parseString()
            if (!keys.add(key)) throw CanonicalizationException("duplicate object key: $key")
            skipWhitespace()
            expect(':')
            parseValue()
            skipWhitespace()
            if (consume('}')) return
            expect(',')
        }
    }

    private fun parseArray() {
        expect('[')
        skipWhitespace()
        if (consume(']')) return
        while (true) {
            parseValue()
            skipWhitespace()
            if (consume(']')) return
            expect(',')
        }
    }

    private fun parseString(): String {
        expect('"')
        val out = StringBuilder()
        while (index < source.length) {
            val ch = source[index++]
            when (ch) {
                '"' -> return out.toString()
                '\\' -> {
                    if (index >= source.length) fail("bad escape")
                    when (val escaped = source[index++]) {
                        '"', '\\', '/' -> out.append(escaped)
                        'b' -> out.append('\b')
                        'f' -> out.append('\u000C')
                        'n' -> out.append('\n')
                        'r' -> out.append('\r')
                        't' -> out.append('\t')
                        'u' -> out.append(parseUnicodeEscape())
                        else -> fail("bad escape")
                    }
                }
                else -> {
                    if (ch.code < 0x20) fail("control in string")
                    out.append(ch)
                }
            }
        }
        fail("unterminated string")
    }

    private fun parseUnicodeEscape(): Char {
        if (index + 4 > source.length) fail("short unicode escape")
        val hex = source.substring(index, index + 4)
        if (!hex.all { it in '0'..'9' || it in 'a'..'f' || it in 'A'..'F' }) fail("bad unicode escape")
        index += 4
        return hex.toInt(16).toChar()
    }

    private fun parseNumber() {
        if (consume('-') && index >= source.length) fail("bad number")
        if (consume('0')) {
            // zero prefix handled by the following delimiter check.
        } else {
            if (index >= source.length || source[index] !in '1'..'9') fail("bad number")
            while (index < source.length && source[index].isDigit()) index++
        }
        if (index < source.length && source[index] == '.') {
            index++
            if (index >= source.length || !source[index].isDigit()) fail("bad fraction")
            while (index < source.length && source[index].isDigit()) index++
        }
        if (index < source.length && (source[index] == 'e' || source[index] == 'E')) {
            index++
            if (index < source.length && (source[index] == '+' || source[index] == '-')) index++
            if (index >= source.length || !source[index].isDigit()) fail("bad exponent")
            while (index < source.length && source[index].isDigit()) index++
        }
    }

    private fun expectLiteral(literal: String) {
        if (!source.startsWith(literal, index)) fail("bad literal")
        index += literal.length
    }

    private fun skipWhitespace() {
        while (index < source.length && source[index] in charArrayOf(' ', '\n', '\r', '\t')) index++
    }

    private fun expect(expected: Char) {
        if (index >= source.length || source[index] != expected) fail("expected $expected")
        index++
    }

    private fun consume(expected: Char): Boolean {
        if (index < source.length && source[index] == expected) {
            index++
            return true
        }
        return false
    }

    private fun fail(message: String): Nothing = throw CanonicalizationException("invalid JSON at $index: $message")
}
