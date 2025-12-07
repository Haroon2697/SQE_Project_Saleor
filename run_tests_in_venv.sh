#!/bin/bash
# Script to run tests with virtual environment activated

cd "$(dirname "$0")"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please create it first:"
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install ."
    exit 1
fi

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not installed. Installing dependencies..."
    pip install .
fi

# Run tests
echo "🧪 Running tests..."
if [ "$1" == "--coverage" ] || [ "$1" == "-c" ]; then
    echo "📊 Running with coverage report..."
    python -m pytest tests/ "${@:2}" --cov=saleor --cov-report=html --cov-report=term
    echo ""
    echo "✅ Coverage report generated at: htmlcov/index.html"
elif [ "$1" == "--new" ] || [ "$1" == "-n" ]; then
    echo "🧪 Running new extensive tests..."
    python -m pytest tests/whitebox/test_checkout_calculations_extensive.py \
                   tests/whitebox/test_checkout_actions_extensive.py \
                   tests/whitebox/test_webhook_utils_extensive.py \
                   "${@:2}" -v
else
    python -m pytest tests/ "${@}" -v
fi

