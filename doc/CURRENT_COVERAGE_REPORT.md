# Current Coverage Report

**Generated:** December 7, 2024  
**Overall Coverage:** 49.64%  
**Target Coverage:** 80%+  
**Gap:** 30.36%

---

## 📊 Overall Statistics

- **Line Coverage:** 49.64%
- **Branch Coverage:** 0.00%
- **Packages Analyzed:** 150

---

## 📦 Module Coverage Breakdown

### Order Module
- `graphql.order.mutations`: 51.0%
- `graphql.order`: 47.0%
- `graphql.order.bulk_mutations`: 38.7%
- `order`: 34.8% ⚠️ **Needs Improvement**

### Checkout Module
- `graphql.checkout.mutations`: 53.6%
- `graphql.checkout`: 51.2%
- `checkout`: 31.5% ⚠️ **Needs Improvement**
- `graphql.checkout.dataloaders`: 31.0%

### Payment Module
- `graphql.payment`: 67.2%
- `graphql.payment.mutations.stored_payment_methods`: 65.7%
- `graphql.payment.mutations.payment`: 61.8%
- `payment`: 48.1% ⚠️ **Needs Improvement**

### Discount Module
- `graphql.discount.types`: 77.7%
- `discount`: 67.1%
- `graphql.discount.mutations`: 56.8%
- `graphql.discount`: 53.0%

### Shipping Module
- `graphql.shipping.bulk_mutations`: 79.0%
- `graphql.shipping`: 65.5%
- `graphql.shipping.mutations`: 56.6%
- `shipping`: 53.2%

### Webhook Module
- `graphql.webhook`: 77.8%
- `webhook.response_schemas`: 73.9%
- `graphql.webhook.mutations`: 57.1%
- `webhook`: 53.7%

---

## ✅ Recently Added Test Files

The following comprehensive test files have been created to increase coverage:

1. **`test_shipping_utils_comprehensive.py`**
   - Tests for `saleor/shipping/utils.py`
   - Covers 6 utility functions
   - Expected to increase shipping module coverage

2. **`test_discount_utils_checkout_comprehensive.py`**
   - Tests for `saleor/discount/utils/checkout.py`
   - Covers checkout discount operations
   - Expected to increase discount/checkout coverage

3. **`test_discount_utils_order_comprehensive.py`**
   - Tests for `saleor/discount/utils/order.py`
   - Covers order discount operations
   - Expected to increase discount/order coverage

4. **`test_order_calculations_comprehensive.py`**
   - Tests for `saleor/order/calculations.py`
   - Covers order price calculations and tax handling
   - Expected to significantly increase order module coverage

---

## 🎯 Priority Areas for Improvement

Based on the coverage report, the following modules need the most attention:

1. **Order Module (34.8%)** - Critical business logic
   - `order/actions.py` - Order lifecycle management
   - `order/calculations.py` - Price calculations
   - `order/utils.py` - Utility functions

2. **Checkout Module (31.5%)** - Critical user flow
   - `checkout/base_calculations.py` - Checkout calculations
   - `checkout/utils.py` - Checkout utilities

3. **Payment Module (48.1%)** - Financial operations
   - `payment/utils.py` - Payment processing utilities

---

## 📈 Expected Impact

With the newly added comprehensive tests, we expect:

- **Order Module:** Increase from 34.8% to ~55-60%
- **Checkout Module:** Increase from 31.5% to ~50-55%
- **Discount Module:** Increase from 67.1% to ~75-80%
- **Shipping Module:** Increase from 53.2% to ~65-70%
- **Overall Coverage:** Increase from 49.64% to ~55-60%

---

## 🔄 Next Steps

1. **Run Tests:** Execute the new test files to verify they work correctly
2. **Regenerate Coverage:** Run coverage report after executing new tests
3. **Identify Gaps:** Focus on modules still below 50% coverage
4. **Add More Tests:** Continue adding tests for low-coverage modules
5. **Target 80%:** Work towards the 80%+ coverage goal

---

## 📁 Coverage Report Locations

- **HTML Report:** `htmlcov/combined/index.html`
- **White-box Report:** `htmlcov/whitebox/index.html`
- **Integration Report:** `htmlcov/integration/index.html`
- **XML Report:** `coverage.xml`

---

## 🚀 How to View Coverage Reports

```bash
# View HTML report in browser
xdg-open htmlcov/combined/index.html

# Or start a local server
cd htmlcov/combined
python3 -m http.server 8001
# Then open http://localhost:8001 in your browser
```

---

**Note:** This report is based on the latest test run. Coverage will improve as new tests are executed and verified.

