# Cypress Test Suite

## Overview

This directory contains the Cypress end-to-end (E2E) test suite for the Saleor Dashboard. The tests cover black-box testing scenarios including authentication, navigation, product management, orders, and more.

## Prerequisites

1. **Saleor Dashboard** must be running on `http://localhost:9000`
2. **Saleor Backend** must be running on `http://localhost:8000`
3. **Node.js** 20+ installed
4. **Cypress** installed (via npm)

## Installation

```bash
npm install
```

## Running Tests

### Interactive Mode (Recommended for Development)

```bash
npm run cypress:open
```

This opens the Cypress Test Runner GUI where you can:
- Select which tests to run
- Watch tests execute in real-time
- Debug test failures
- See screenshots and videos

### Headless Mode (For CI/CD)

```bash
npm run cypress:run
```

### Run Specific Test

```bash
npx cypress run --spec "cypress/e2e/login.cy.js"
```

### Run with Firefox (Recommended if Electron Crashes)

```bash
npx cypress run --browser firefox
```

## Test Files

1. **login.cy.js** - Login functionality tests
2. **auth_navigation.cy.js** - Authentication and navigation
3. **dashboard.cy.js** - Dashboard functionality
4. **products.cy.js** - Product management
5. **orders.cy.js** - Order management
6. **customer.cy.js** - Customer management
7. **catalog.cy.js** - Catalog browsing
8. **discounts.cy.js** - Discount management
9. **fullfillment.cy.js** - Order fulfillment
10. **forms.cy.js** - Form validation
11. **graphql-api.cy.js** - GraphQL API tests
12. **modeling.cy.js** - Data modeling tests
13. **navigation.cy.js** - Navigation tests

## Custom Commands

### `cy.login(email, password)`
Login to the dashboard with custom credentials.

```javascript
cy.login('admin@example.com', 'admin123');
```

### `cy.loginAsAdmin(email, password)`
Login as admin (alternative method).

```javascript
cy.loginAsAdmin(); // Uses defaults: admin@example.com / admin
```

### `cy.logout()`
Logout from the dashboard.

```javascript
cy.logout();
```

### `cy.waitForAPI()`
Wait for the GraphQL API to be ready.

```javascript
cy.waitForAPI();
```

### `cy.waitForDashboard()`
Wait for the dashboard to be ready.

```javascript
cy.waitForDashboard();
```

### `cy.checkDashboardRunning()`
Check if the dashboard is accessible.

```javascript
cy.checkDashboardRunning();
```

## Default Credentials

- **Email:** `admin@example.com`
- **Password:** `admin` (for `loginAsAdmin`) or `admin123` (for `login`)

## Configuration

The Cypress configuration is in `cypress.config.js`:

- **Base URL:** `http://localhost:9000`
- **Viewport:** 1280x720
- **Timeouts:** 15 seconds (commands), 30 seconds (page load)
- **Retries:** 2 retries for failed tests in run mode
- **Memory Management:** Enabled to prevent Electron crashes

## Troubleshooting

### Electron Renderer Crashes

If you encounter Electron renderer crashes:

1. **Use Firefox instead:**
   ```bash
   npx cypress run --browser firefox
   ```

2. **Reduce memory usage:**
   - The config already has `numTestsKeptInMemory: 0`
   - Try running fewer tests at once

3. **Increase system resources:**
   - Close other applications
   - Increase available RAM if possible

### Tests Timing Out

If tests are timing out:

1. **Check if dashboard is running:**
   ```bash
   curl http://localhost:9000
   ```

2. **Increase timeouts** in `cypress.config.js` if needed

3. **Add explicit waits** in test files

### Dashboard Not Accessible

If the dashboard is not accessible:

1. **Start the dashboard:**
   ```bash
   cd saleor-dashboard
   npm run dev
   ```

2. **Check the port:**
   - Default is port 9000
   - Update `baseUrl` in `cypress.config.js` if different

### Login Failures

If login tests are failing:

1. **Verify credentials:**
   - Default: `admin@example.com` / `admin` or `admin123`
   - Create a superuser if needed: `python manage.py createsuperuser`

2. **Check dashboard URL:**
   - Should be `http://localhost:9000`
   - Update if different

## Best Practices

1. **Use custom commands** for common operations (login, logout, etc.)
2. **Add explicit waits** for async operations
3. **Use data-test-id attributes** when possible for more stable selectors
4. **Keep tests independent** - each test should be able to run alone
5. **Clean up after tests** - logout, clear data, etc.

## CI/CD Integration

The tests are configured to run in CI/CD pipelines:

```yaml
- name: Run Cypress Tests
  run: |
    npm run cypress:run
```

For CI/CD, consider:
- Using headless mode
- Storing videos and screenshots as artifacts
- Setting up proper environment variables
- Using Firefox for more stable runs

## Support

For issues or questions:
1. Check the Cypress documentation: https://docs.cypress.io
2. Review test screenshots in `cypress/screenshots/`
3. Review test videos in `cypress/videos/`
4. Check the console output for detailed error messages

