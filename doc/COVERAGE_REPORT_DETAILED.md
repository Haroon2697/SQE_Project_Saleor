# Detailed Coverage Report

**Generated:** December 7, 2025  
**Coverage Tool:** coverage.py v7.12.0  
**Overall Coverage:** 48%

---

## Coverage Statistics

| Metric | Value |
|--------|-------|
| **Total Statements** | 82,616 |
| **Covered** | 42,973 |
| **Missing** | 39,643 |
| **Excluded** | 632 |
| **Coverage** | **48%** |

---

## File-by-File Coverage Report

*Note: Files with 100% coverage are skipped in detailed reports. Only files with <100% coverage are shown below.*

### Format Legend
- **File Path**: Module/file path
- **Statements**: Total number of statements
- **Missing**: Number of statements not covered
- **Excluded**: Number of statements excluded from coverage
- **Coverage**: Percentage of statements covered

---

## Key Modules Needing More Tests

### 🔴 Critical (0-20% Coverage)

| File | Statements | Missing | Coverage |
|------|-----------|---------|----------|
| `saleor/checkout/complete_checkout.py` | 628 | 531 | **15%** |
| `saleor/checkout/tasks.py` | 102 | 102 | **0%** |
| `saleor/app/manifest_validations.py` | 247 | 203 | **18%** |
| `saleor/asgi/gzip_compression.py` | 80 | 74 | **8%** |
| `saleor/asgi/cors_handler.py` | 41 | 35 | **15%** |
| `saleor/asgi/asgi_handler.py` | 54 | 42 | **22%** |
| `saleor/attribute/utils.py` | 100 | 86 | **14%** |
| `saleor/channel/tasks/saleor3_22.py` | 7 | 7 | **0%** |
| `saleor/giftcard/tasks.py` | 28 | 28 | **0%** |
| `saleor/order/actions.py` | 687 | 585 | **15%** |
| `saleor/order/base_calculations.py` | 149 | 121 | **19%** |
| `saleor/payment/tasks.py` | 66 | 66 | **0%** |
| `saleor/warehouse/tasks.py` | 34 | 34 | **0%** |

### 🟡 High Priority (20-40% Coverage)

| File | Statements | Missing | Coverage |
|------|-----------|---------|----------|
| `saleor/checkout/calculations.py` | 262 | 148 | **44%** |
| `saleor/checkout/base_calculations.py` | 107 | 55 | **49%** |
| `saleor/checkout/utils.py` | 531 | 376 | **29%** |
| `saleor/checkout/payment_utils.py` | 67 | 53 | **21%** |
| `saleor/checkout/fetch.py` | 325 | 201 | **38%** |
| `saleor/webhook/utils.py` | 71 | 3 | **96%** |
| `saleor/webhook/transport/asynchronous/transport.py` | 311 | 242 | **22%** |
| `saleor/webhook/transport/synchronous/transport.py` | 192 | 192 | **0%** |
| `saleor/order/calculations.py` | 297 | 215 | **28%** |
| `saleor/order/utils.py` | 569 | 434 | **24%** |
| `saleor/payment/utils.py` | 724 | 588 | **19%** |
| `saleor/warehouse/management.py` | 393 | 340 | **13%** |
| `saleor/warehouse/availability.py` | 178 | 137 | **23%** |
| `saleor/app/installation_utils.py` | 169 | 116 | **31%** |
| `saleor/app/tasks.py` | 75 | 53 | **29%** |
| `saleor/account/notifications.py` | 72 | 52 | **28%** |
| `saleor/account/tasks.py` | 58 | 35 | **40%** |
| `saleor/account/utils.py` | 119 | 65 | **45%** |

---

## Test Files Analysis

### ✅ Test Files Created (37 files in `tests/whitebox/`)

1. **Checkout Module Tests:**
   - `test_checkout_actions_extensive.py` - Tests `saleor/checkout/actions.py`
   - `test_checkout_calculations_extensive.py` - Tests `saleor/checkout/calculations.py`
   - `test_checkout_base_calculations_comprehensive.py` - Tests `saleor/checkout/base_calculations.py`
   - `test_checkout_utils_comprehensive.py` - Tests `saleor/checkout/utils.py`

