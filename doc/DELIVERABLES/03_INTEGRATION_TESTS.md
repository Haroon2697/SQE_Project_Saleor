# Deliverable 3: Integration Test Suite

## 📋 Overview

**Location:** `tests/integration/`  
**Type:** Integration Tests (Black-box API Testing)  
**Framework:** Pytest with Django Test Client  
**Purpose:** Test API endpoints and system integration  
**Status:** ✅ 1 Test File, 4 Test Cases

---

## 🎯 Purpose

Integration tests verify that different components of the Saleor application work together correctly by:
- Testing API endpoints end-to-end
- Verifying HTTP responses
- Testing GraphQL API functionality
- Ensuring system integration works as expected

---

## 📊 Test Files

### **test_api.py**

#### **Test Cases:**

1. **`test_health_endpoint`**
   - **Purpose:** Verify health check endpoint
   - **Endpoint:** `/health/`
   - **Expected:** HTTP 200 response
   - **Verification:**
     - Endpoint is accessible
     - Returns successful status
     - Response format is correct

2. **`test_graphql_endpoint_exists`**
   - **Purpose:** Verify GraphQL endpoint exists
   - **Endpoint:** `/graphql/`
   - **Expected:** HTTP 200 response
   - **Verification:**
     - GraphQL endpoint is accessible
     - Accepts POST requests
     - Returns valid response

3. **`test_graphql_shop_query`**
   - **Purpose:** Test GraphQL shop query
   - **Endpoint:** `/graphql/`
   - **Query:** `{ shop { name } }`
   - **Expected:** Valid GraphQL response with shop data
   - **Verification:**
     - Query executes successfully
     - Returns shop information
     - Response structure is correct

4. **`test_dashboard_endpoint`**
   - **Purpose:** Verify dashboard endpoint
   - **Endpoint:** `/dashboard/`
   - **Expected:** HTTP 200 response
   - **Verification:**
     - Dashboard is accessible
     - Returns HTML content
     - Page loads correctly

---

## 🧪 Test Execution

### **Run Integration Tests**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
pytest tests/integration/ -v
```

### **Run with Coverage**
```bash
pytest tests/integration/ \
    --cov=saleor \
    --cov-report=html:htmlcov/integration \
    --cov-report=term \
    -v
```

### **Run Specific Test**
```bash
pytest tests/integration/test_api.py::test_graphql_shop_query -v
```

---

## 🔍 Test Structure

### **Example Test Case**
```python
@pytest.mark.django_db
def test_graphql_shop_query(client):
    """Test GraphQL shop query endpoint"""
    query = """
    {
        shop {
            name
        }
    }
    """
    response = client.post('/graphql/', {
        'query': query
    }, content_type='application/json')
    
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    assert 'shop' in data['data']
```

---

## 📊 Coverage

### **Endpoints Tested**
- ✅ Health check endpoint
- ✅ GraphQL API endpoint
- ✅ Dashboard endpoint
- ✅ GraphQL queries

### **Coverage Areas**
- API endpoint accessibility
- HTTP response codes
- Response data structure
- GraphQL query execution

---

## 🚀 Running in CI/CD

Integration tests run automatically in the CI/CD pipeline:
- **Stage:** Test (Stage 3)
- **Job:** Backend Tests
- **Reports:** Uploaded as artifacts

---

## 📈 Statistics

- **Total Test Files:** 1
- **Total Test Cases:** 4
- **Endpoints Tested:** 4
- **Coverage:** API endpoint integration

---

## 🔗 Related Documentation

- `doc/COVERAGE_AND_TESTING_SETUP.md` - Test setup guide
- `run_tests_with_html_coverage.sh` - Test execution script

