# Deliverable 2: White-Box Test Suite

## 📋 Overview

**Location:** `tests/whitebox/`  
**Type:** Unit Tests (White-box Testing)  
**Framework:** Pytest with Django  
**Coverage Target:** 80%+ with Statement, Decision, and MC/DC coverage  
**Status:** ✅ 26 Test Files, 400+ Test Cases

---

## 🎯 Purpose

White-box tests verify the internal logic and implementation of the Saleor application by:
- Testing individual functions and methods
- Verifying business logic correctness
- Ensuring edge cases are handled
- Achieving high code coverage (Statement, Decision, MC/DC)

---

## 📊 Test Files Breakdown

### **Core Module Tests** (3 files)

#### `test_core_models.py`
- **Purpose:** Test core Django models
- **Test Cases:** 6 tests
- **Coverage:** SortableModel, PublishableModel
- **Key Functions Tested:**
  - Model creation and validation
  - Sorting functionality
  - Publishing state management

#### `test_core_metadata.py`
- **Purpose:** Test metadata functionality
- **Test Cases:** 3 tests
- **Coverage:** ModelWithMetadata
- **Key Functions Tested:**
  - Metadata storage and retrieval
  - Metadata validation

#### `test_core_utils.py`
- **Purpose:** Test core utility functions
- **Test Cases:** 4 tests
- **Coverage:** Utility functions (get_client_ip, build_absolute_uri, etc.)
- **Key Functions Tested:**
  - IP address extraction
  - URL building
  - Request processing

---

### **Product Module Tests** (4 files)

#### `test_product_models.py`
- **Purpose:** Test product model methods
- **Test Cases:** 8 tests
- **Coverage:** Product, ProductVariant models
- **Key Functions Tested:**
  - Product creation
  - Variant management
  - Price calculations

#### `test_product_utils.py`
- **Purpose:** Test product utility functions
- **Test Cases:** 2 tests
- **Coverage:** Product utility functions
- **Key Functions Tested:**
  - Product availability checks
  - Price calculations

#### `test_product_availability_comprehensive.py`
- **Purpose:** Comprehensive product availability tests
- **Test Cases:** 4 tests
- **Coverage:** Product availability logic
- **Key Functions Tested:**
  - Stock checking
  - Availability calculations
  - Edge cases

#### `test_product_availability_utils_comprehensive.py`
- **Purpose:** Comprehensive product availability utility tests
- **Test Cases:** Multiple test classes
- **Coverage:** `saleor/product/utils/availability.py`
- **Key Functions Tested:**
  - `get_product_availability`
  - `get_variant_availability`
  - Stock management

---

### **Order Module Tests** (3 files)

#### `test_order_base_calculations.py`
- **Purpose:** Test base order calculations
- **Test Cases:** 5 tests
- **Coverage:** `saleor/order/base_calculations.py`
- **Key Functions Tested:**
  - `base_order_subtotal`
  - `base_order_total`
  - `base_order_shipping`

#### `test_order_base_calculations_comprehensive.py`
- **Purpose:** Comprehensive order calculation tests
- **Test Cases:** 50+ tests
- **Coverage:** All functions in `base_calculations.py`
- **Key Functions Tested:**
  - `base_order_shipping`
  - `base_order_subtotal`
  - `base_order_total`
  - `base_order_line_total`
  - `propagate_order_discount_on_order_prices`
  - `calculate_prices`
  - `assign_order_prices`
  - And 8 more functions

#### `test_order_calculations.py`
- **Purpose:** Test order calculation logic
- **Test Cases:** 3 tests
- **Coverage:** Order price calculations
- **Key Functions Tested:**
  - Order total calculations
  - Discount applications

#### `test_order_utils_comprehensive.py`
- **Purpose:** Comprehensive order utility tests
- **Test Cases:** 60+ tests
- **Coverage:** `saleor/order/utils.py` (55 functions)
- **Key Functions Tested:**
  - Order creation utilities
  - Order line management
  - Order status updates
  - Price calculations

---

### **Checkout Module Tests** (3 files)

#### `test_checkout_base_calculations.py`
- **Purpose:** Test base checkout calculations
- **Test Cases:** 2 tests
- **Coverage:** `saleor/checkout/base_calculations.py`
- **Key Functions Tested:**
  - `base_checkout_subtotal`
  - `checkout_total`

#### `test_checkout_base_calculations_comprehensive.py`
- **Purpose:** Comprehensive checkout calculation tests
- **Test Cases:** 40+ tests
- **Coverage:** All functions in `base_calculations.py`
- **Key Functions Tested:**
  - `calculate_base_line_unit_price`
  - `calculate_base_line_total_price`
  - `base_checkout_delivery_price`
  - `base_checkout_subtotal`
  - `base_checkout_total`
  - And 7 more functions

#### `test_checkout_calculations_comprehensive.py`
- **Purpose:** Additional checkout calculation tests
- **Test Cases:** Multiple test classes
- **Coverage:** Checkout calculation edge cases
- **Key Functions Tested:**
  - Discount calculations
  - Voucher applications
  - Shipping calculations

#### `test_checkout_utils_comprehensive.py`
- **Purpose:** Comprehensive checkout utility tests
- **Test Cases:** 70+ tests
- **Coverage:** `saleor/checkout/utils.py` (57 functions)
- **Key Functions Tested:**
  - `invalidate_checkout`
  - `check_variant_in_stock`
  - `add_variant_to_checkout`
  - `get_voucher_discount_for_checkout`
  - `is_shipping_required`
  - And 52 more functions

---

### **Payment Module Tests** (3 files)

#### `test_payment_utils.py`
- **Purpose:** Basic payment utility tests
- **Test Cases:** 3 tests
- **Coverage:** Payment utilities
- **Key Functions Tested:**
  - Payment creation
  - Payment validation

