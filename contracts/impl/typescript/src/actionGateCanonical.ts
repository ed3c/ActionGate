declare function require(name: string): any;
declare const Buffer: any;

const { createHash } = require("node:crypto");

const MAX_SAFE_INTEGER = 9_007_199_254_740_991;
const KEY_PATTERN = /^[A-Za-z0-9_.:-]+$/;
const ARRAY_INDEX_PATTERN = /^(0|[1-9][0-9]*)$/;

export class CanonicalizationError extends Error {}

export type CanonicalValue =
  | null
  | boolean
  | number
  | string
  | CanonicalValue[]
  | { readonly [key: string]: CanonicalValue };

export function canonicalString(value: unknown): string {
  return encode(validate(value, "$", new WeakSet<object>()));
}

export function canonicalBytes(value: unknown): Uint8Array {
  return Buffer.from(canonicalString(value), "utf8");
}

export function digestBase64Url(domain: string, value: unknown): string {
  const domainBytes = exactAsciiDomainBytes(domain);
  return createHash("sha256")
    .update(domainBytes)
    .update(Buffer.from(canonicalBytes(value)))
    .digest("base64url");
}

export function authorizationSigningInput(challenge: unknown): Uint8Array {
  return Buffer.concat([
    exactAsciiDomainBytes("ActionGate-AuthorizationChallenge-v1\0"),
    Buffer.from(canonicalBytes(challenge)),
  ]);
}

export function sha256Base64Url(bytes: Uint8Array): string {
  return createHash("sha256").update(Buffer.from(bytes)).digest("base64url");
}

export function assertNoDuplicateKeys(raw: string): void {
  new DuplicateKeyParser(raw).parseDocument();
}

function exactAsciiDomainBytes(domain: string): Uint8Array {
  if (domain.length === 0 || domain.charCodeAt(domain.length - 1) !== 0) {
    throw new CanonicalizationError("domain must end with NUL");
  }
  for (let index = 0; index < domain.length; index += 1) {
    if (domain.charCodeAt(index) > 0x7f) {
      throw new CanonicalizationError("domain must contain exact ASCII bytes");
    }
  }
  return Buffer.from(domain, "ascii");
}

function validate(value: unknown, path: string, active: WeakSet<object>): CanonicalValue {
  if (value === null) return null;
  switch (typeof value) {
    case "boolean":
      return value;
    case "number":
      if (!Number.isSafeInteger(value) || value < -MAX_SAFE_INTEGER || value > MAX_SAFE_INTEGER) {
        throw new CanonicalizationError(`number is not a safe integer at ${path}`);
      }
      return value;
    case "string":
      validateUnicode(value, path);
      return value;
    case "object":
      if (active.has(value)) throw new CanonicalizationError(`cyclic container at ${path}`);
      active.add(value);
      try {
        if (Array.isArray(value)) {
          return validateArray(value, path, active);
        }
        return validateObject(value, path, active);
      } finally {
        active.delete(value);
      }
    default:
      throw new CanonicalizationError(`unsupported type ${typeof value} at ${path}`);
  }
}

function validateArray(value: unknown[], path: string, active: WeakSet<object>): CanonicalValue[] {
  const allowedKeys = new Set<string>(["length"]);
  const result: CanonicalValue[] = [];
  for (let index = 0; index < value.length; index += 1) {
    const key = String(index);
    allowedKeys.add(key);
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor || !descriptor.enumerable || !("value" in descriptor)) {
      throw new CanonicalizationError(`sparse or accessor array element at ${path}[${index}]`);
    }
    result.push(validate(descriptor.value, `${path}[${index}]`, active));
  }
  for (const ownKey of Reflect.ownKeys(value)) {
    if (typeof ownKey !== "string") {
      throw new CanonicalizationError(`symbol array property at ${path}`);
    }
    if (!allowedKeys.has(ownKey)) {
      if (!ARRAY_INDEX_PATTERN.test(ownKey)) {
        throw new CanonicalizationError(`extra array property ${ownKey} at ${path}`);
      }
      throw new CanonicalizationError(`out-of-range array property ${ownKey} at ${path}`);
    }
  }
  return result;
}

function validateObject(value: object, path: string, active: WeakSet<object>): CanonicalValue {
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) {
    throw new CanonicalizationError(`unsupported object at ${path}`);
  }
  const result: Record<string, CanonicalValue> = Object.create(null);
  for (const ownKey of Reflect.ownKeys(value)) {
    if (typeof ownKey !== "string") {
      throw new CanonicalizationError(`symbol object key at ${path}`);
    }
    if (!KEY_PATTERN.test(ownKey)) {
      throw new CanonicalizationError(`invalid key ${ownKey} at ${path}`);
    }
    const descriptor = Object.getOwnPropertyDescriptor(value, ownKey);
    if (!descriptor || !descriptor.enumerable || !("value" in descriptor)) {
      throw new CanonicalizationError(`non-data or non-enumerable property ${ownKey} at ${path}`);
    }
    if (Object.prototype.hasOwnProperty.call(result, ownKey)) {
      throw new CanonicalizationError(`duplicate key ${ownKey} at ${path}`);
    }
    result[ownKey] = validate(descriptor.value, `${path}.${ownKey}`, active);
  }
  return result;
}

function encode(value: CanonicalValue): string {
  if (value === null) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return String(value);
  if (typeof value === "string") return quote(value);
  if (Array.isArray(value)) return `[${value.map(encode).join(",")}]`;
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${quote(key)}:${encode(value[key])}`)
    .join(",")}}`;
}

