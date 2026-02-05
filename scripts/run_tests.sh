#!/usr/bin/env bash
# Run Python unit tests and/or Playwright browser tests.
#
# Usage:
#   bash scripts/run_tests.sh          # run all tests
#   bash scripts/run_tests.sh python   # Python unit tests only
#   bash scripts/run_tests.sh e2e      # Playwright browser tests only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

MODE="${1:-all}"

run_python() {
    echo "=== Running Python unit tests ==="
    uv run pytest tests/unit/ --verbose
    echo ""
}

run_e2e() {
    echo "=== Running Playwright browser tests ==="
    uv run pytest tests/e2e/ --verbose
    echo ""
}

case "$MODE" in
    python)
        run_python
        ;;
    e2e)
        run_e2e
        ;;
    all)
        run_python
        run_e2e
        ;;
    *)
        echo "Usage: $0 [python|e2e|all]"
        exit 1
        ;;
esac

echo "=== All tests complete ==="
