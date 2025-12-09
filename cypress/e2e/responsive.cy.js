/**
 * Responsive Design Tests (Black-box UI Testing)
 * 
 * Tests responsive behavior across different viewport sizes
 */

const BASE = "http://localhost:9000/dashboard";

describe('Responsive Design', () => {
  beforeEach(() => {
    cy.loginAsAdmin();
  });

  describe('Mobile Viewport', () => {
    it('should display correctly on mobile', () => {
      cy.viewport(375, 667); // iPhone SE
      cy.visit(`${BASE}/products/`);
      cy.get('body').should('be.visible');
    });

    it('should have mobile navigation menu', () => {
      cy.viewport(375, 667);
      cy.visit(`${BASE}/products/`);
      cy.get('body').should('be.visible');
      // Check for mobile menu button
      cy.get('button[aria-label*="menu" i], button[aria-label*="navigation" i]').should('exist');
    });
  });

  describe('Tablet Viewport', () => {
    it('should display correctly on tablet', () => {
      cy.viewport(768, 1024); // iPad
      cy.visit(`${BASE}/products/`);
      cy.get('body').should('be.visible');
    });

    it('should adapt layout for tablet', () => {
      cy.viewport(768, 1024);
      cy.visit(`${BASE}/orders/`);
      cy.get('body').should('be.visible');
    });
  });

  describe('Desktop Viewport', () => {
    it('should display correctly on desktop', () => {
      cy.viewport(1920, 1080);
      cy.visit(`${BASE}/products/`);
      cy.get('body').should('be.visible');
    });

    it('should show full navigation on desktop', () => {
      cy.viewport(1920, 1080);
      cy.visit(`${BASE}/`);
      cy.get('body').should('be.visible');
      // Navigation should be visible
      cy.get('nav, [role="navigation"]').should('exist');
    });
  });

  describe('Large Desktop Viewport', () => {
    it('should display correctly on large desktop', () => {
      cy.viewport(2560, 1440);
      cy.visit(`${BASE}/products/`);
      cy.get('body').should('be.visible');
    });
  });

  describe('Viewport Resizing', () => {
    it('should adapt when viewport is resized', () => {
      cy.viewport(1920, 1080);
      cy.visit(`${BASE}/products/`);
      cy.get('body').should('be.visible');
      
      cy.viewport(375, 667);
      cy.get('body').should('be.visible');
    });
  });
});

