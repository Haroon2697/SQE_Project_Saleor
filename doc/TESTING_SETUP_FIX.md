# Testing Setup Fix

## Issue
When running `pytest tests/ --cov=saleor --cov-report=html`, you get:
```
ModuleNotFoundError: No module named 'django'
```

## Solution

### Option 1: Activate Virtual Environment First (Recommended)

```bash
cd /home/haroon/SQE/SQE_Project_Saleor

# Activate virtual environment
source .venv/bin/activate

# Now run tests
pytest tests/ --cov=saleor --cov-report=html
```

### Option 2: Use the Helper Script

I've created a helper script that automatically activates the virtual environment:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor

# Run all tests
./run_tests_in_venv.sh

# Run with coverage
./run_tests_in_venv.sh --coverage

# Run only new extensive tests
./run_tests_in_venv.sh --new
```

### Option 3: Fix pytest Configuration Issue

If you see errors about `--record-mode=none`, you can override the pytest config:

```bash
source .venv/bin/activate
pytest tests/ --override-ini="addopts=-v --ds=saleor.tests.settings" --cov=saleor --cov-report=html
```

## Quick Test Commands

### Test New Extensive Test Files

```bash
source .venv/bin/activate

# Test checkout calculations
pytest tests/whitebox/test_checkout_calculations_extensive.py -v --override-ini="addopts=-v" --ds=saleor.tests.settings

# Test checkout actions
pytest tests/whitebox/test_checkout_actions_extensive.py -v --override-ini="addopts=-v" --ds=saleor.tests.settings

# Test webhook utils
pytest tests/whitebox/test_webhook_utils_extensive.py -v --override-ini="addopts=-v" --ds=saleor.tests.settings
```

### Run All Tests with Coverage

```bash
source .venv/bin/activate
pytest tests/ --override-ini="addopts=-v --ds=saleor.tests.settings" --cov=saleor --cov-report=html --cov-report=term
```

## Verify Setup

```bash
source .venv/bin/activate
python -c "import django; print(f'Django {django.__version__} installed')"
python -c "import pytest; print(f'pytest {pytest.__version__} installed')"
```

## Expected Output

After running tests, you should see:
- Test results with pass/fail status
- Coverage report in terminal
- HTML coverage report at `htmlcov/index.html`

## Troubleshooting

1. **If virtual environment doesn't exist:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install .
   ```

2. **If Django is not installed:**
   ```bash
   source .venv/bin/activate
   pip install .
   ```

3. **If pytest options cause issues:**
   Use `--override-ini="addopts=-v"` to override problematic options

