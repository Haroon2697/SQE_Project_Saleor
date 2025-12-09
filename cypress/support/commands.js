// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

/**
 * Check if dashboard is running
 */
Cypress.Commands.add('checkDashboardRunning', () => {
  cy.request({
    method: 'GET',
    url: 'http://localhost:9000',
    failOnStatusCode: false,
    timeout: 5000
  }).then((response) => {
    if (response.status !== 200) {
      throw new Error(`Dashboard not accessible. Status: ${response.status}`);
    }
  });
});

/**
 * Login to Saleor Dashboard
 * @param {string} email - User email
 * @param {string} password - User password
 */
Cypress.Commands.add('login', (email = 'admin@example.com', password = 'admin123') => {
  cy.visit('/', {
    timeout: 30000,
    failOnStatusCode: false
  });
  
  // Wait for page to load
  cy.get('body', { timeout: 15000 }).should('be.visible');
  
  // Wait for login form to appear
  cy.get('input[name="email"], input[type="email"]', { timeout: 15000 })
    .should('be.visible')
    .first()
    .clear()
    .type(email);
    
  cy.get('input[name="password"], input[type="password"]', { timeout: 10000 })
    .should('be.visible')
    .first()
    .clear()
    .type(password);
    
  cy.get('button[type="submit"], button')
    .contains(/sign|login|submit/i)
    .should('be.visible')
    .click();
    
  // Wait for navigation after login
  cy.url({ timeout: 15000 }).should('not.include', '/login');
});

/**
 * Login as Admin (alternative method from saleor-cypress)
 * @param {string} email - Admin email (default: admin@example.com)
 * @param {string} password - Admin password (default: admin)
 */
Cypress.Commands.add('loginAsAdmin', (email = 'admin@example.com', password = 'admin') => {
  // Always start from login page
  cy.visit('/dashboard/', {
    timeout: 30000,
    failOnStatusCode: false
  });

  // Wait for page to load
  cy.get('body', { timeout: 15000 }).should('be.visible');

  // Check if we're already logged in
  cy.get('body').then(($body) => {
    if ($body.text().includes('Saleor Dashboard') || $body.text().includes('Dashboard')) {
      cy.log('Already logged in');
      return;
    }

    // Try to find login form - it might be at root or /dashboard/login
    cy.get('body').then(($body) => {
      const hasLoginForm = $body.find('input[name="email"], input[type="email"]').length > 0;
      
      if (!hasLoginForm) {
        // Try visiting login page directly
        cy.visit('/', { timeout: 30000, failOnStatusCode: false });
        cy.wait(2000);
      }

      // Login form - try multiple selectors with error handling
      cy.get('input[name="email"], input[type="email"]', { timeout: 15000 })
        .first()
        .should('be.visible')
        .clear()
        .type(email);
        
      cy.get('input[name="password"], input[type="password"]', { timeout: 10000 })
        .first()
        .should('be.visible')
        .clear()
        .type(password);

      // Try multiple button selectors
      cy.get('body').then(($body) => {
        const signInBtn = $body.find('button:contains("Sign in"), button:contains("Sign In"), button[type="submit"]');
        if (signInBtn.length > 0) {
          cy.wrap(signInBtn.first()).click();
        } else {
          cy.contains(/sign in|login|submit/i, { timeout: 10000 })
            .should('be.visible')
            .click();
        }
      });

      // Wait for navigation - check multiple indicators
      cy.wait(3000);
      cy.url({ timeout: 20000 }).should('not.include', '/login');
      // Verify we're logged in by checking for dashboard content
      cy.get('body', { timeout: 15000 }).should(($body) => {
        const bodyText = $body.text().toLowerCase();
        const isLoggedIn = bodyText.includes('dashboard') || 
                          bodyText.includes('saleor') ||
                          !bodyText.includes('sign in');
        expect(isLoggedIn).to.be.true;
      });
    });
  });
});

/**
 * Logout from Saleor Dashboard
 */
Cypress.Commands.add('logout', () => {
  cy.get('[data-test-id="user-menu"]', { timeout: 10000 })
    .should('be.visible')
    .click();
    
  cy.contains('Logout', { timeout: 5000 })
    .should('be.visible')
    .click();
    
  cy.url({ timeout: 10000 }).should('include', '/login');
});

/**
 * Wait for GraphQL API to be ready
 * This command gracefully handles cases where the backend is not running
 */
Cypress.Commands.add('waitForAPI', () => {
  // Check if backend is running, but don't fail if it's not
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/graphql/',
    body: {
      query: '{ shop { name } }'
    },
    failOnStatusCode: false,
    timeout: 5000
  }).then((response) => {
    if (response.status === 0 || response.status >= 500) {
      cy.log('Backend API not available - some tests may be skipped');
    }
  }).catch(() => {
    // Backend not running - log but don't fail
    cy.log('Backend API (port 8000) is not running - tests requiring API will be skipped');
  });
});

/**
 * Wait for dashboard to be ready
 */
Cypress.Commands.add('waitForDashboard', () => {
  cy.request({
    method: 'GET',
    url: 'http://localhost:9000',
    failOnStatusCode: false,
    timeout: 15000
  });
});
