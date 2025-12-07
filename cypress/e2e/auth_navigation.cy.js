// cypress/e2e/auth_navigation.cy.js

describe("Saleor Authentication & Dashboard Navigation", () => {
  const baseUrl = "http://localhost:9000/dashboard/";
  const adminEmail = "admin@example.com";
  const adminPassword = "admin"; // adjust if different locally

  beforeEach(() => {
    cy.visit(baseUrl);
  });

  // 1. Basic UI render
  it("renders Sign In page with required fields", () => {
    cy.contains("Sign In").should("exist");

    cy.get('input[name="email"]').should("be.visible");
    cy.get('input[name="password"]').should("be.visible");

    cy.contains("Forgot password?").should("be.visible");
    cy.contains("Sign in").should("be.visible");
  });

  // 2. Empty submit validation
  it("shows validation errors when submitting empty credentials", () => {
    cy.contains("Sign in").click();

    // Adjust these to your actual error texts if needed
    cy.contains(/email/i).should("exist");
    cy.contains(/password/i).should("exist");
  });

  // 3. Invalid credentials – confirm we stay on login form
  it("rejects invalid credentials and stays on Sign In page", () => {
    cy.get('input[name="email"]').clear().type("wrong@example.com");
    cy.get('input[name="password"]').clear().type("wrongpass");

    cy.contains("Sign in").click();

    // Still seeing login form
    cy.contains("Sign In").should("be.visible");
    cy.get('input[name="email"]').should("be.visible");
    cy.get('input[name="password"]').should("be.visible");
  });

  
});
