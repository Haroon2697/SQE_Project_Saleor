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

  // Login form
  cy.get('input[name="email"]', { timeout: 15000 })
    .should('be.visible')
    .clear()
    .type(email);
    
  cy.get('input[name="password"]', { timeout: 10000 })
    .should('be.visible')
    .clear()
    .type(password);

  cy.contains(/sign in/i, { timeout: 10000 })
    .should('be.visible')
    .click();

  // Logged in indicator – text in left top of dashboard
  cy.contains('Saleor Dashboard', { timeout: 15000 }).should('exist');
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
 */
Cypress.Commands.add('waitForAPI', () => {
  // Wait for backend GraphQL API (port 8000)
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/graphql/',
    body: {
      query: '{ shop { name } }'
    },
    failOnStatusCode: false,
    timeout: 10000
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
