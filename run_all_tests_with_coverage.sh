#!/bin/bash

# ============================================
# Run All Tests and Generate HTML Coverage Report
# ============================================

set -e  # Exit on error

# Ensure we are in the project root
cd /home/haroon/SQE/SQE_Project_Saleor

echo "🚀 Starting comprehensive test run with coverage..."
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

# Ensure coverage directories exist
mkdir -p htmlcov htmlcov/whitebox htmlcov/integration htmlcov/combined || true

echo ""
echo "📊 Step 1: Running White-box Tests (Unit Tests)..."
echo "=================================================="
pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=html:htmlcov/whitebox \
    --cov-report=term \
    --cov-report=term-missing \
    --cov-report=xml:coverage-whitebox.xml \
    -v \
    --tb=short \
    --override-ini="addopts=" || echo "⚠️  White-box tests completed with some failures"

echo ""
echo "📊 Step 2: Running Integration Tests (Black-box API)..."
echo "======================================================"
pytest tests/integration/ \
    --cov=saleor \
    --cov-append \
    --cov-report=html:htmlcov/integration \
    --cov-report=term \
    --cov-report=term-missing \
    --cov-report=xml:coverage-integration.xml \
    -v \
    --tb=short \
    --override-ini="addopts=" || echo "⚠️  Integration tests completed with some failures"

echo ""
echo "📊 Step 3: Running Unit Tests..."
echo "================================="
pytest tests/unit/ \
    --cov=saleor \
    --cov-append \
    --cov-report=term \
    --cov-report=term-missing \
    -v \
    --tb=short \
    --override-ini="addopts=" || echo "⚠️  Unit tests completed with some failures"

echo ""
echo "📊 Step 4: Running Basic Tests..."
echo "=================================="
pytest tests/test_basic.py \
    --cov=saleor \
    --cov-append \
    --cov-report=term \
    --cov-report=term-missing \
    -v \
    --tb=short \
    --override-ini="addopts=" || echo "⚠️  Basic tests completed with some failures"

echo ""
echo "📊 Step 5: Generating Combined Coverage Report..."
echo "================================================"
pytest tests/ \
    --cov=saleor \
    --cov-report=html:htmlcov/combined \
    --cov-report=term \
    --cov-report=term-missing \
    --cov-report=xml:coverage.xml \
    -v \
    --tb=short \
    --override-ini="addopts=" || echo "⚠️  Combined tests completed with some failures"

echo ""
echo "📈 Step 6: Generating Coverage Summary..."
echo "=========================================="
python -m coverage report --skip-covered || echo "⚠️  Coverage report generation completed with warnings"

echo ""
echo "✅ Test execution complete!"
echo ""
echo "📊 Coverage Reports Generated:"
echo "   📁 htmlcov/whitebox/index.html      - White-box test coverage"
echo "   📁 htmlcov/integration/index.html   - Integration test coverage"
echo "   📁 htmlcov/combined/index.html      - Combined coverage (ALL TESTS)"
echo "   📁 coverage.xml                     - XML coverage report"
echo ""
echo "🌐 To view HTML coverage reports, open:"
echo "   file:///home/haroon/SQE/SQE_Project_Saleor/htmlcov/combined/index.html"
echo ""
echo "📈 Coverage Summary:"
python -m coverage report --skip-covered | tail -1 || echo "Coverage summary unavailable"

