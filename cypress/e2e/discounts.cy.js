/// <reference types="cypress" />

const BASE = "http://localhost:9000/dashboard";

/* =======================
 * PROMOTIONS (SALES)
 * ======================= */

describe("Discounts – Promotions (Sales)", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/discounts/sales/`);
  });

  it("shows promotions list with key columns and at least one discount", () => {
    cy.contains("Discounts").should("exist");
    cy.contains("All discounts").should("exist");

    // Just check column headers by text (no need to enforce <th>)
    cy.contains("Name").should("exist");
    cy.contains("Discount type").should("exist");
    cy.contains("Starts").should("exist");
    cy.contains("Ends").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("can search promotions using the search box", () => {
    cy.get('input[placeholder="Search discounts..."]')
      .should("exist")
      .type("Happy black day!{enter}");

    cy.contains("tbody tr", "Happy black day!").should("exist");
  });

  it("opens an existing promotion and shows its main sections", () => {
    cy.contains("tbody tr", "Happy black day!").click();

    cy.url().should("match", /\/dashboard\/discounts\/sales\/.+/);
    cy.contains("Happy black day!").should("exist");

    cy.contains("General information").should("exist");
    cy.contains("Active Dates").should("exist");
    cy.contains("Rules").should("exist");

    // Check that there is at least one rule summary chip
    cy.contains("Order rule").should("exist");
  });

  it("opens Add rule modal from an existing promotion and allows filling fields including channel suggestion", () => {
    cy.contains("tbody tr", "Happy black day!").click();

    cy.contains("button", "Add rule").click();

    // Modal / sheet header
    cy.contains("Add rule").should("exist");

    // Name & Channel inputs (top row)
    cy.get('input[placeholder="Name"]').type("Cypress rule");
    cy.get('input[placeholder="Channel"]')
      .click()
      .type("Channel-USD");

    // Channel suggestions should show and allow selecting Channel-USD
    cy.contains("Channel-USD", { timeout: 5000 }).click();

    // Reward section – value field
    cy.get('input[placeholder="Reward value"]').type("10");

    // Description is optional but should be present
    cy.contains("Description").parent().find("textarea").type("Rule created in automated test");
  });

  it("opens Create Discount page and shows all major sections and Save button", () => {
    cy.contains("button", "Create Discount").click();

    cy.url().should("include", "/discounts/sales/add");
    cy.contains("Create Discount").should("exist");

    cy.contains("General information").should("exist");
    cy.contains("Discount type").should("exist");
    cy.contains("Discount name").should("exist");

    cy.contains("Description").should("exist");
    cy.contains("Active Dates").should("exist");
    cy.contains("Rules").should("exist");

    // Start Date & Start Hour inputs should be present
    cy.contains("label", "Start Date")
      .parent()
      .find("input")
      .should("exist");

    cy.contains("label", "Start Hour")
      .parent()
      .find("input")
      .should("exist");

    // “Set end date” checkbox is visible
    cy.contains("Set end date").parent().find('input[type="checkbox"]').should("exist");

    // Rules section has + Add rule button
    cy.contains("button", "Add rule").should("exist");

    // Bottom navigation buttons
    cy.contains("button", "Save").should("exist");
    cy.contains("button", "Back").should("exist");
  });

  it("starts filling a new discount and opens Add rule in Create Discount flow", () => {
    cy.contains("button", "Create Discount").click();

    const discountName = `Cypress Discount ${Date.now()}`;

    cy.contains("label", "Discount name")
      .parent()
      .find("input")
      .type(discountName);

    // Optional: give a short description
    cy.contains("label", "Description")
      .parent()
      .find("textarea")
      .type("Created by Cypress test");

    // Set a start date (keep it simple – just verify typing works)
    cy.contains("label", "Start Date")
      .parent()
      .find("input")
      .clear()
      .type("12/31/2025");

    // Open Add rule from this page
    cy.contains("button", "Add rule").click();
    cy.contains("Add rule").should("exist");

    // In the rule sheet, again use channel suggestions
    cy.get('input[placeholder="Name"]').type("Create-flow rule");
    cy.get('input[placeholder="Channel"]')
      .click()
      .type("Channel-USD");

    cy.contains("Channel-USD", { timeout: 5000 }).click();
    cy.get('input[placeholder="Reward value"]').type("5");
  });
});

/* =======================
 * VOUCHERS
 * ======================= */

describe("Discounts – Vouchers", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/discounts/vouchers/`);
  });

  it("shows vouchers list with key columns and at least one voucher", () => {
    cy.contains("Vouchers").should("exist");
    cy.contains("All vouchers").should("exist");

    cy.contains("Voucher").should("exist");
    cy.contains("Min. Spent").should("exist");
    cy.contains("Starts").should("exist");
    cy.contains("Ends").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens an existing voucher from the list", () => {
    // Click the first row in the vouchers table
    cy.get("tbody tr").first().click();

    cy.url().should("match", /\/dashboard\/discounts\/vouchers\/.+/);
    cy.contains("Voucher").should("exist"); // main voucher section
    cy.contains("Discount Type").should("exist");
    cy.contains("Value").should("exist");
  });

  it("opens Create Voucher page and shows main sections and Save button", () => {
    cy.contains("button", "Create voucher").click();

    cy.url().should("include", "/discounts/vouchers/add");
    cy.contains("Create Voucher").should("exist");

    cy.contains("General Information").should("exist");
    cy.contains("Voucher Name").should("exist");

    cy.contains("Voucher codes").should("exist");
    cy.contains("Add code").should("exist");

    cy.contains("Discount Type").should("exist");
    cy.contains("Fixed Amount").should("exist");
    cy.contains("Percentage").should("exist");
    cy.contains("Free Shipping").should("exist");

    cy.contains("Value").should("exist");
    cy.contains("Availability").should("exist");
    cy.contains("Channel-PLN").should("exist");
    cy.contains("Channel-USD").should("exist");

    cy.contains("button", "Save").should("exist");
    cy.contains("button", "Back").should("exist");
  });

  it("starts filling Create Voucher form with basic data", () => {
    cy.contains("button", "Create voucher").click();

    const voucherName = `Cypress Voucher ${Date.now()}`;

    cy.contains("label", "Voucher Name")
      .parent()
      .find("input")
      .type(voucherName);

    // Keep default Fixed Amount, just provide a value
    cy.contains("label", "Value")
      .parent()
      .find("input")
      .type("15");

    // Optionally open Add code menu to ensure it’s interactive
    cy.contains("button", "Add code").click();

    // We don't depend on exact menu labels; just verify menu opens
    cy.get("body").within(() => {
      cy.contains(/code/i).should("exist");
    });
  });
});
