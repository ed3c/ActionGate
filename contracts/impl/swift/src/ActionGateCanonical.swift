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
private let argumentsDomain = "ActionGate-Arguments-v1\0"
private let actionEnvelopeDomain = "ActionGate-ActionEnvelope-v1\0"
private let authorizationChallengeDomain = "ActionGate-AuthorizationChallenge-v1\0"
private let digestDomains: Set<String> = [argumentsDomain, actionEnvelopeDomain]

func isValidActionGateKey(_ key: String) -> Bool {
    guard !key.isEmpty else { return false }
    return key.unicodeScalars.allSatisfy { scalar in
        switch scalar.value {
        case 0x41...0x5A, 0x61...0x7A, 0x30...0x39, 0x5F, 0x2E, 0x3A, 0x2D:
            return true
        default:
            return false
        }
    }
}

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
        var bytes = try domainBytes(domain, allowed: digestDomains)
        bytes.append(contentsOf: try canonicalData(value))
        return base64URL(SHA256.hash(bytes))
    }

    static func authorizationSigningInput(_ challenge: Any?) throws -> [UInt8] {
        var bytes = try domainBytes(authorizationChallengeDomain, allowed: [authorizationChallengeDomain])
        bytes.append(contentsOf: try canonicalData(challenge))
        return bytes
    }

    static func sha256Base64URL(_ bytes: [UInt8]) -> String {
        base64URL(SHA256.hash(bytes))
    }

    static func assertCanonicalJsonInput(_ raw: String) throws {
        var parser = RestrictedJSONParser(raw)
        try parser.parseDocument()
    }

    static func assertNoDuplicateKeys(_ raw: String) throws {
        try assertCanonicalJsonInput(raw)
    }

    private static func domainBytes(_ domain: String, allowed: Set<String>) throws -> [UInt8] {
        guard domain.unicodeScalars.allSatisfy({ $0.value <= 0x7f }) else {
            throw CanonicalizationError.invalid("domain must contain exact ASCII bytes")
        }
        let bytes = Array(domain.utf8)
        guard bytes.last == 0 else {
            throw CanonicalizationError.invalid("domain must end with NUL")
        }
        guard allowed.contains(domain) else {
            throw CanonicalizationError.invalid("unregistered domain label")
        }
        return bytes
    }

    private static func fromAny(_ value: Any?) throws -> CanonicalValue {
        guard let value else { return .null }
        if value is NSMutableArray || value is NSMutableDictionary {
            throw CanonicalizationError.invalid("mutable Foundation containers are forbidden")
        }
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
        guard isValidActionGateKey(key) else {
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
