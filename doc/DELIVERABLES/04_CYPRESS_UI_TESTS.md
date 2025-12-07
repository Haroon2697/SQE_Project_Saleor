# Deliverable 4: Cypress UI Test Suite

## 📋 Overview

**Location:** `cypress/e2e/`  
**Type:** End-to-End UI Tests (Black-box Testing)  
**Framework:** Cypress  
**Purpose:** Test user interface and user workflows  
**Status:** ✅ 7 Test Files, 20+ Test Cases

---

## 🎯 Purpose

Cypress UI tests verify the Saleor Dashboard user interface by:
- Testing user interactions (clicks, form submissions)
- Verifying page navigation
- Testing form validation
- Ensuring UI elements work correctly
- Testing complete user workflows

---

## 📊 Test Files Breakdown

### **1. login.cy.js**
- **Purpose:** Test login functionality
- **Test Cases:** 5 tests
- **Coverage:**
  - Login form display
  - Invalid credentials handling
  - Successful login
  - Required field validation
  - Password field validation

**Key Tests:**
- `should display login form` - Verifies login form elements
- `should show error for invalid credentials` - Tests error handling
- `should successfully login with valid credentials` - Tests successful login
- `should require email field` - Tests email validation
- `should require password field` - Tests password validation

---

### **2. dashboard.cy.js**
- **Purpose:** Test dashboard functionality
- **Test Cases:** 3 tests
- **Coverage:**
  - Dashboard display after login
  - Dashboard content visibility
  - User menu accessibility

**Key Tests:**
- `should display dashboard after login` - Verifies dashboard loads
- `should display dashboard content` - Tests content visibility
- `should have user menu accessible` - Tests user menu

---

### **3. navigation.cy.js**
- **Purpose:** Test navigation functionality
- **Test Cases:** 5 tests
- **Coverage:**
  - Navigation to dashboard
  - Navigation menu visibility
  - Navigation to products page
  - Navigation to orders page
  - Navigation to customers page

**Key Tests:**
- `should navigate to dashboard home after login` - Tests dashboard navigation
- `should have navigation menu visible` - Tests menu visibility
- `should be able to navigate to products page` - Tests products navigation
- `should be able to navigate to orders page` - Tests orders navigation
- `should be able to navigate to customers page` - Tests customers navigation

---

### **4. products.cy.js**
- **Purpose:** Test products page functionality
- **Test Cases:** 4 tests
- **Coverage:**
  - Products page navigation
  - Products list display
  - Product search functionality
  - Product creation button

**Key Tests:**
- `should navigate to products page` - Tests products page access
- `should display products list` - Tests products list display
- `should allow searching for products` - Tests search functionality
- `should display product creation button` - Tests create button

---

### **5. forms.cy.js**
- **Purpose:** Test form validation and submission
- **Test Cases:** 3 tests
- **Coverage:**
  - Required field validation
  - Invalid input error messages
  - Successful form submission

**Key Tests:**
- `should validate required fields` - Tests form validation
- `should show error messages for invalid input` - Tests error handling
- `should successfully submit valid form` - Tests form submission

---

### **6. orders.cy.js**
- **Purpose:** Test orders page functionality
- **Test Cases:** Multiple tests
- **Coverage:**
  - Orders page navigation
  - Orders list display
  - Order details

---

### **7. graphql-api.cy.js**
- **Purpose:** Test GraphQL API via UI
- **Test Cases:** Multiple tests
- **Coverage:**
  - GraphQL query execution
  - API response handling
  - Error handling

---

## 🔧 Configuration

### **cypress.config.js**
```javascript
{
  e2e: {
    baseUrl: 'http://localhost:9000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000
  },
  projectId: 'rpaahx'
}
```

### **Custom Commands** (`cypress/support/commands.js`)
- `cy.login(email, password)` - Login helper
- `cy.logout()` - Logout helper
- `cy.waitForAPI()` - Wait for backend API

---

## 🧪 Test Execution

### **Run Cypress in Interactive Mode**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
npm run cypress:open
```

### **Run Cypress in Headless Mode**
```bash
npm run cypress:run
```

### **Run with Recording**
```bash
CYPRESS_RECORD_KEY=your-key npm run cypress:run:record
```

### **Start Servers First**
```bash
# Terminal 1: Start servers
./start_servers_for_cypress.sh

# Terminal 2: Run Cypress
npm run cypress:open
```

---

## 📊 Test Coverage

### **UI Elements Tested**
- ✅ Login form
- ✅ Dashboard
- ✅ Navigation menu
- ✅ Products page
- ✅ Orders page
- ✅ Forms and validation
- ✅ Error messages

### **User Workflows Tested**
- ✅ Login → Dashboard
- ✅ Navigation between pages
- ✅ Form submission
- ✅ Search functionality
- ✅ Error handling

---

## 🚀 Running in CI/CD

Cypress tests run automatically in the CI/CD pipeline:
- **Stage:** Test (Stage 3)
- **Job:** UI Tests
- **Requirements:**
  - Backend server running (port 8000)
  - Dashboard running (port 9000)
- **Reports:** Videos and screenshots uploaded as artifacts

---

## 📈 Statistics

- **Total Test Files:** 7
- **Total Test Cases:** 20+
- **Pages Tested:** 5+
- **User Workflows:** 10+

---

## 🔍 Test Structure

### **Example Test Case**
```javascript
describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should display login form', () => {
    cy.get('input[name="email"]').should('be.visible');
    cy.get('input[name="password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible');
  });
});
```

---

## 🔗 Related Documentation

- `CYPRESS_SETUP_GUIDE.md` - Cypress setup instructions
- `start_servers_for_cypress.sh` - Server startup script
- `cypress.config.js` - Cypress configuration
- `cypress/support/commands.js` - Custom commands

