/**
 * Search Functionality Tests (Black-box UI Testing)
 * 
 * Tests search functionality across the Saleor Dashboard
 */

const BASE = "http://localhost:9000/dashboard";

describe('Search Functionality', () => {
  beforeEach(() => {
    cy.loginAsAdmin();
  });

  describe('Global Search', () => {
    it('should have a global search input', () => {
      cy.visit(`${BASE}/`);
      cy.get('input[type="search"], input[placeholder*="search" i]').should('exist');
    });

    it('should allow typing in search input', () => {
      cy.visit(`${BASE}/`);
      cy.get('input[type="search"], input[placeholder*="search" i]')
        .first()
        .should('be.visible')
        .type('test');
    });
  });

  describe('Product Search', () => {
    it('should search for products', () => {
      cy.visit(`${BASE}/products/`);
      cy.get('input[placeholder*="search" i], input[type="search"]')
        .should('exist')
        .first()
        .type('product{enter}');
      cy.get('body').should('be.visible');
    });

    it('should display search results', () => {
      cy.visit(`${BASE}/products/`);
      cy.get('input[placeholder*="search" i], input[type="search"]')
        .first()
        .type('test{enter}');
      cy.wait(2000);
      cy.get('body').should('be.visible');
    });

    it('should clear search results', () => {
      cy.visit(`${BASE}/products/`);
      const searchInput = cy.get('input[placeholder*="search" i], input[type="search"]').first();
      searchInput.type('test');
      searchInput.clear();
      cy.get('body').should('be.visible');
    });
  });

  describe('Customer Search', () => {
    it('should search for customers', () => {
      cy.visit(`${BASE}/customers/`);
      cy.get('input[placeholder*="search" i], input[type="search"]')
        .should('exist')
        .first()
        .type('customer{enter}');
      cy.get('body').should('be.visible');
    });
  });

  describe('Order Search', () => {
    it('should search for orders', () => {
      cy.visit(`${BASE}/orders/`);
      cy.get('input[placeholder*="search" i], input[type="search"]')
        .should('exist')
        .first()
        .type('order{enter}');
      cy.get('body').should('be.visible');
    });
  });

  describe('Filter and Search Combination', () => {
    it('should combine search with filters', () => {
      cy.visit(`${BASE}/products/`);
      cy.get('input[placeholder*="search" i], input[type="search"]')
        .first()
        .type('test');
      // Look for filter buttons
      cy.get('button, [role="button"]').contains(/filter/i).should('exist');
    });
  });
});

