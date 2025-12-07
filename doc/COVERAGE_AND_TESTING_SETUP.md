# Coverage and Testing Setup Guide

## ✅ Completed Setup

### 1. Docker Build Fix ✅
- **Issue:** Docker build failed because README.md was missing
- **Fix:** Created README.md in root directory (copied from doc/README.md)
- **Files Updated:**
  - `Dockerfile` - Now copies README.md properly
  - `.github/workflows/complete-cicd-pipeline.yml` - Updated auto-generated Dockerfile

### 2. Cypress Setup ✅
- **Status:** Fully configured and ready
- **Configuration Files:**
  - `cypress.config.js` - Configured with project ID and base URL
  - `package.json` - Contains Cypress scripts and dependencies
  - `cypress/support/commands.js` - Custom commands (login, logout, waitForAPI)
  - `cypress/support/e2e.js` - Support file with error handling

- **Test Files:**
  - `cypress/e2e/login.cy.js` - Login functionality tests
  - `cypress/e2e/dashboard.cy.js` - Dashboard tests
  - `cypress/e2e/navigation.cy.js` - Navigation tests
  - `cypress/e2e/products.cy.js` - Products page tests
  - `cypress/e2e/forms.cy.js` - Form validation tests

- **CI/CD Integration:**
  - Cypress runs in Stage 3 (Test) of the CI/CD pipeline
  - Configured to start backend server and dashboard
  - Tests run with or without recording (based on CYPRESS_RECORD_KEY)

### 3. HTML Coverage Reports ✅
- **Status:** Fully configured and generating reports
- **Script:** `run_tests_with_html_coverage.sh` - Runs all tests and generates HTML reports
- **Report Locations:**
  - `htmlcov/index.html` - Main combined coverage report ⭐
  - `htmlcov/combined/index.html` - All tests combined
  - `htmlcov/whitebox/index.html` - White-box tests only
  - `htmlcov/integration/index.html` - Integration tests only

- **CI/CD Integration:**
  - HTML coverage reports are uploaded as artifacts
  - Available for download from GitHub Actions
  - Retention: 30 days

### 4. Additional Test Cases ✅
- **New Test Files Created:**
  - `tests/whitebox/test_webhook_utils_comprehensive.py` - Webhook utility tests
  - `tests/whitebox/test_payment_utils_additional.py` - Additional payment utility tests

- **Coverage Target:** 80%+ (working towards this goal)

## 🚀 How to Run Tests and Generate Coverage Reports

### Option 1: Using the Script (Recommended)
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
./run_tests_with_html_coverage.sh
```

### Option 2: Manual Command
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
source .venv/bin/activate  # or venv/bin/activate

# Run all tests with HTML coverage
pytest tests/ \
    --cov=saleor \
    --cov-report=html:htmlcov/combined \
    --cov-report=term \
    --cov-report=term-missing \
    --cov-report=xml:coverage.xml \
    -v
```

### Option 3: Run Specific Test Types
```bash
# White-box tests only
pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=html:htmlcov/whitebox \
    -v

# Integration tests only
pytest tests/integration/ \
    --cov=saleor \
    --cov-report=html:htmlcov/integration \
    -v
```

## 📊 Viewing HTML Coverage Reports

### Local Viewing
1. **Open in Browser:**
   ```bash
   # Main report
   xdg-open htmlcov/index.html
   
   # Or use file:// URL
   file:///home/haroon/SQE/SQE_Project_Saleor/htmlcov/index.html
   ```

2. **Start a Simple HTTP Server:**
   ```bash
   cd htmlcov
   python -m http.server 8001
   # Then open http://localhost:8001 in your browser
   ```

### CI/CD Reports
- HTML coverage reports are uploaded as artifacts in GitHub Actions
- Download from the "Actions" tab → Select workflow run → "Artifacts"
- Reports are available for 30 days

## 🎨 Running Cypress Tests

### Local Development
```bash
# Install dependencies (if not already done)
npm install

# Run Cypress in interactive mode
npm run cypress:open

# Run Cypress in headless mode
npm run cypress:run

# Run with recording (requires CYPRESS_RECORD_KEY)
CYPRESS_RECORD_KEY=your-key npm run cypress:run:record
```

### CI/CD
- Cypress tests run automatically in the CI/CD pipeline
- Backend server starts on port 8000
- Dashboard starts on port 9000 (if available)
- Tests run in headless mode
- Videos and screenshots are saved as artifacts

## 📈 Coverage Goals

- **Current Target:** 80%+ overall coverage
- **Coverage Types:**
  - Statement Coverage ✅
  - Decision Coverage ✅
  - MC/DC Coverage ✅ (where applicable)

## 🔧 Troubleshooting

### HTML Reports Not Generated
1. Ensure `pytest-cov` is installed: `pip install pytest-cov`
2. Check that tests are running: `pytest tests/ -v`
3. Verify htmlcov directory exists: `ls -la htmlcov/`

### Cypress Tests Failing
1. Ensure backend server is running: `python manage.py runserver 0.0.0.0:8000`
2. Check dashboard is accessible: `curl http://localhost:9000`
3. Verify Cypress is installed: `npm list cypress`
4. Check Cypress configuration: `cat cypress.config.js`

### Docker Build Failing
1. Ensure README.md exists in root: `ls -la README.md`
2. Check Dockerfile syntax: `docker build --dry-run .`
3. Verify pyproject.toml exists: `ls -la pyproject.toml`

## 📝 Next Steps

1. **Increase Coverage:**
   - Continue adding tests for low-coverage modules
   - Focus on webhook, payment, and graphql modules
   - Fix failing tests to improve coverage

2. **Improve Cypress Tests:**
   - Add more E2E test scenarios
   - Test form submissions
   - Test error handling

3. **CI/CD Enhancements:**
   - Add coverage thresholds
   - Fail builds if coverage drops below 80%
   - Add coverage badges to README

## 📚 Related Documentation

- `doc/COMPREHENSIVE_WHITEBOX_TESTING.md` - White-box testing guide
- `doc/TEST_PLAN_COVERAGE_ANALYSIS.md` - Coverage analysis
- `doc/QA_TEST_REPORT.md` - Test results and coverage gaps