function quote(value: string): string {
  validateUnicode(value, "$string");
  let output = '"';
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    switch (code) {
      case 0x22:
        output += '\\"';
        break;
      case 0x5c:
        output += "\\\\";
        break;
      case 0x08:
        output += "\\b";
        break;
      case 0x09:
        output += "\\t";
        break;
      case 0x0a:
        output += "\\n";
        break;
      case 0x0c:
        output += "\\f";
        break;
      case 0x0d:
        output += "\\r";
        break;
      default:
        if (code < 0x20) {
          output += `\\u${code.toString(16).padStart(4, "0")}`;
        } else if (code >= 0xd800 && code <= 0xdbff) {
          output += value[index] + value[index + 1];
          index += 1;
        } else {
          output += value[index];
        }
    }
  }
  return `${output}"`;
}

function validateUnicode(value: string, path: string): void {
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    if (code >= 0xd800 && code <= 0xdbff) {
      if (index + 1 >= value.length) throw new CanonicalizationError(`lone high surrogate at ${path}`);
      const low = value.charCodeAt(index + 1);
      if (low < 0xdc00 || low > 0xdfff) throw new CanonicalizationError(`lone high surrogate at ${path}`);
      index += 1;
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      throw new CanonicalizationError(`lone low surrogate at ${path}`);
    }
  }
}

class DuplicateKeyParser {
  private index = 0;

  constructor(private readonly source: string) {}

  parseDocument(): void {
    this.skipWhitespace();
    this.parseValue();
    this.skipWhitespace();
    if (this.index !== this.source.length) this.fail("trailing data");
  }

  private parseValue(): void {
    this.skipWhitespace();
    const token = this.source[this.index];
    if (token === undefined) this.fail("unexpected end");
    if (token === "{") this.parseObject();
    else if (token === "[") this.parseArray();
    else if (token === '"') this.parseString();
    else if (token === "t") this.expectLiteral("true");
    else if (token === "f") this.expectLiteral("false");
    else if (token === "n") this.expectLiteral("null");
    else if (token === "-" || /[0-9]/.test(token)) this.parseNumber();
    else this.fail("invalid value");
  }

  private parseObject(): void {
    this.expect("{");
    this.skipWhitespace();
    const keys = new Set<string>();
    if (this.consume("}")) return;
    while (true) {
      this.skipWhitespace();
      const key = this.parseString();
      if (keys.has(key)) throw new CanonicalizationError(`duplicate object key: ${key}`);
      keys.add(key);
      this.skipWhitespace();
      this.expect(":");
      this.parseValue();
      this.skipWhitespace();
      if (this.consume("}")) return;
      this.expect(",");
    }
  }

  private parseArray(): void {
    this.expect("[");
    this.skipWhitespace();
    if (this.consume("]")) return;
    while (true) {
      this.parseValue();
      this.skipWhitespace();
      if (this.consume("]")) return;
      this.expect(",");
    }
  }

  private parseString(): string {
    this.expect('"');
    let output = "";
    while (this.index < this.source.length) {
      const char = this.source[this.index++];
      if (char === '"') {
        validateUnicode(output, "$raw-string");
        return output;
      }
      if (char === "\\") {
        const escaped = this.source[this.index++];
        if (escaped === undefined) this.fail("bad escape");
        if ('"\\/'.includes(escaped)) output += escaped;
        else if (escaped === "b") output += "\b";
        else if (escaped === "f") output += "\f";
        else if (escaped === "n") output += "\n";
        else if (escaped === "r") output += "\r";
        else if (escaped === "t") output += "\t";
        else if (escaped === "u") output += this.parseUnicodeEscape();
        else this.fail("bad escape");
      } else {
        if (char.charCodeAt(0) < 0x20) this.fail("control in string");
        output += char;
      }
    }
    return this.fail("unterminated string");
  }

  private parseUnicodeEscape(): string {
    const hex = this.source.slice(this.index, this.index + 4);
    if (!/^[0-9A-Fa-f]{4}$/.test(hex)) this.fail("bad unicode escape");
    this.index += 4;
    return String.fromCharCode(Number.parseInt(hex, 16));
  }

  private parseNumber(): void {
    this.consume("-");
    if (this.consume("0")) {
      if (/[0-9]/.test(this.source[this.index] ?? "")) this.fail("leading zero");
    } else {
      if (!/[1-9]/.test(this.source[this.index] ?? "")) this.fail("bad number");
      while (/[0-9]/.test(this.source[this.index] ?? "")) this.index += 1;
    }
    if (this.consume(".")) {
      if (!/[0-9]/.test(this.source[this.index] ?? "")) this.fail("bad fraction");
      while (/[0-9]/.test(this.source[this.index] ?? "")) this.index += 1;
    }
    if ((this.source[this.index] ?? "").toLowerCase() === "e") {
      this.index += 1;
      if (["+", "-"].includes(this.source[this.index] ?? "")) this.index += 1;
      if (!/[0-9]/.test(this.source[this.index] ?? "")) this.fail("bad exponent");
      while (/[0-9]/.test(this.source[this.index] ?? "")) this.index += 1;
    }
  }

  private expectLiteral(literal: string): void {
    if (!this.source.startsWith(literal, this.index)) this.fail("bad literal");
    this.index += literal.length;
  }

  private skipWhitespace(): void {
    while ([" ", "\n", "\r", "\t"].includes(this.source[this.index] ?? "")) this.index += 1;
  }

  private expect(expected: string): void {
    if (this.source[this.index] !== expected) this.fail(`expected ${expected}`);
    this.index += 1;
  }

  private consume(expected: string): boolean {
    if (this.source[this.index] !== expected) return false;
    this.index += 1;
    return true;
  }

  private fail(message: string): never {
    throw new CanonicalizationError(`invalid JSON at ${this.index}: ${message}`);
  }
}
