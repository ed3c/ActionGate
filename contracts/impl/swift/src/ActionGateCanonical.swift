import Foundation
import CoreFoundation

enum CanonicalizationError: Error, CustomStringConvertible {
    case invalid(String)

    var description: String {
        switch self {
        case .invalid(let message): return message
        }
    }
}

private let maxSafeInteger: Int64 = 9_007_199_254_740_991
private let keyPattern = try! NSRegularExpression(pattern: "^[A-Za-z0-9_.:-]+$")

indirect enum CanonicalValue {
    case null
    case bool(Bool)
    case integer(Int64)
    case text(String)
    case array([CanonicalValue])
    case object([String: CanonicalValue])
}

enum ActionGateCanonical {
    static func canonicalData(_ value: Any?) throws -> Data {
        Data(try encode(fromAny(value)).utf8)
    }

    static func canonicalString(_ value: Any?) throws -> String {
        try encode(fromAny(value))
    }

    static func digestBase64URL(domain: String, value: Any?) throws -> String {
        guard domain.utf8.last == 0 else {
            throw CanonicalizationError.invalid("domain must end with NUL")
        }
        var bytes = Array(domain.utf8)
        bytes.append(contentsOf: try canonicalData(value))
        return base64URL(SHA256.hash(bytes))
    }

    static func authorizationSigningInput(_ challenge: Any?) throws -> [UInt8] {
        var bytes = Array("ActionGate-AuthorizationChallenge-v1\0".utf8)
        bytes.append(contentsOf: try canonicalData(challenge))
        return bytes
    }

    static func sha256Base64URL(_ bytes: [UInt8]) -> String {
        base64URL(SHA256.hash(bytes))
    }

    static func assertNoDuplicateKeys(_ raw: String) throws {
        var parser = DuplicateKeyParser(raw)
        try parser.parseDocument()
    }

    private static func fromAny(_ value: Any?) throws -> CanonicalValue {
        guard let value else { return .null }
        if let string = value as? String { return .text(string) }

        if let number = value as? NSNumber {
            if CFGetTypeID(number) == CFBooleanGetTypeID() {
                return .bool(number.boolValue)
            }
            let type = String(cString: number.objCType)
            switch type {
            case "c", "s", "i", "l", "q":
                return try checkedInteger(number.int64Value)
            case "C", "S", "I", "L", "Q":
                let unsigned = number.uint64Value
                guard unsigned <= UInt64(maxSafeInteger) else {
                    throw CanonicalizationError.invalid("integer outside safe range")
                }
                return .integer(Int64(unsigned))
            default:
                throw CanonicalizationError.invalid("floating point is forbidden")
            }
        }

        switch value {
        case let integer as Int: return try checkedInteger(Int64(integer))
        case let integer as Int8: return try checkedInteger(Int64(integer))
        case let integer as Int16: return try checkedInteger(Int64(integer))
        case let integer as Int32: return try checkedInteger(Int64(integer))
        case let integer as Int64: return try checkedInteger(integer)
        case let integer as UInt where integer <= UInt(maxSafeInteger): return .integer(Int64(integer))
        case let integer as UInt8: return .integer(Int64(integer))
        case let integer as UInt16: return .integer(Int64(integer))
        case let integer as UInt32: return .integer(Int64(integer))
        case let integer as UInt64 where integer <= UInt64(maxSafeInteger): return .integer(Int64(integer))
        case is Float, is Double: throw CanonicalizationError.invalid("floating point is forbidden")
        case let array as [Any?]: return .array(try array.map(fromAny))
        case let object as [String: Any?]:
            var converted: [String: CanonicalValue] = [:]
            for (key, item) in object {
                try validateKey(key)
                guard converted[key] == nil else {
                    throw CanonicalizationError.invalid("duplicate object key: \(key)")
                }
                converted[key] = try fromAny(item)
            }
            return .object(converted)
        default:
            throw CanonicalizationError.invalid("unsupported value type: \(type(of: value))")
        }
    }

    private static func checkedInteger(_ value: Int64) throws -> CanonicalValue {
        guard value >= -maxSafeInteger && value <= maxSafeInteger else {
            throw CanonicalizationError.invalid("integer outside safe range")
        }
        return .integer(value)
    }

    private static func validateKey(_ key: String) throws {
        let range = NSRange(key.startIndex..<key.endIndex, in: key)
        guard !key.isEmpty, keyPattern.firstMatch(in: key, range: range) != nil else {
            throw CanonicalizationError.invalid("invalid object key: \(key)")
        }
    }

