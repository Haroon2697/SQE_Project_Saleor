#!/bin/bash
cd /home/haroon/SQE/SQE_Project_Saleor
source .venv/bin/activate

echo "Running tests..."
pytest tests/whitebox/test_core_utils_coverage.py \
    tests/whitebox/test_exceptions_coverage.py \
    tests/whitebox/test_core_weight_coverage.py \
    tests/whitebox/test_url_utils_coverage.py \
    tests/whitebox/test_validators_coverage.py \
    tests/whitebox/test_promo_code_coverage.py \
    tests/whitebox/test_shipping_interface_coverage.py \
    tests/whitebox/test_discount_interface_coverage.py \
    --override-ini="addopts=" \
    --cov=saleor \
    --cov-report=term \
    -v

echo "Tests completed."

