#!/bin/bash

# Quick test runner script for Saleor SQE Project

echo "=========================================="
echo "🧪 RUNNING SALEOR TESTS"
echo "=========================================="
echo

cd "$(dirname "$0")"
source .venv/bin/activate

# Check if pytest is installed
if ! python -m pytest --version > /dev/null 2>&1; then
    echo "⚠️  pytest not found. Installing..."
    pip install pytest pytest-django pytest-cov
fi

# Run tests based on argument
case "$1" in
    unit)
        echo "Running unit tests (white-box)..."
        pytest tests/unit/ -v
        ;;
    integration)
        echo "Running integration tests (black-box)..."
        pytest tests/integration/ -v
        ;;
    basic)
        echo "Running basic tests..."
        pytest tests/test_basic.py -v
        ;;
    coverage)
        echo "Running tests with coverage..."
        pytest --cov=saleor --cov-report=html --cov-report=term tests/
        echo
        echo "📊 Coverage report generated in htmlcov/"
        ;;
    all|"")
        echo "Running all tests..."
        pytest tests/ -v
        ;;
    *)
        echo "Usage: $0 [unit|integration|basic|coverage|all]"
        exit 1
        ;;
esac

echo
echo "=========================================="