    private static func encode(_ value: CanonicalValue) throws -> String {
        switch value {
        case .null: return "null"
        case .bool(let value): return value ? "true" : "false"
        case .integer(let value): return String(value)
        case .text(let value): return quote(value)
        case .array(let values): return "[" + (try values.map(encode).joined(separator: ",")) + "]"
        case .object(let values):
            let entries = try values.keys.sorted().map { key -> String in
                try validateKey(key)
                return quote(key) + ":" + (try encode(values[key]!))
            }
            return "{" + entries.joined(separator: ",") + "}"
        }
    }

    private static func quote(_ value: String) -> String {
        var output = "\""
        for scalar in value.unicodeScalars {
            switch scalar.value {
            case 0x22: output += "\\\""
            case 0x5C: output += "\\\\"
            case 0x08: output += "\\b"
            case 0x09: output += "\\t"
            case 0x0A: output += "\\n"
            case 0x0C: output += "\\f"
            case 0x0D: output += "\\r"
            case 0x00...0x1F:
                output += String(format: "\\u%04x", scalar.value)
            default:
                output.unicodeScalars.append(scalar)
            }
        }
        output += "\""
        return output
    }

    private static func base64URL(_ bytes: [UInt8]) -> String {
        Data(bytes).base64EncodedString()
            .replacingOccurrences(of: "+", with: "-")
            .replacingOccurrences(of: "/", with: "_")
            .replacingOccurrences(of: "=", with: "")
    }
}

private enum SHA256 {
    private static let initial: [UInt32] = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    private static let constants: [UInt32] = [
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
    ]

    static func hash(_ input: [UInt8]) -> [UInt8] {
        var message = input
        let bitLength = UInt64(message.count) * 8
        message.append(0x80)
        while message.count % 64 != 56 { message.append(0) }
        for shift in stride(from: 56, through: 0, by: -8) {
            message.append(UInt8((bitLength >> UInt64(shift)) & 0xff))
        }

        var state = initial
        var offset = 0
        while offset < message.count {
            var words = [UInt32](repeating: 0, count: 64)
            for index in 0..<16 {
                let base = offset + index * 4
                words[index] = UInt32(message[base]) << 24 |
                    UInt32(message[base + 1]) << 16 |
                    UInt32(message[base + 2]) << 8 |
                    UInt32(message[base + 3])
            }
            for index in 16..<64 {
                let s0 = rotateRight(words[index - 15], 7) ^ rotateRight(words[index - 15], 18) ^ (words[index - 15] >> 3)
                let s1 = rotateRight(words[index - 2], 17) ^ rotateRight(words[index - 2], 19) ^ (words[index - 2] >> 10)
                words[index] = words[index - 16] &+ s0 &+ words[index - 7] &+ s1
            }

            var a = state[0], b = state[1], c = state[2], d = state[3]
            var e = state[4], f = state[5], g = state[6], h = state[7]
            for index in 0..<64 {
                let sum1 = rotateRight(e, 6) ^ rotateRight(e, 11) ^ rotateRight(e, 25)
                let choice = (e & f) ^ ((~e) & g)
                let temp1 = h &+ sum1 &+ choice &+ constants[index] &+ words[index]
                let sum0 = rotateRight(a, 2) ^ rotateRight(a, 13) ^ rotateRight(a, 22)
                let majority = (a & b) ^ (a & c) ^ (b & c)
                let temp2 = sum0 &+ majority
                h = g; g = f; f = e; e = d &+ temp1
                d = c; c = b; b = a; a = temp1 &+ temp2
            }
            state[0] &+= a; state[1] &+= b; state[2] &+= c; state[3] &+= d
            state[4] &+= e; state[5] &+= f; state[6] &+= g; state[7] &+= h
            offset += 64
        }

        return state.flatMap { value in
            [UInt8((value >> 24) & 0xff), UInt8((value >> 16) & 0xff), UInt8((value >> 8) & 0xff), UInt8(value & 0xff)]
        }
    }

    private static func rotateRight(_ value: UInt32, _ count: UInt32) -> UInt32 {
        (value >> count) | (value << (32 - count))
    }
}

private struct DuplicateKeyParser {
    private let scalars: [UnicodeScalar]
    private var index = 0

    init(_ source: String) {
        self.scalars = Array(source.unicodeScalars)
    }

    mutating func parseDocument() throws {
        skipWhitespace()
        try parseValue()
        skipWhitespace()
        guard index == scalars.count else { throw error("trailing data") }
    }

