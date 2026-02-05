#!/usr/bin/env bash
# Run both Python unit tests and Cypress browser tests.
#
# Usage:
#   bash scripts/run_tests.sh          # run all tests
#   bash scripts/run_tests.sh python   # Python only
#   bash scripts/run_tests.sh cypress  # Cypress only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

MODE="${1:-all}"

run_python() {
    echo "=== Running Python unit tests ==="
    uv run pytest tests/ --verbose
    echo ""
}

run_cypress() {
    echo "=== Generating Cypress fixtures ==="
    uv run python cypress/fixtures/generate_fixtures.py

    echo "=== Running Cypress browser tests ==="
    npm run test:e2e
    echo ""
}

case "$MODE" in
    python)
        run_python
        ;;
    cypress)
        run_cypress
        ;;
    all)
        run_python
        run_cypress
        ;;
    *)
        echo "Usage: $0 [python|cypress|all]"
        exit 1
        ;;
esac

echo "=== All tests complete ==="
