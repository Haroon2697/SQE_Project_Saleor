# Deliverable 8: Unit Test Suite

## 📋 Overview

**Location:** `tests/unit/`  
**Type:** Unit Tests  
**Framework:** Pytest with Django  
**Purpose:** Test individual units of code in isolation  
**Status:** ✅ 1 Test File, 6 Test Cases

---

## 🎯 Purpose

Unit tests verify individual components of the Saleor application by:
- Testing models in isolation
- Verifying model methods
- Testing utility functions
- Ensuring individual units work correctly

---

## 📊 Test Files

### **test_models.py**

#### **Test Cases:**

1. **`test_create_user`**
   - **Purpose:** Test user creation
   - **Model:** `User`
   - **Verification:**
     - User can be created
     - User fields are set correctly
     - User is saved to database

2. **`test_create_superuser`**
   - **Purpose:** Test superuser creation
   - **Model:** `User`
   - **Verification:**
     - Superuser can be created
     - Superuser has admin privileges
     - Superuser is active

3. **`test_create_category`**
   - **Purpose:** Test category creation
   - **Model:** `Category`
   - **Verification:**
     - Category can be created
     - Category fields are set correctly
     - Category hierarchy works

4. **`test_create_product_type`**
   - **Purpose:** Test product type creation
   - **Model:** `ProductType`
   - **Verification:**
     - Product type can be created
     - Product type fields are set correctly

5. **`test_create_product`**
   - **Purpose:** Test product creation
   - **Model:** `Product`
   - **Verification:**
     - Product can be created
     - Product is linked to product type
     - Product fields are set correctly

6. **`test_site_settings`**
   - **Purpose:** Test site settings
   - **Model:** `SiteSettings`
   - **Verification:**
     - Site settings can be created
     - Settings are accessible

---

## 🧪 Test Execution

### **Run Unit Tests**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
pytest tests/unit/ -v
```

### **Run with Coverage**
```bash
pytest tests/unit/ \
    --cov=saleor \
    --cov-report=html:htmlcov/unit \
    --cov-report=term \
    -v
```

---

## 📊 Coverage

### **Models Tested**
- ✅ User model
- ✅ Category model
- ✅ ProductType model
- ✅ Product model
- ✅ SiteSettings model

### **Coverage Areas**
- Model creation
- Model field validation
- Model relationships
- Model methods

---

## 🚀 Running in CI/CD

Unit tests run automatically in the CI/CD pipeline:
- **Stage:** Test (Stage 3)
- **Job:** Backend Tests
- **Reports:** Included in combined coverage

---

## 📈 Statistics

- **Total Test Files:** 1
- **Total Test Cases:** 6
- **Models Tested:** 5
- **Coverage:** Model creation and validation

---

## 🔗 Related Documentation

- `doc/DELIVERABLES/02_WHITEBOX_TESTS.md` - White-box tests
- `doc/COVERAGE_AND_TESTING_SETUP.md` - Test setup guide

