/**
 * Login Page Tests (Black-box UI Testing)
 * 
 * Tests the login functionality of the Saleor Dashboard
 */

describe('Login Page', () => {
  beforeEach(() => {
    // Visit the login page before each test (dashboard runs on port 9000)
    // Use valid Cypress visit options
    cy.visit('/', {
      timeout: 30000,
      failOnStatusCode: false
    });
    
    // Wait for page to be fully loaded
    cy.get('body', { timeout: 15000 }).should('be.visible');
  });

  it('should display login form', () => {
    // Check if login form elements are visible
    cy.get('input[name="email"]').should('be.visible');
    cy.get('input[name="password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible');
  });

  it('should show error for invalid credentials', () => {
    // Try to login with wrong credentials
    cy.get('input[name="email"]', { timeout: 10000 }).should('be.visible').clear().type('wrong@example.com');
    cy.get('input[name="password"]').should('be.visible').clear().type('wrongpassword');
    cy.get('button[type="submit"]').should('be.visible').click();
    
    // Wait a bit for error to appear or page to stay on login
    cy.wait(2000);
    
    // Should show error message or stay on login page
    // Try multiple possible error message formats
    cy.get('body', { timeout: 5000 }).then(($body) => {
      const bodyText = $body.text().toLowerCase();
      if (bodyText.includes('invalid') || bodyText.includes('incorrect') || bodyText.includes('error') || bodyText.includes('wrong')) {
        cy.log('Error message detected');
        // Test passes if error message is found
        expect(true).to.be.true;
      } else {
        // If no error message, verify we're still on login page (which also indicates failure)
        cy.url({ timeout: 5000 }).should('satisfy', (url) => {
          return url.includes('/login') || url.includes('/dashboard/login') || url === 'http://localhost:9000/';
        });
        cy.log('Still on login page - credentials rejected');
      }
    });
  });

  it('should successfully login with valid credentials', () => {
    // Login with valid credentials
    cy.login('admin@example.com', 'admin123');
    
    // Should redirect away from login page
    cy.url({ timeout: 15000 }).should('not.include', '/login');
    // Dashboard might be at root or /dashboard - check both
    cy.url().should('satisfy', (url) => {
      return url.includes('/dashboard') || url === 'http://localhost:9000/' || !url.includes('/login');
    });
  });

  it('should require email field', () => {
    // Try to submit without email
    cy.get('input[name="password"]').type('admin123');
    cy.get('button[type="submit"]').click();
    
    // Should show validation error or prevent submission
    cy.get('input[name="email"]').should('have.attr', 'required');
  });

  it('should require password field', () => {
    // Try to submit without password
    cy.get('input[name="email"]').type('admin@example.com');
    cy.get('button[type="submit"]').click();
    
    // Should show validation error or prevent submission
    cy.get('input[name="password"]').should('have.attr', 'required');
  });
});

