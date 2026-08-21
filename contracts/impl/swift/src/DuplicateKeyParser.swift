struct DuplicateKeyParser {
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
                case "u": output += try parseUnicodeEscapeSequence()
                default: throw error("bad escape")
                }
            } else {
                guard scalar.value >= 0x20 else { throw error("control in string") }
                output.unicodeScalars.append(scalar)
            }
        }
        throw error("unterminated string")
    }

    private mutating func parseUnicodeEscapeSequence() throws -> String {
        let first = try readUnicodeCodeUnit()
        if first >= 0xD800 && first <= 0xDBFF {
            guard consume("\\"), consume("u") else { throw error("high surrogate without low surrogate") }
            let second = try readUnicodeCodeUnit()
            guard second >= 0xDC00 && second <= 0xDFFF else { throw error("invalid low surrogate") }
            let scalarValue = 0x10000 + ((first - 0xD800) << 10) + (second - 0xDC00)
            guard let scalar = UnicodeScalar(scalarValue) else { throw error("invalid surrogate pair") }
            return String(scalar)
        }
        if first >= 0xDC00 && first <= 0xDFFF {
            throw error("lone low surrogate")
        }
        guard let scalar = UnicodeScalar(first) else { throw error("bad unicode escape") }
        return String(scalar)
    }

    private mutating func readUnicodeCodeUnit() throws -> UInt32 {
        guard index + 4 <= scalars.count else { throw error("short unicode escape") }
        let text = String(String.UnicodeScalarView(scalars[index..<(index + 4)]))
        guard let value = UInt32(text, radix: 16) else { throw error("bad unicode escape") }
        index += 4
        return value
    }

    private mutating func parseNumber() throws {
        _ = consume("-")
        guard index < scalars.count else { throw error("bad number") }
        if consume("0") {
            if index < scalars.count && isDigit(scalars[index]) { throw error("leading zero") }
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
