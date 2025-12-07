/// <reference types="cypress" />

const BASE = "http://localhost:9000/dashboard";

/* =======================
 * NAVIGATION
 * ======================= */

describe("Catalog – Navigation", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/products/`);
  });

  it("navigates between Products, Categories, Collections and Gift Cards", () => {
    // Products
    cy.contains("All products").should("exist");

    // Categories
    cy.contains("Categories").click();
    cy.url().should("include", "/dashboard/categories");
    cy.contains("All Categories").should("exist");

    // Collections
    cy.contains("Collections").click();
    cy.url().should("include", "/dashboard/collections");
    cy.contains("All Collections").should("exist");

    // Gift Cards
    cy.contains("Gift Cards").click();
    cy.url().should("include", "/dashboard/gift-cards");
    cy.contains("All gift cards").should("exist");
  });
});

/* =======================
 * PRODUCTS
 * ======================= */

describe("Catalog – Products list & Create product", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/products/`);
  });

  it("shows products table with key columns and at least one product", () => {
    cy.contains("All products").should("exist");

    cy.contains("th", "Product").should("exist");
    cy.contains("th", "Availability").should("exist");
    cy.contains("th", "Description").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("filters products using search input", () => {
    const searchText = "Gift card";

    cy.get('input[placeholder="Search Products..."]')
      .should("exist")
      .type(`${searchText}{enter}`);

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens Create Product flow and shows Select product type modal", () => {
    cy.contains("Create Product").click();

    cy.contains("Select a product type").should("exist");
    cy.get('input[placeholder="Product type"]').should("exist");
    cy.contains("Back").should("exist");
    cy.contains("Confirm").should("be.disabled");
  });

  it("shows product type suggestions when typing and includes Audiobook", () => {
    cy.contains("Create Product").click();

    cy.get('input[placeholder="Product type"]').click().type("audio");

    cy.contains("Audiobook", { timeout: 5000 }).should("exist");
  });

  it("does NOT allow confirming with an arbitrary product type (e.g. 'aaa')", () => {
    cy.contains("Create Product").click();

    cy.get('input[placeholder="Product type"]').click().clear().type("aaa");

    cy.contains("Confirm").should("be.disabled");
  });

  it("allows confirming only after selecting a suggestion (Audiobook example)", () => {
    cy.contains("Create Product").click();

    cy.get('input[placeholder="Product type"]').click().type("audio");
    cy.contains("Audiobook").click();

    cy.contains("Confirm").should("not.be.disabled").click();

    cy.url().should("include", "/dashboard/products/add");
    cy.contains("General Information").should("exist");
  });

  it("can cancel Create Product via Back button and return to products list", () => {
    cy.contains("Create Product").click();

    cy.contains("Back").click();

    cy.contains("All products").should("exist");
    cy.url().should("include", "/dashboard/products");
  });
});

/* =======================
 * CATEGORIES
 * ======================= */

