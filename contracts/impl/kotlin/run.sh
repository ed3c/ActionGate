#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD="$ROOT/build"
rm -rf "$BUILD"
mkdir -p "$BUILD"
kotlinc "$ROOT/src/ActionGateCanonical.kt" "$ROOT/tests/CanonicalizerTest.kt" -include-runtime -d "$BUILD/c01-kotlin-tests.jar"
java -jar "$BUILD/c01-kotlin-tests.jar"
rm -rf "$BUILD"
