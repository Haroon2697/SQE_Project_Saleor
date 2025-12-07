// cypress/support/commands.js

Cypress.Commands.add(
  "loginAsAdmin",
  (email = "admin@example.com", password = "admin") => {
    // Always start from login page
    cy.visit("http://localhost:9000/dashboard/");

    // Login form
    cy.get('input[name="email"]').should("be.visible").clear().type(email);
    cy.get('input[name="password"]').should("be.visible").clear().type(password);

    cy.contains(/sign in/i).click();

    // Logged in indicator – text in left top of dashboard
    cy.contains("Saleor Dashboard", { timeout: 10000 }).should("exist");
  }
);