    private mutating func parseValue() throws {
        skipWhitespace()
        guard index < scalars.count else { throw error("unexpected end") }
        switch scalars[index].value {
        case 0x7B: try parseObject()
        case 0x5B: try parseArray()
        case 0x22: _ = try parseString()
        case 0x74: try expectLiteral("true")
        case 0x66: try expectLiteral("false")
        case 0x6E: try expectLiteral("null")
        case 0x2D, 0x30...0x39: try parseNumber()
        default: throw error("invalid value")
        }
    }

    private mutating func parseObject() throws {
        try expect("{")
        skipWhitespace()
        var keys = Set<String>()
        if consume("}") { return }
        while true {
            skipWhitespace()
            let key = try parseString()
            guard keys.insert(key).inserted else {
                throw CanonicalizationError.invalid("duplicate object key: \(key)")
            }
            skipWhitespace()
            try expect(":")
            try parseValue()
            skipWhitespace()
            if consume("}") { return }
            try expect(",")
        }
    }

    private mutating func parseArray() throws {
        try expect("[")
        skipWhitespace()
        if consume("]") { return }
        while true {
            try parseValue()
            skipWhitespace()
            if consume("]") { return }
            try expect(",")
        }
    }

    private mutating func parseString() throws -> String {
        try expect("\"")
        var output = ""
        while index < scalars.count {
            let scalar = scalars[index]
            index += 1
            if scalar == "\"" { return output }
            if scalar == "\\" {
                guard index < scalars.count else { throw error("bad escape") }
                let escaped = scalars[index]
                index += 1
                switch escaped {
                case "\"", "\\", "/": output.unicodeScalars.append(escaped)
                case "b": output.append("\u{8}")
                case "f": output.append("\u{C}")
                case "n": output.append("\n")
                case "r": output.append("\r")
                case "t": output.append("\t")
                case "u": output.unicodeScalars.append(try parseUnicodeEscape())
                default: throw error("bad escape")
                }
            } else {
                guard scalar.value >= 0x20 else { throw error("control in string") }
                output.unicodeScalars.append(scalar)
            }
        }
        throw error("unterminated string")
    }

    private mutating func parseUnicodeEscape() throws -> UnicodeScalar {
        guard index + 4 <= scalars.count else { throw error("short unicode escape") }
        let text = String(String.UnicodeScalarView(scalars[index..<(index + 4)]))
        guard let value = UInt32(text, radix: 16), let scalar = UnicodeScalar(value) else { throw error("bad unicode escape") }
        index += 4
        return scalar
    }

    private mutating func parseNumber() throws {
        _ = consume("-")
        guard index < scalars.count else { throw error("bad number") }
        if consume("0") {
            // zero prefix accepted only as this single digit before suffix.
        } else {
            guard isDigit(scalars[index]), scalars[index] != "0" else { throw error("bad number") }
            while index < scalars.count && isDigit(scalars[index]) { index += 1 }
        }
        if consume(".") {
            guard index < scalars.count && isDigit(scalars[index]) else { throw error("bad fraction") }
            while index < scalars.count && isDigit(scalars[index]) { index += 1 }
        }
        if index < scalars.count && (scalars[index] == "e" || scalars[index] == "E") {
            index += 1
            if index < scalars.count && (scalars[index] == "+" || scalars[index] == "-") { index += 1 }
            guard index < scalars.count && isDigit(scalars[index]) else { throw error("bad exponent") }
            while index < scalars.count && isDigit(scalars[index]) { index += 1 }
        }
    }

    private mutating func expectLiteral(_ literal: String) throws {
        for scalar in literal.unicodeScalars { try expect(scalar) }
    }

    private mutating func skipWhitespace() {
        while index < scalars.count && [" ", "\n", "\r", "\t"].contains(scalars[index]) { index += 1 }
    }

    private mutating func expect(_ expected: UnicodeScalar) throws {
        guard index < scalars.count && scalars[index] == expected else { throw error("expected \(expected)") }
        index += 1
    }

    private mutating func consume(_ expected: UnicodeScalar) -> Bool {
        guard index < scalars.count && scalars[index] == expected else { return false }
        index += 1
        return true
    }

    private func isDigit(_ scalar: UnicodeScalar) -> Bool { scalar.value >= 0x30 && scalar.value <= 0x39 }
    private func error(_ message: String) -> CanonicalizationError { .invalid("invalid JSON at \(index): \(message)") }
}
