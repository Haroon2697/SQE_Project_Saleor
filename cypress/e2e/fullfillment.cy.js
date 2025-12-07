/// <reference types="cypress" />

const BASE = "http://localhost:9000/dashboard";

describe("Fulfillment – Orders & Drafts", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
  });

  /* =======================
   * ORDERS LIST
   * ======================= */

  it("shows Orders list with key columns and at least one order", () => {
    cy.visit(`${BASE}/orders/`);

    cy.contains("Orders").should("exist");
    cy.contains("All orders").should("exist");

    cy.contains("th", "Number").should("exist");
    cy.contains("th", "Date").should("exist");
    cy.contains("th", "Customer").should("exist");
    cy.contains("th", "Payment").should("exist");
    cy.contains("th", "Fulfillment status").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens an order details page from the Orders list", () => {
    cy.visit(`${BASE}/orders/`);

    cy.get("tbody tr").first().click();

    cy.url().should("match", /\/dashboard\/orders\/.+/);

    cy.contains("Unfulfilled order lines").should("exist");
    cy.contains("Order summary").should("exist");
    cy.contains("Payments summary").should("exist");
    cy.contains("Customer").should("exist");
  });

  /* =======================
   * CREATE DRAFT FROM ORDERS
   * ======================= */

  it("starts creating a draft order from Orders list by selecting a channel suggestion", () => {
    cy.visit(`${BASE}/orders/`);

    cy.contains("Create order").click();

    // Channel modal
    cy.contains("Select a channel").should("exist");

    // The channel select is suggestion-based – type & choose from list
    cy.contains("Channel name")
      .parent()
      .within(() => {
        cy.get("input, div[role='combobox']").click().type("USD");
      });

    cy.contains("Channel-USD").click(); // select from suggestion

    cy.contains("Confirm").click();

    // Should land on a new draft order page
    cy.url().should("include", "/dashboard/orders/drafts/");
    cy.contains(/Draft/i).should("exist");
    cy.contains("Order summary").should("exist");
  });

  /* =======================
   * DRAFTS LIST
   * ======================= */

  it("shows Drafts list and allows opening Create order flow", () => {
    cy.visit(`${BASE}/orders/drafts/`);

    cy.contains("Drafts").should("exist");
    cy.contains("All draft orders").should("exist");
    cy.contains("No orders found").should("exist"); // in your screenshot

    cy.contains("Create order").should("exist").click();

    cy.contains("Select a channel").should("exist");
    cy.contains("Channel name").should("exist");
    cy.contains("Back").should("exist");
    cy.contains("Confirm").should("exist");
  });

  /* =======================
   * FULL DRAFT CREATION FLOW
   * ======================= */

  it("creates a draft order by selecting channel, customer and product from suggestions", () => {
    // ---- Step 1: create draft & select channel from suggestions ----
    cy.visit(`${BASE}/orders/drafts/`);

    cy.contains("Create order").click();
    cy.contains("Select a channel").should("exist");

    cy.contains("Channel name")
      .parent()
      .within(() => {
        cy.get("input, div[role='combobox']").click().type("USD");
      });

    cy.contains("Channel-USD").click(); // select suggestion
    cy.contains("Confirm").click();

    // On draft order detail page
    cy.url().should("include", "/dashboard/orders/drafts/");
    cy.contains(/Draft/i).should("exist");

    // ---- Step 2: choose customer from suggestions ----
    // Open customer picker (label/section will depend on your UI)
    cy.contains("Customer")
      .parent()
      .within(() => {
        // There is usually a button like "Add customer" / "Search customers"
        cy.contains(/add customer|search customers/i).click();
      });

    // Type partial name and pick from suggestion list
    cy.get('input[placeholder*="Search"], input[type="search"]').type(
      "Brenda"
    );
    cy.contains("Brenda Williams", { timeout: 5000 }).click();

    // Check that the customer was attached
    cy.contains("brenda.williams@example.com", { matchCase: false }).should(
      "exist"
    );

    // ---- Step 3: add a product line from suggestions ----
    cy.contains(/add products?|add product/i).click();

    cy.get('input[placeholder*="Search"], input[type="search"]').type("White");

    cy.contains("White Plimsolls", { timeout: 5000 }).click();

    // Confirm add product (Saleor shows a confirm / add button in modal)
    cy.contains(/add|confirm/i).click();

    // At least one line should now appear in order lines table
    cy.contains("White Plimsolls").should("exist");

    // ---- Step 4: save draft ----
    cy.contains("Save").click();

    // After saving, URL stays on this draft and we have no validation errors
    cy.url().should("include", "/dashboard/orders/drafts/");
    cy.contains("Changes saved", { matchCase: false }).should("exist");
  });

  /* =======================
   * CREATE ORDER FLOW FROM DRAFTS – CANCEL
   * ======================= */

  it("can cancel channel selection and remain on Drafts list", () => {
    cy.visit(`${BASE}/orders/drafts/`);

    cy.contains("Create order").click();
    cy.contains("Select a channel").should("exist");

    cy.contains("Back").click();

    cy.contains("All draft orders").should("exist");
    cy.url().should("include", "/dashboard/orders/drafts");
  });
});
