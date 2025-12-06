# 🎨 Cypress UI Testing Setup

**Date:** 2025-12-04  
**Project:** SQE Project - Saleor UI Testing  
**Status:** ✅ **COMPLETE**

---

## ✅ What's Been Set Up

### **1. Cypress Installation** ✅
- ✅ Cypress installed as dev dependency
- ✅ Project ID: `rpaahx`
- ✅ Record key configured

### **2. Test Files Created** ✅
- ✅ `cypress/e2e/login.cy.js` - Login page tests
- ✅ `cypress/e2e/navigation.cy.js` - Navigation tests
- ✅ `cypress/e2e/graphql-api.cy.js` - GraphQL API tests
- ✅ `cypress/e2e/dashboard.cy.js` - Dashboard tests

### **3. Configuration Files** ✅
- ✅ `cypress.config.js` - Main Cypress configuration
- ✅ `cypress/support/e2e.js` - Support file
- ✅ `cypress/support/commands.js` - Custom commands
- ✅ `cypress/fixtures/example.json` - Test fixtures

### **4. CI/CD Integration** ✅
- ✅ Updated `.github/workflows/cicd-pipeline.yml` to run Cypress tests
- ✅ Configured to run in GitHub Actions

---

## 📁 Project Structure

```
SQE_Project_Saleor/
├── cypress/
│   ├── e2e/                    # Test files
│   │   ├── login.cy.js
│   │   ├── navigation.cy.js
│   │   ├── graphql-api.cy.js
│   │   └── dashboard.cy.js
│   ├── fixtures/               # Test data
│   │   └── example.json
│   ├── support/                # Support files
│   │   ├── e2e.js
│   │   └── commands.js
│   ├── videos/                 # Test videos (gitignored)
│   └── screenshots/            # Test screenshots (gitignored)
├── cypress.config.js          # Cypress configuration
└── .cypress.env.json.example  # Environment variables template
```

---

## 🚀 How to Use

### **1. Set Up Environment Variables**

Create `.cypress.env.json` file (not committed to git):

```json
{
  "CYPRESS_RECORD_KEY": "8d5f0fe8-0c32-4259-8073-86ef9b7ac337"
}
```

**OR** set environment variable:
```bash
export CYPRESS_RECORD_KEY="8d5f0fe8-0c32-4259-8073-86ef9b7ac337"
```

### **2. Start Saleor Backend**

Before running Cypress tests, start the Saleor server:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

Keep this running in one terminal.

### **3. Run Cypress Tests**

#### **Option A: Open Cypress UI (Interactive)**
```bash
npm run cypress:open
```

This opens the Cypress Test Runner where you can:
- See all test files
- Run tests interactively
- Watch tests run in real-time
- Debug tests

#### **Option B: Run Tests Headless (Command Line)**
```bash
npm run cypress:run
```

This runs all tests in headless mode (no browser window).

#### **Option C: Run Tests with Recording**
```bash
npm run cypress:run:record
```

This runs tests and records them to Cypress Dashboard (requires record key).

---

## 🧪 Test Files Overview

### **1. Login Tests** (`login.cy.js`)
Tests the login functionality:
- ✅ Login form display
- ✅ Invalid credentials error
- ✅ Successful login
- ✅ Required field validation

### **2. Navigation Tests** (`navigation.cy.js`)
Tests navigation functionality:
- ✅ Dashboard navigation after login
- ✅ Navigation menu visibility
- ✅ Products page navigation
- ✅ Orders page navigation
- ✅ Customers page navigation

### **3. GraphQL API Tests** (`graphql-api.cy.js`)
Tests GraphQL API endpoints:
- ✅ GraphQL playground access
- ✅ Shop query execution
- ✅ Products query execution
- ✅ Error handling for invalid queries

### **4. Dashboard Tests** (`dashboard.cy.js`)
Tests dashboard functionality:
- ✅ Dashboard display after login
- ✅ Dashboard content visibility
- ✅ User menu accessibility

---

## 🔧 Custom Commands

Cypress custom commands are defined in `cypress/support/commands.js`:

### **`cy.login(email, password)`**
Logs into the Saleor Dashboard.

**Usage:**
```javascript
cy.login('admin@example.com', 'admin123');
cy.login(); // Uses default credentials
```

### **`cy.logout()`**
Logs out from the Saleor Dashboard.

**Usage:**
```javascript
cy.logout();
```

### **`cy.waitForAPI()`**
Waits for the GraphQL API to be ready.

