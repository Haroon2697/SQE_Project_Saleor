# 🧪 White-Box Testing Guide

**Project:** Saleor SQE - White-Box Testing  
**Date:** 2025-12-04  
**Focus:** Backend Python Code (`saleor` directory)

---

## 📋 Overview

**White-box testing** focuses on testing the **internal structure, logic, and code paths** of the application.

### ✅ What We're Testing:
- **Backend Code:** `saleor/` directory (Python/Django)
- **Main Logic Files:** Core models, calculations, business logic

### ❌ What We're NOT Testing (White-box):
- **Frontend Code:** `saleor-dashboard/` (React/TypeScript)
  - This is tested with **Black-box testing** (Cypress) ✅

---

## 🎯 Coverage Types

### 1. **Statement Coverage**
- **Goal:** Execute every statement at least once
- **Requirement:** 100% statement coverage
- **Tests:** All code paths executed

### 2. **Decision Coverage (Branch Coverage)**
- **Goal:** Test all decision outcomes (True/False)
- **Requirement:** All branches tested
- **Tests:** Both True and False branches for each condition

### 3. **MC/DC Coverage (Modified Condition/Decision Coverage)**
- **Goal:** Test independent effect of each condition on decision outcome
- **Requirement:** Each condition independently affects the decision
- **Tests:** All combinations where each condition independently changes the outcome

---

## 📁 Test Structure

```
tests/whitebox/
├── __init__.py
├── test_core_models.py          # Core models (SortableModel, PublishableModel)
├── test_product_models.py       # Product models (ProductVariant methods)
└── test_order_calculations.py   # Order calculations (fetch_order_prices_if_expired)
```

---

## 🧪 Test Files

### **1. test_core_models.py**
**Target:** `saleor/core/models.py`

**Classes Tested:**
- `SortableModel` - save(), delete(), get_max_sort_order()
- `PublishableModel` - published() queryset

**Coverage:**
- ✅ Statement Coverage
- ✅ Decision Coverage
- ✅ MC/DC Coverage

**Test Cases:**
- `TestSortableModelStatementCoverage` - 5 tests
- `TestSortableModelDecisionCoverage` - 4 tests
- `TestSortableModelMCDC` - 2 tests
- `TestPublishableModelStatementCoverage` - 4 tests
- `TestPublishableModelDecisionCoverage` - 5 tests
- `TestPublishableModelMCDC` - 4 tests

**Total:** 24 test cases

---

### **2. test_product_models.py**
**Target:** `saleor/product/models.py`

**Methods Tested:**
- `ProductVariant.get_base_price()` - Price calculation logic
- `ProductVariant.get_price()` - Discounted price with promotions
- `ProductVariant.get_prior_price_amount()` - Prior price retrieval
- `ProductVariant.get_weight()` - Weight calculation (fallback chain)
- `ProductVariant.is_digital()` - Digital product detection

**Coverage:**
- ✅ Statement Coverage
- ✅ Decision Coverage
- ✅ MC/DC Coverage

**Test Cases:**
- `TestProductVariantGetBasePrice` - 2 tests
- `TestProductVariantGetBasePriceDecision` - 2 tests
- `TestProductVariantGetPrice` - 3 tests
- `TestProductVariantGetPriceDecision` - 4 tests
- `TestProductVariantGetPriorPriceAmount` - 3 tests
- `TestProductVariantGetWeight` - 3 tests
- `TestProductVariantIsDigital` - 3 tests
- `TestProductVariantIsDigitalMCDC` - 3 tests

**Total:** 23 test cases

---

### **3. test_order_calculations.py**
**Target:** `saleor/order/calculations.py`

**Functions Tested:**
- `fetch_order_prices_if_expired()` - Complex order price calculation logic

**Coverage:**
- ✅ Statement Coverage
- ✅ Decision Coverage
- ✅ MC/DC Coverage

**Test Cases:**
- `TestFetchOrderPricesIfExpiredStatementCoverage` - 5 tests
- `TestFetchOrderPricesIfExpiredDecisionCoverage` - 6 tests
- `TestFetchOrderPricesIfExpiredMCDC` - 4 tests

**Total:** 15 test cases

---

## 🚀 Running Tests

### **Option 1: Using the Script (Recommended)**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
./run_whitebox_tests.sh
```

### **Option 2: Manual Command**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
source venv/bin/activate  # If using venv

pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=html:htmlcov/whitebox \
    --cov-report=term \
    --cov-report=xml:coverage-whitebox.xml \
    -v
```

### **Option 3: Run Specific Test File**
```bash
pytest tests/whitebox/test_core_models.py -v --cov=saleor.core.models
pytest tests/whitebox/test_product_models.py -v --cov=saleor.product.models
pytest tests/whitebox/test_order_calculations.py -v --cov=saleor.order.calculations
```

---

## 📊 Coverage Reports

