# Deliverable 5: Test Execution Scripts

## 📋 Overview

**Location:** Root directory (`/home/haroon/SQE/SQE_Project_Saleor/`)  
**Type:** Bash Shell Scripts  
**Purpose:** Automate test execution and coverage report generation  
**Status:** ✅ 7 Test Scripts Created

---

## 📊 Scripts Breakdown

### **1. run_tests_with_html_coverage.sh**
- **Purpose:** Run all tests and generate HTML coverage reports
- **Location:** Root directory
- **Features:**
  - Runs all test suites (whitebox, integration, unit)
  - Generates HTML coverage reports
  - Creates separate reports for each test type
  - Generates combined coverage report
  - Shows coverage summary in terminal

**Usage:**
```bash
./run_tests_with_html_coverage.sh
```

**Output:**
- `htmlcov/combined/index.html` - Main combined report
- `htmlcov/whitebox/index.html` - White-box tests only
- `htmlcov/integration/index.html` - Integration tests only
- `coverage.xml` - XML coverage report

---

### **2. run_all_whitebox_tests.sh**
- **Purpose:** Run all white-box tests
- **Location:** Root directory
- **Features:**
  - Runs all tests in `tests/whitebox/`
  - Generates HTML coverage report
  - Shows coverage in terminal
  - Generates XML report

**Usage:**
```bash
./run_all_whitebox_tests.sh
```

**Output:**
- `htmlcov/whitebox/index.html`
- `coverage-whitebox.xml`

---

### **3. run_comprehensive_whitebox_tests.sh**
- **Purpose:** Run comprehensive white-box tests with detailed analysis
- **Location:** Root directory
- **Features:**
  - Comprehensive test execution
  - Detailed coverage analysis
  - Statement, Decision, MC/DC coverage
  - Duration reporting

**Usage:**
```bash
./run_comprehensive_whitebox_tests.sh
```

**Output:**
- Detailed coverage reports
- Test duration information
- Coverage metrics

---

### **4. run_whitebox_tests.sh**
- **Purpose:** Run white-box tests with coverage
- **Location:** Root directory
- **Features:**
  - White-box test execution
  - HTML coverage generation
  - Terminal coverage display

**Usage:**
```bash
./run_whitebox_tests.sh
```

---

### **5. run_all_tests_with_coverage.sh**
- **Purpose:** Run all tests with comprehensive coverage
- **Location:** Root directory
- **Features:**
  - Runs all test types sequentially
  - Generates separate coverage reports
  - Combines coverage at the end
  - Shows coverage summary

**Usage:**
```bash
./run_all_tests_with_coverage.sh
```

**Output:**
- Multiple coverage reports
- Combined coverage report
- Coverage summary

---

### **6. run_tests.sh**
- **Purpose:** Basic test execution script
- **Location:** Root directory
- **Features:**
  - Simple test execution
  - Basic coverage reporting

**Usage:**
```bash
./run_tests.sh
```

---

### **7. start_servers_for_cypress.sh**
- **Purpose:** Start backend and dashboard servers for Cypress testing
- **Location:** Root directory
- **Features:**
  - Starts Saleor backend (port 8000)
  - Starts Saleor dashboard (port 9000)
  - Waits for servers to be ready
  - Handles cleanup on exit

**Usage:**
```bash
./start_servers_for_cypress.sh
```

**Requirements:**
- PostgreSQL running
- Virtual environment activated
- Dashboard dependencies installed

---

## 🔧 Script Features

### **Common Features**
- ✅ Virtual environment activation
- ✅ Coverage report generation
- ✅ HTML report creation
- ✅ XML report generation
- ✅ Terminal coverage display
- ✅ Error handling

### **Coverage Report Types**
- **HTML Reports:** Interactive browser-based reports
- **XML Reports:** For CI/CD integration
- **Terminal Reports:** Inline coverage display
- **Missing Coverage:** Shows uncovered lines

---

## 📊 Coverage Report Locations

### **HTML Reports**
- `htmlcov/index.html` - Main report
- `htmlcov/combined/index.html` - All tests combined
- `htmlcov/whitebox/index.html` - White-box tests
- `htmlcov/integration/index.html` - Integration tests

### **XML Reports**
- `coverage.xml` - Combined coverage
- `coverage-whitebox.xml` - White-box coverage
- `coverage-integration.xml` - Integration coverage

---

## 🚀 Usage Examples

### **Generate All Coverage Reports**
```bash
./run_tests_with_html_coverage.sh
```

### **Run Only White-Box Tests**
```bash
./run_all_whitebox_tests.sh
```

### **Start Servers for Cypress**
```bash
# Terminal 1
./start_servers_for_cypress.sh

# Terminal 2
npm run cypress:open
```

---

## 📈 Statistics

- **Total Scripts:** 7
- **Test Execution Scripts:** 6
- **Server Management Scripts:** 1
- **Coverage Report Types:** 3 (HTML, XML, Terminal)

---

## 🔗 Related Documentation

- `doc/COVERAGE_AND_TESTING_SETUP.md` - Coverage setup guide
- `doc/COMPREHENSIVE_WHITEBOX_TESTING.md` - White-box testing guide
- `CYPRESS_SETUP_GUIDE.md` - Cypress setup guide