describe("Catalog – Categories list & Create category", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/categories/`);
  });

  it("shows categories table with key columns", () => {
    cy.contains("All Categories").should("exist");

    cy.contains("th", "Category name").should("exist");
    cy.contains("th", "Number of products").should("exist");
    cy.contains("th", "Subcategories").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens Create category page and shows main sections", () => {
    cy.contains("Create category").click();

    cy.contains("Create New Category").should("exist");
    cy.contains("General Information").should("exist");

    // Category Name input by label
    cy.contains("label", "Category Name")
      .parent()
      .find("input")
      .should("exist");

    cy.contains("label", "Category Description")
      .parent()
      .find("textarea")
      .should("exist");

    cy.contains("Search Engine Preview").should("exist");
    cy.contains("Metadata").should("exist");
    cy.contains("Private Metadata").should("exist");

    cy.contains("Save").should("exist");
    cy.contains("Back").should("exist");
  });

  it("does not navigate away when saving with empty Category Name", () => {
    cy.contains("Create category").click();

    cy.url().should("include", "/categories/add");
    cy.contains("Save").click();

    // Still on add page => validation blocked save
    cy.url().should("include", "/categories/add");
  });

  it("creates a new category successfully when valid data is provided", () => {
    const categoryName = `Test Category ${Date.now()}`;

    cy.contains("Create category").click();

    cy.contains("label", "Category Name")
      .parent()
      .find("input")
      .type(categoryName);

    cy.contains("label", "Category Description")
      .parent()
      .find("textarea")
      .type("Created via Cypress test");

    cy.contains("Save").click();

    cy.url().should("include", "/dashboard/categories");
    cy.contains(categoryName).should("exist");
  });

  it("expands Search Engine Preview section", () => {
    cy.contains("Create category").click();

    cy.contains("Search Engine Preview").click();

    cy.contains("Slug").should("exist");
    cy.contains("Search engine title").should("exist");
    cy.contains("Search engine description").should("exist");
  });

  it("keeps user on list page when clicking Back from Create category", () => {
    cy.contains("Create category").click();
    cy.contains("Back").click();

    cy.contains("All Categories").should("exist");
    cy.url().should("include", "/dashboard/categories");
  });
});

/* =======================
 * COLLECTIONS
 * ======================= */

describe("Catalog – Collections list & Add collection", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/collections/`);
  });

  it("shows collections table with basic columns", () => {
    cy.contains("All Collections").should("exist");

    cy.contains("th", "Collection Name").should("exist");
    cy.contains("th", "No. of Products").should("exist");
    cy.contains("th", "Availability").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens Add Collection page and shows required fields", () => {
    cy.contains("Create collection").click();

    cy.contains("Add Collection").should("exist");

    cy.contains("label", "Name")
      .parent()
      .find("input")
      .should("exist");

    cy.contains("label", "Description")
      .parent()
      .find("textarea")
      .should("exist");

    cy.contains("Background Image").should("exist");
    cy.contains("Search Engine Preview").should("exist");
    cy.contains("Availability").should("exist");

    cy.contains("Save").should("exist");
    cy.contains("Back").should("exist");
  });

  it("does not navigate away when saving without Name", () => {
    cy.contains("Create collection").click();

    cy.url().should("include", "/collections/add");
    cy.contains("Save").click();

    cy.url().should("include", "/collections/add");
  });

  it("creates new collection with valid data", () => {
    const collectionName = `Cypress Collection ${Date.now()}`;

    cy.contains("Create collection").click();

    cy.contains("label", "Name")
      .parent()
      .find("input")
      .type(collectionName);

    cy.contains("label", "Description")
      .parent()
      .find("textarea")
      .type("Created by automated test");

    cy.contains("Save").click();

    cy.url().should("include", "/dashboard/collections");
    cy.contains(collectionName).should("exist");
  });

  it("allows toggling availability dropdowns for channels", () => {
    cy.contains("Create collection").click();

    cy.contains("Channel-PLN").click();
    cy.contains("Channel-USD").click();
  });
});

/* =======================
 * GIFT CARDS
 * ======================= */

describe("Catalog – Gift cards list & Issue gift card", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/gift-cards/`);
  });

  it("shows gift cards table with key columns", () => {
    cy.contains("All gift cards").should("exist");

    cy.contains("th", "Gift Card").should("exist");
    cy.contains("th", "Status").should("exist");
    cy.contains("th", "Tag").should("exist");
    cy.contains("th", "Product").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens Issue gift card dialog with core elements", () => {
    cy.contains("Issue card").click();

    cy.contains("Issue gift card").should("exist");
    // amount field is number input
    cy.get('input[type="number"]').first().should("exist");
    cy.contains("Back").should("exist");
    cy.contains("Issue").should("exist");
  });

  it("does not navigate away when issuing with invalid amount", () => {
    cy.contains("Issue card").click();
    cy.url().should("include", "action=gift-card-create");

    cy.get('input[type="number"]').first().clear().type("0");
    cy.contains("Issue").click();

    // Still in create dialog URL
    cy.url().should("include", "action=gift-card-create");
  });

  it("issues a new gift card with minimal required data", () => {
    cy.contains("Issue card").click();

    cy.get('input[type="number"]').first().clear().type("10");
    cy.contains("Issue").click();

    cy.url().should("include", "/dashboard/gift-cards");
  });

  it("closes Issue gift card dialog when clicking Back", () => {
    cy.contains("Issue card").click();

    cy.contains("Issue gift card").should("exist");
    cy.contains("Back").click();

    cy.contains("Issue gift card").should("not.exist");
    cy.contains("All gift cards").should("exist");
  });
});
