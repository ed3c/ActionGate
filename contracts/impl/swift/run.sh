#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD="$ROOT/build"
rm -rf "$BUILD"
mkdir -p "$BUILD"
swiftc "$ROOT/src/ActionGateCanonical.swift" "$ROOT/tests/main.swift" -o "$BUILD/c01-swift-tests"
"$BUILD/c01-swift-tests"
rm -rf "$BUILD"
