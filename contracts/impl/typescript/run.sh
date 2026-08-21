#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
rm -rf "$ROOT/build"
tsc -p "$ROOT/tsconfig.json"
node "$ROOT/build/tests/test.js"
rm -rf "$ROOT/build"
