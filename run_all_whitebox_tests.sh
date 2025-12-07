#!/bin/bash

# Comprehensive White-Box Test Runner
# Runs all white-box tests and generates coverage reports

# Ensure we are in the project root
cd /home/haroon/SQE/SQE_Project_Saleor

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found at .venv/bin/activate"
    exit 1
fi

# Create coverage directories
mkdir -p htmlcov htmlcov/whitebox htmlcov/integration || true

echo "🧪 Running all white-box tests with coverage..."
echo ""

# Run pytest with coverage for all white-box tests
# --override-ini="addopts=": Overrides any addopts in setup.cfg that might conflict
pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=html:htmlcov/whitebox \
    --cov-report=term \
    --cov-report=term-missing \
    --cov-report=xml:coverage-whitebox.xml \
    -v \
    --tb=short \
    --override-ini="addopts="

echo ""
echo "✅ Test execution complete!"
echo ""
echo "📊 Coverage reports generated:"
echo "  - HTML: htmlcov/whitebox/index.html"
echo "  - XML:  coverage-whitebox.xml"
echo ""
echo "📈 To view HTML coverage report:"
echo "  open htmlcov/whitebox/index.html"