### **HTML Coverage Report**
**Location:** `htmlcov/whitebox/index.html`

**To View:**
```bash
# Open in browser
xdg-open htmlcov/whitebox/index.html  # Linux
open htmlcov/whitebox/index.html      # macOS
start htmlcov/whitebox/index.html     # Windows
```

**Features:**
- ✅ Line-by-line coverage
- ✅ Branch coverage
- ✅ Missing coverage highlighted
- ✅ Interactive navigation

### **Terminal Report**
Shows coverage summary in terminal:
- Total coverage percentage
- Coverage by module
- Missing lines

### **XML Report**
**Location:** `coverage-whitebox.xml`

**Use Cases:**
- CI/CD integration
- Coverage tracking tools
- Automated reporting

---

## 📈 Coverage Metrics

### **Target Coverage:**
- **Statement Coverage:** 80%+ (aiming for 100%)
- **Decision Coverage:** 80%+ (all branches tested)
- **MC/DC Coverage:** Where applicable (complex conditions)

### **Current Coverage:**
Run tests to see current metrics:
```bash
pytest tests/whitebox/ --cov=saleor --cov-report=term-missing
```

---

## 🎯 Test Coverage Examples

### **Example 1: Statement Coverage**
```python
def test_save_new_object_no_existing_max(self):
    """Execute: if self.pk is None -> set sort_order = 0"""
    category = Category.objects.create(name="Test", slug="test")
    assert category.sort_order == 0  # Statement executed
```

### **Example 2: Decision Coverage**
```python
def test_decision_price_override_none_true(self):
    """Decision: price_override is None -> TRUE branch"""
    price = variant.get_base_price(listing, price_override=None)
    assert price == listing.price  # TRUE branch tested

def test_decision_price_override_none_false(self):
    """Decision: price_override is None -> FALSE branch"""
    price = variant.get_base_price(listing, price_override=Decimal("100"))
    assert price.amount == Decimal("100")  # FALSE branch tested
```

### **Example 3: MC/DC Coverage**
```python
def test_mcdc_condition_a_true_b_false(self):
    """MC/DC: (published_at <= today) AND is_published = False"""
    product = Product.objects.create(
        is_published=False,  # Condition B = False
        published_at=timezone.now() - timedelta(days=1)  # Condition A = True
    )
    assert product not in Product.objects.published()  # Decision = False
```

---

## 📝 Adding New Tests

### **Template for Statement Coverage Test:**
```python
@pytest.mark.django_db
def test_function_statement_coverage(self):
    """Statement Coverage: Test all code paths"""
    # Setup
    obj = Model.objects.create(...)
    
    # Execute
    result = obj.method()
    
    # Verify all statements executed
    assert result is not None
```

### **Template for Decision Coverage Test:**
```python
@pytest.mark.django_db
def test_decision_condition_true(self):
    """Decision: condition = True -> TRUE branch"""
    # Setup for True condition
    result = function(condition=True)
    assert result == expected_true

@pytest.mark.django_db
def test_decision_condition_false(self):
    """Decision: condition = False -> FALSE branch"""
    # Setup for False condition
    result = function(condition=False)
    assert result == expected_false
```

### **Template for MC/DC Coverage Test:**
```python
@pytest.mark.django_db
def test_mcdc_condition_a_true_b_false(self):
    """MC/DC: Condition A independently affects decision"""
    # Setup: A=True, B=False
    result = function(condition_a=True, condition_b=False)
    # Verify A independently affects outcome
    assert result == expected_when_a_true
```

---

## 🔍 Finding Main Logic Files

### **Key Files to Test:**
1. **Core Models:** `saleor/core/models.py`
2. **Product Models:** `saleor/product/models.py`
3. **Order Calculations:** `saleor/order/calculations.py`
4. **Checkout Calculations:** `saleor/checkout/calculations.py`
5. **Base Calculations:** `saleor/order/base_calculations.py`
6. **Utils:** `saleor/*/utils.py` files

### **How to Identify:**
- Look for functions with:
  - Multiple if/else statements
  - Complex conditions (AND/OR)
  - Business logic
  - Calculations
  - Decision points

---

## ✅ Verification Checklist

- [ ] All test files created
- [ ] Tests run successfully
- [ ] HTML coverage report generated
- [ ] Statement coverage > 80%
- [ ] Decision coverage > 80%
- [ ] MC/DC coverage for complex conditions
- [ ] All tests passing
- [ ] Coverage reports accessible

---

## 📚 Resources

- **Pytest Documentation:** https://docs.pytest.org/
- **Coverage.py Documentation:** https://coverage.readthedocs.io/
- **MC/DC Coverage:** https://en.wikipedia.org/wiki/Modified_condition/decision_coverage

---

**Status:** ✅ White-box testing framework ready  
**Next Steps:** Run tests and review coverage reports

