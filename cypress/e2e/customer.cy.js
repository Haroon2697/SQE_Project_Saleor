/// <reference types="cypress" />

const BASE = "http://localhost:9000/dashboard";

describe("Customers – list, details, create & delete", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
  });

  /* =======================
   * LIST PAGE
   * ======================= */

  it("shows Customers list with key columns and at least one customer", () => {
    cy.visit(`${BASE}/customers/`);

    cy.contains("Customers").should("exist");
    cy.contains("All customers").should("exist");

    cy.contains("th", "Customer name").should("exist");
    cy.contains("th", "Customer e-mail").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("filters customers using search input", () => {
    cy.visit(`${BASE}/customers/`);

    cy.get('input[placeholder="Search customers..."]')
      .should("exist")
      .type("Ashley{enter}");

    cy.contains("tbody tr", "Ashley Cook").should("exist");
  });

  it("opens customer details when clicking a row", () => {
    cy.visit(`${BASE}/customers/`);

    cy.contains("tbody tr", "Ashley Cook").click();

    cy.url().should("match", /\/dashboard\/customers\/.+/);
    cy.contains("Ashley Cook").should("exist");
    cy.contains("User account active").should("exist");
    cy.contains("Account Information").should("exist");
    cy.contains("Address Information").should("exist");
  });

  /* =======================
   * EXISTING CUSTOMER – EDIT & SAVE
   * ======================= */

  it("updates note for an existing customer and saves without confirmation popup", () => {
    cy.visit(`${BASE}/customers/`);
    cy.contains("tbody tr", "Ashley Cook").click();

    const noteText = `Updated by Cypress at ${Date.now()}`;

    cy.contains("label", "Note")
      .parent()
      .find("textarea")
      .clear()
      .type(noteText);

    // Save should directly save – no confirmation dialog
    cy.contains("button", "Save").click();

    // Still on same customer page
    cy.url().should("match", /\/dashboard\/customers\/.+/);

    // Note is persisted
    cy.contains("label", "Note")
      .parent()
      .find("textarea")
      .should("have.value", noteText);
  });

  /* =======================
   * CREATE CUSTOMER
   * ======================= */

  it("opens Create customer page and shows main sections", () => {
    cy.visit(`${BASE}/customers/`);

    cy.contains("Create customer").click();

    cy.url().should("include", "/dashboard/customers/add");
    cy.contains("Create Customer").should("exist");

    cy.contains("Customer Overview").should("exist");
    cy.contains("Primary Address").should("exist");
    cy.contains("Notes").should("exist");

    cy.contains("button", "Save").should("exist");
    cy.contains("button", "Back").should("exist");
  });

  it("does not navigate away when saving an empty Create customer form", () => {
    cy.visit(`${BASE}/customers/add`);

    cy.url().should("include", "/customers/add");
    cy.contains("button", "Save").click();

    // We should still be on the create form page (validation prevented navigation)
    cy.url().should("include", "/customers/add");
  });

  it("creates a new customer by filling mandatory fields and selecting Country from suggestions", () => {
    cy.visit(`${BASE}/customers/add`);

    const uniqueSuffix = Date.now();
    const firstName = `Test${uniqueSuffix}`;
    const lastName = "Customer";
    const email = `test.customer.${uniqueSuffix}@example.com`;

    // --- Customer Overview ---
    cy.contains("label", "First Name")
      .parent()
      .find("input")
      .type(firstName);

    cy.contains("label", "Last Name")
      .parent()
      .find("input")
      .type(lastName);

    cy.contains("label", "Email address")
      .parent()
      .find("input")
      .type(email);

    // --- Primary Address (fill common mandatory ones) ---
    cy.contains("label", "First Name")
      .filter(':contains("First Name")')
      .eq(1) // the second "First Name" label – in Primary Address
      .parent()
      .find("input")
      .type(firstName);

    cy.contains("label", "Last Name")
      .filter(':contains("Last Name")')
      .eq(1)
      .parent()
      .find("input")
      .type(lastName);

    cy.contains("label", "Address line 1")
      .parent()
      .find("input")
      .type("123 Cypress Street");

    cy.contains("label", "City")
      .parent()
      .find("input")
      .type("Testville");

    cy.contains("label", "ZIP / Postal code")
      .parent()
      .find("input")
      .type("12345");

    // Country – uses suggestion dropdown. Click, type, pick from suggestion.
    cy.contains("label", "Country")
      .parent()
      .within(() => {
        cy.get("input, [role='combobox']").click().type("United States");
      });

    cy.contains("United States of America", { timeout: 5000 }).click();

    // --- Save (no confirmation dialog expected) ---
    cy.contains("button", "Save").click();

    // After save, we should be on the new customer's detail page
    cy.url().should("match", /\/dashboard\/customers\/.+/);
    cy.contains(firstName).should("exist");
    cy.contains(lastName).should("exist");
    cy.contains(email).should("exist");
  });

  /* =======================
   * DELETE CUSTOMER – CONFIRMATION REQUIRED
   * ======================= */

  it("shows confirmation when deleting a customer and deletes after confirming", () => {
    // First, create a lightweight customer to delete
    cy.visit(`${BASE}/customers/add`);

    const uniqueSuffix = Date.now();
    const firstName = `DeleteMe${uniqueSuffix}`;
    const lastName = "Temp";
    const email = `deleteme.${uniqueSuffix}@example.com`;

    cy.contains("label", "First Name")
      .parent()
      .find("input")
      .type(firstName);

    cy.contains("label", "Last Name")
      .parent()
      .find("input")
      .type(lastName);

    cy.contains("label", "Email address")
      .parent()
      .find("input")
      .type(email);

    cy.contains("button", "Save").click();

    cy.url().should("match", /\/dashboard\/customers\/.+/);
    cy.contains(email).should("exist");

    // --- Delete flow ---
    cy.contains("button", "Delete").click();

    // Confirmation dialog should appear
    cy.contains(/delete customer/i).should("exist");

    // First cancel to ensure it doesn’t delete without explicit confirm
    cy.contains(/cancel/i).click();
    cy.contains(email).should("exist");

    // Delete again and confirm this time
    cy.contains("button", "Delete").click();
    cy.contains(/delete customer/i).should("exist");
    cy.contains(/^delete$/i).click(); // confirm button inside dialog

    // After deletion, we should be back on Customers list and customer should not exist
    cy.url().should("include", "/dashboard/customers");
    cy.contains(email).should("not.exist");
  });
});