#### `test_payment_utils_comprehensive.py`
- **Purpose:** Comprehensive payment utility tests
- **Test Cases:** 20+ tests
- **Coverage:** Payment utility functions
- **Key Functions Tested:**
  - Payment processing
  - Transaction handling
  - Payment gateway integration

#### `test_payment_utils_additional.py`
- **Purpose:** Additional payment utility tests
- **Test Cases:** 15+ tests
- **Coverage:** `saleor/payment/utils.py`
- **Key Functions Tested:**
  - `create_payment_lines_information`
  - `create_checkout_payment_lines_information`
  - `create_order_payment_lines_information`
  - `generate_transactions_data`
  - `create_payment_information`
  - `create_payment`

---

### **Other Module Tests** (6 files)

#### `test_discount_utils.py`
- **Purpose:** Test discount utilities
- **Test Cases:** 5 tests
- **Coverage:** Discount calculations
- **Key Functions Tested:**
  - Voucher validation
  - Promotion calculations

#### `test_account_utils.py`
- **Purpose:** Test account utilities
- **Test Cases:** 4 tests
- **Coverage:** User account management
- **Key Functions Tested:**
  - Address management
  - User utilities

#### `test_shipping_utils.py`
- **Purpose:** Test shipping utilities
- **Test Cases:** 1 test
- **Coverage:** Shipping calculations
- **Key Functions Tested:**
  - Shipping method selection

#### `test_warehouse_management_comprehensive.py`
- **Purpose:** Comprehensive warehouse management tests
- **Test Cases:** 20+ tests
- **Coverage:** `saleor/warehouse/management.py`
- **Key Functions Tested:**
  - Stock management
  - Warehouse operations
  - Inventory tracking

#### `test_warehouse_availability_comprehensive.py`
- **Purpose:** Comprehensive warehouse availability tests
- **Test Cases:** 15+ tests
- **Coverage:** `saleor/warehouse/availability.py`
- **Key Functions Tested:**
  - Stock availability checks
  - Allocation management
  - Reservation handling

#### `test_webhook_utils.py`
- **Purpose:** Basic webhook utility tests
- **Test Cases:** 3 tests
- **Coverage:** Webhook utilities
- **Key Functions Tested:**
  - Webhook creation
  - Webhook validation

#### `test_webhook_utils_comprehensive.py`
- **Purpose:** Comprehensive webhook utility tests
- **Test Cases:** 10+ tests
- **Coverage:** `saleor/webhook/utils.py`
- **Key Functions Tested:**
  - `get_filter_for_single_webhook_event`
  - `get_webhooks_for_event`
  - `get_webhooks_for_multiple_events`

---

## 🧪 Test Execution

### **Run All White-Box Tests**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
pytest tests/whitebox/ -v
```

### **Run with Coverage**
```bash
pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=html:htmlcov/whitebox \
    --cov-report=term \
    -v
```

### **Run Specific Test File**
```bash
pytest tests/whitebox/test_order_base_calculations_comprehensive.py -v
```

### **Run Specific Test Class**
```bash
pytest tests/whitebox/test_order_base_calculations_comprehensive.py::TestBaseOrderShipping -v
```

---

## 📊 Coverage Metrics

### **Target Coverage**
- **Statement Coverage:** 80%+
- **Decision Coverage:** 80%+
- **MC/DC Coverage:** Where applicable

### **Current Coverage**
- **Overall:** ~49-60% (working towards 80%+)
- **Business Logic Modules:** 70-90%
- **Utility Functions:** 60-80%

### **Coverage Reports**
- **HTML Report:** `htmlcov/whitebox/index.html`
- **XML Report:** `coverage-whitebox.xml`
- **Terminal Report:** Shown during test execution

---

## 🔍 Test Structure

### **Test Class Organization**
```python
@pytest.mark.django_db
class TestFunctionName:
    """Test function_name() - Statement Coverage"""
    
    def test_function_name_basic_case(self):
        """Statement: Test basic functionality"""
        # Test implementation
    
    def test_function_name_edge_case(self):
        """Decision: Test edge case"""
        # Test implementation
```

### **Coverage Types**

#### **Statement Coverage**
- Every executable statement is tested
- All code paths are executed
- Example: `if x > 0: return True`

#### **Decision Coverage**
- All branch decisions (True/False) are tested
- Both outcomes of conditions are tested
- Example: `if x > 0 and y < 10:`

#### **MC/DC Coverage**
- Modified Condition/Decision Coverage
- Each condition independently affects the outcome
- Complex boolean expressions fully tested

---

## 📝 Test Data Management

### **Fixtures**
- Django test database (automatic)
- Model factories (where applicable)
- Mock objects for external dependencies

### **Test Isolation**
- Each test runs in isolation
- Database transactions rolled back after each test
- No side effects between tests

---

## 🚀 Running Tests in CI/CD

Tests are automatically executed in the CI/CD pipeline:
- **Stage:** Test (Stage 3)
- **Job:** Backend Tests
- **Matrix:** Multiple Python versions
- **Reports:** Uploaded as artifacts

---

## 📈 Statistics

- **Total Test Files:** 26
- **Total Test Functions:** 400+
- **Modules Tested:** 11
- **Functions Tested:** 150+
- **Average Tests per File:** 15-20

---

## 🔗 Related Documentation

- `doc/COMPREHENSIVE_WHITEBOX_TESTING.md` - Detailed testing guide
- `doc/TEST_PLAN_COVERAGE_ANALYSIS.md` - Coverage analysis
- `run_all_whitebox_tests.sh` - Test execution script
- `run_comprehensive_whitebox_tests.sh` - Comprehensive test script

