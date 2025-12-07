#!/bin/bash

# ============================================
# Run All Tests and Generate HTML Coverage Report
# ============================================

set -e  # Exit on error

# Ensure we are in the project root
cd /home/haroon/SQE/SQE_Project_Saleor

echo "🚀 Starting comprehensive test run with HTML coverage reports..."
echo ""

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found, using system Python"
fi

# Install dependencies if needed
pip install -q pytest pytest-cov coverage || echo "Dependencies already installed"

# Ensure coverage directories exist
mkdir -p htmlcov htmlcov/whitebox htmlcov/integration htmlcov/combined || true

echo ""
echo "📊 Running All Tests with Coverage..."
echo "====================================="

# Run all tests with coverage and generate HTML reports
pytest tests/ \
    --cov=saleor \
    --cov-report=html:htmlcov/combined \
    --cov-report=term \
    --cov-report=term-missing \
    --cov-report=xml:coverage.xml \
    -v \
    --tb=short \
    --override-ini="addopts=" \
    --junit-xml=junit-tests.xml || echo "⚠️  Some tests may have failed, but continuing..."

echo ""
echo "📊 Running White-box Tests Separately..."
echo "=========================================="

pytest tests/whitebox/ \
    --cov=saleor \
    --cov-append \
    --cov-report=html:htmlcov/whitebox \
    --cov-report=term \
    --cov-report=term-missing \
    -v \
    --tb=short \
    --override-ini="addopts=" || echo "⚠️  White-box tests completed with some failures"

echo ""
echo "📊 Running Integration Tests Separately..."
echo "==========================================="

pytest tests/integration/ \
    --cov=saleor \
    --cov-append \
    --cov-report=html:htmlcov/integration \
    --cov-report=term \
    --cov-report=term-missing \
    -v \
    --tb=short \
    --override-ini="addopts=" || echo "⚠️  Integration tests completed with some failures"

echo ""
echo "📈 Generating Coverage Summary..."
echo "=================================="

python -m coverage report --skip-covered || echo "⚠️  Coverage report generation completed with warnings"

echo ""
echo "✅ Test execution complete!"
echo ""
echo "📊 HTML Coverage Reports Generated:"
echo "   📁 htmlcov/combined/index.html      - Combined coverage (ALL TESTS) ⭐ MAIN REPORT"
echo "   📁 htmlcov/whitebox/index.html     - White-box test coverage"
echo "   📁 htmlcov/integration/index.html   - Integration test coverage"
echo "   📁 coverage.xml                    - XML coverage report (for CI/CD)"
echo ""
echo "🌐 To view HTML coverage reports, open:"
echo "   file://$(pwd)/htmlcov/combined/index.html"
echo ""
echo "📈 Coverage Summary:"
python -m coverage report --skip-covered | tail -1 || echo "Coverage summary unavailable"
echo ""
echo "💡 Tip: Open htmlcov/combined/index.html in your browser to see detailed coverage!"

