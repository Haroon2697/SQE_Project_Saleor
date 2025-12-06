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
 * Login to Saleor Dashboard
 * @param {string} email - User email
 * @param {string} password - User password
 */
Cypress.Commands.add('login', (email = 'admin@example.com', password = 'admin123') => {
  cy.visit('/');  // Dashboard root URL
  // Wait for login form to appear
  cy.get('input[name="email"], input[type="email"]', { timeout: 10000 }).first().type(email);
  cy.get('input[name="password"], input[type="password"]').first().type(password);
  cy.get('button[type="submit"], button').contains(/sign|login|submit/i).click();
  // Wait for navigation after login
  cy.url({ timeout: 10000 }).should('not.include', '/login');
});

/**
 * Logout from Saleor Dashboard
 */
Cypress.Commands.add('logout', () => {
  cy.get('[data-test-id="user-menu"]').click();
  cy.contains('Logout').click();
  cy.url().should('include', '/login');
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
    failOnStatusCode: false
  });
});

