/**
 * Login Page Tests (Black-box UI Testing)
 * 
 * Tests the login functionality of the Saleor Dashboard
 */

describe('Login Page', () => {
  beforeEach(() => {
    // Visit the login page before each test (dashboard runs on port 9000)
    cy.visit('/');
  });

  it('should display login form', () => {
    // Check if login form elements are visible
    cy.get('input[name="email"]').should('be.visible');
    cy.get('input[name="password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible');
  });

  it('should show error for invalid credentials', () => {
    // Try to login with wrong credentials
    cy.get('input[name="email"]').type('wrong@example.com');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    
    // Should show error message (adjust selector based on actual error display)
    cy.contains('Invalid', { timeout: 5000 }).should('be.visible');
  });

  it('should successfully login with valid credentials', () => {
    // Login with valid credentials
    cy.login('admin@example.com', 'admin123');
    
    // Should redirect to dashboard (not login page)
    cy.url().should('not.include', '/login');
    cy.url().should('include', '/dashboard');
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