2. **Order Module Tests:**
   - `test_order_actions_comprehensive.py` - Tests `saleor/order/actions.py`
   - `test_order_calculations_comprehensive.py` - Tests `saleor/order/calculations.py`
   - `test_order_base_calculations_comprehensive.py` - Tests `saleor/order/base_calculations.py`
   - `test_order_utils_comprehensive.py` - Tests `saleor/order/utils.py`

3. **Webhook Module Tests:**
   - `test_webhook_utils_extensive.py` - Tests `saleor/webhook/utils.py`
   - `test_webhook_utils_comprehensive.py` - Additional webhook tests

4. **Warehouse Module Tests:**
   - `test_warehouse_management_comprehensive.py` - Tests `saleor/warehouse/management.py`
   - `test_warehouse_availability_comprehensive.py` - Tests `saleor/warehouse/availability.py`

5. **Other Module Tests:**
   - `test_asgi_handlers.py` - Tests `saleor/asgi/`
   - `test_app_installation_utils.py` - Tests `saleor/app/installation_utils.py`
   - `test_account_notifications.py` - Tests `saleor/account/notifications.py`
   - And many more...

---

## Test Coverage Mapping

### ✅ Correctly Mapped Tests

| Test File | Target Module | Status |
|-----------|---------------|--------|
| `test_checkout_actions_extensive.py` | `saleor/checkout/actions.py` | ✅ Correct |
| `test_checkout_calculations_extensive.py` | `saleor/checkout/calculations.py` | ✅ Correct |
| `test_checkout_base_calculations_comprehensive.py` | `saleor/checkout/base_calculations.py` | ✅ Correct |
| `test_order_actions_comprehensive.py` | `saleor/order/actions.py` | ✅ Correct |
| `test_order_calculations_comprehensive.py` | `saleor/order/calculations.py` | ✅ Correct |
| `test_webhook_utils_extensive.py` | `saleor/webhook/utils.py` | ✅ Correct |
| `test_warehouse_management_comprehensive.py` | `saleor/warehouse/management.py` | ✅ Correct |
| `test_asgi_handlers.py` | `saleor/asgi/` | ✅ Correct |

---

## Issues Found

### ⚠️ Test Failures

**334 tests failed, 253 passed** (57% failure rate)

**Common Failure Categories:**

1. **Database/Model Issues:**
   - Warehouse management tests failing due to model setup
   - Stock allocation tests need proper fixtures

2. **Mock/Setup Issues:**
   - Webhook utils tests need proper app/permission setup
   - ASGI handler tests need proper async mocking

3. **Import/Dependency Issues:**
   - Some tests have incorrect imports
   - Missing fixtures or test data

### 🔧 Recommendations

1. **Fix Test Fixtures:**
   - Ensure all required models are properly created
   - Add proper database transactions
   - Fix mock setups for async code

2. **Improve Test Data:**
   - Create comprehensive fixtures
   - Add proper test factories
   - Ensure all required relationships are set up

3. **Fix Import Issues:**
   - Verify all imports are correct
   - Ensure test dependencies are installed
   - Check for circular import issues

---

## Coverage Improvement Plan

### Phase 1: Fix Failing Tests (Target: +5% coverage)
- Fix 334 failing tests
- Expected impact: +5% overall coverage

### Phase 2: Add Missing Tests (Target: +15% coverage)
- `saleor/checkout/complete_checkout.py` - 531 statements (15% → 80%)
- `saleor/checkout/tasks.py` - 102 statements (0% → 80%)
- `saleor/webhook/transport/` - Both sync and async (0% → 80%)
- `saleor/asgi/` - All handlers (8-22% → 80%)

### Phase 3: Enhance Existing Tests (Target: +10% coverage)
- Improve existing test coverage
- Add edge case tests
- Add error handling tests

**Total Expected: 48% + 30% = 78%** (close to 80% target)

---

## Next Steps

1. ✅ **Fix failing tests** - Address the 334 test failures
2. ✅ **Add complete_checkout tests** - Biggest gap (531 statements)
3. ✅ **Add webhook transport tests** - Critical for production
4. ✅ **Add ASGI handler tests** - Required for deployment
5. ✅ **Improve test fixtures** - Better test data setup

---

*For the complete file-by-file coverage report, see the HTML report at: `htmlcov/combined/index.html`*