**Usage:**
```javascript
cy.waitForAPI();
```

---

## 📊 Running Tests in CI/CD

### **GitHub Actions**

The CI/CD pipeline automatically runs Cypress tests:

1. **Backend tests** run first (Pytest)
2. **UI tests** run second (Cypress)
3. Tests run in parallel using matrix strategy

### **Environment Variables in CI/CD**

Add to GitHub Secrets:
- `CYPRESS_RECORD_KEY`: `8d5f0fe8-0c32-4259-8073-86ef9b7ac337`

**How to add:**
1. Go to: `Settings → Secrets and variables → Actions`
2. Click: "New repository secret"
3. Name: `CYPRESS_RECORD_KEY`
4. Value: `8d5f0fe8-0c32-4259-8073-86ef9b7ac337`
5. Click: "Add secret"

---

## 🎯 Test Coverage

### **Black-Box UI Testing:**

| Test Area | Test File | Tests |
|-----------|-----------|-------|
| **Login** | `login.cy.js` | 5 tests |
| **Navigation** | `navigation.cy.js` | 5 tests |
| **GraphQL API** | `graphql-api.cy.js` | 4 tests |
| **Dashboard** | `dashboard.cy.js` | 3 tests |
| **Total** | **4 files** | **17 tests** |

---

## 🔍 Debugging Tests

### **Run Specific Test File:**
```bash
npx cypress run --spec "cypress/e2e/login.cy.js"
```

### **Run Tests in Browser:**
```bash
npm run cypress:open
```

### **View Test Videos:**
After running tests, videos are saved in `cypress/videos/`

### **View Screenshots:**
Screenshots on failure are saved in `cypress/screenshots/`

---

## 📝 Writing New Tests

### **Template for New Test File:**

```javascript
/**
 * [Test Description] (Black-box UI Testing)
 * 
 * Tests [what this test file covers]
 */

describe('[Test Suite Name]', () => {
  beforeEach(() => {
    // Setup before each test
    cy.login(); // If login is needed
  });

  it('should [test description]', () => {
    // Test steps
    cy.visit('/dashboard/');
    cy.get('[selector]').should('be.visible');
  });
});
```

### **Best Practices:**

1. **Use custom commands** for common actions (login, logout)
2. **Use fixtures** for test data
3. **Add timeouts** for slow operations
4. **Use descriptive test names**
5. **Group related tests** in describe blocks

---

## ⚠️ Troubleshooting

### **Problem: Tests fail with "Connection refused"**

**Solution:**
- Make sure Saleor backend is running on `http://localhost:8000`
- Check if server started successfully
- Verify `baseUrl` in `cypress.config.js`

### **Problem: Login tests fail**

**Solution:**
- Verify credentials: `admin@example.com` / `admin123`
- Check if superuser exists: `python manage.py shell` → `User.objects.filter(is_superuser=True)`
- Adjust selectors in `cypress/support/commands.js` if login form structure is different

### **Problem: Navigation tests fail**

**Solution:**
- Adjust selectors based on actual Saleor dashboard structure
- Check if navigation menu structure matches selectors
- Use Cypress UI to inspect elements: `npm run cypress:open`

### **Problem: Cypress can't find elements**

**Solution:**
- Use Cypress UI to find correct selectors
- Add longer timeouts: `{ timeout: 10000 }`
- Check if page is fully loaded before interacting

---

## 📚 Resources

- **Cypress Documentation:** https://docs.cypress.io/
- **Cypress Best Practices:** https://docs.cypress.io/guides/references/best-practices
- **Cypress Dashboard:** https://dashboard.cypress.io/
- **Project ID:** `rpaahx`

---

## ✅ Next Steps

1. ✅ Cypress installed and configured
2. ✅ Test files created
3. ✅ CI/CD pipeline updated
4. ⏳ Run tests locally to verify
5. ⏳ Add more test cases as needed
6. ⏳ Configure Cypress Dashboard (optional)

---

## 🎉 Summary

**Cypress UI Testing is now set up!**

- ✅ 4 test files with 17 tests
- ✅ Custom commands for login/logout
- ✅ CI/CD integration
- ✅ Ready to run locally and in CI

**To get started:**
1. Start Saleor backend: `python manage.py runserver 0.0.0.0:8000`
2. Run tests: `npm run cypress:open` or `npm run cypress:run`

---

**Last Updated:** 2025-12-04  
**Status:** ✅ **READY TO USE**

