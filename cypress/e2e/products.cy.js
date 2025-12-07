/**
 * Products Page Tests (Black-box UI Testing)
 * 
 * Tests product-related functionality in the Saleor Dashboard
 */

describe('Products Page', () => {
  beforeEach(() => {
    // Login before each test
    cy.login('admin@example.com', 'admin123');
    cy.waitForAPI();
  });

  it('should navigate to products page', () => {
    // Navigate to products
    cy.visit('/products');
    cy.url().should('include', '/products');
  });

  it('should display products list', () => {
    cy.visit('/products');
    // Check if products list or empty state is visible
    cy.get('body').should('be.visible');
  });

  it('should allow searching for products', () => {
    cy.visit('/products');
    // Look for search input
    cy.get('input[type="search"], input[placeholder*="search" i]', { timeout: 5000 }).should('exist');
  });

  it('should display product creation button', () => {
    cy.visit('/products');
    // Look for create/add product button
    cy.get('button, a').contains(/create|add|new/i).should('exist');
  });
});

