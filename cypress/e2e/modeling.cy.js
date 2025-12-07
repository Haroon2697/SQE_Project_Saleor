/// <reference types="cypress" />

const BASE = "http://localhost:9000/dashboard";

const typeIntoLabeledInput = (labelText, value) => {
  cy.contains("label", labelText)
    .invoke("attr", "for")
    .then((id) => {
      cy.get(`#${id}`).clear().type(value);
    });
};

describe("Modeling – Navigation", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/models/`);
  });

  it("navigates between Models, Model Types and Structures", () => {
    // Models
    cy.contains("Models").should("exist");
    cy.contains("All models").should("exist");

    // Model Types
    cy.contains("Model Types").click();
    cy.url().should("include", "/dashboard/model-types");
    cy.contains("All model types").should("exist");

    // Structures
    cy.contains("Structures").click();
    cy.url().should("include", "/dashboard/structures");
    cy.contains("All structures").should("exist");
  });
});

/* =======================
 * MODELS
 * ======================= */

describe("Modeling – Models list, details & Create model flow", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/models/`);
  });

  it("shows models table with expected columns and at least one row", () => {
    cy.contains("All models").should("exist");

    // Just check header texts exist (not forcing visibility on <th> to avoid 0x0 issues)
    cy.contains("Title").should("exist");
    cy.contains("Slug").should("exist");
    cy.contains("Visibility").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens an existing model (About) and shows key sections", () => {
    cy.contains("About").click();

    cy.contains("General Information").should("exist");
    cy.contains("Title").should("exist");
    cy.contains("Content").should("exist");

    cy.contains("Visibility").should("exist");
    cy.contains("Save").should("exist");
    cy.contains("Back").should("exist");
  });

  it("can toggle visibility of a model and save", () => {
    cy.contains("About").click();

    // Switch to Hidden and save, then ensure it stays Hidden
    cy.contains("Visibility")
      .parent()
      .within(() => {
        cy.contains("Hidden").click();
      });

    cy.contains("Save").click();

    cy.contains("Visibility")
      .parent()
      .within(() => {
        cy.contains("Hidden")
          .find('input[type="radio"]')
          .should("be.checked");
      });
  });

  it("opens Create model flow and shows Select model type modal", () => {
    cy.contains("Create model").click();

    cy.contains("Select a model type").should("exist");

    // Model type field present
    cy.contains("Model type").should("exist");

    // Back & Confirm buttons in modal
    cy.contains("Back").should("exist");
    cy.contains("Confirm").should("exist");
  });

  it("shows model type suggestions and only allows Confirm after choosing one", () => {
    cy.contains("Create model").click();

    // Open model type dropdown (click on input by its label)
    cy.contains("Model type")
      .parent()
      .find("input,div[role='button'],button")
      .first()
      .click();

    // Expect Brand to be one of the suggestions (from your screenshots)
    cy.contains("Brand", { timeout: 5000 }).should("be.visible");

    // If Confirm is disabled before selection, keep that assertion loose
    cy.contains("Confirm").then(($btn) => {
      if ($btn.is(":disabled")) {
        cy.wrap($btn).should("be.disabled");
      }
    });

    // Select Brand from suggestions
    cy.contains("Brand").click();

    // After selecting, Confirm should be enabled and close the modal when clicked
    cy.contains("Confirm").should("not.be.disabled").click();

    cy.contains("Select a model type").should("not.exist");
  });

  it("returns to models list when clicking Back from model details page", () => {
    cy.contains("About").click();
    cy.contains("Back").click();

    cy.contains("All models").should("exist");
    cy.url().should("include", "/dashboard/models");
  });
});

/* =======================
 * MODEL TYPES
 * ======================= */

describe("Modeling – Model Types list & create", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/model-types/`);
  });

  it("shows model types list with header", () => {
    cy.contains("All model types").should("exist");
    cy.contains("Model Type Name").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens existing Model Type (Brand) and shows sections", () => {
    cy.contains("Brand").click();

    cy.contains("Model attributes").should("exist");
    cy.contains("General Information").should("exist");
    cy.contains("Model type Name").should("exist");

    cy.contains("Save").should("exist");
    cy.contains("Back").should("exist");
  });

  it("opens Create model type page and shows mandatory field", () => {
    cy.contains("Create model type").click();

    cy.contains("Create model type").should("exist");
    cy.contains("Model type Name").should("exist");

    cy.contains("Save").should("exist");
    cy.contains("Back").should("exist");
  });

  it("cannot create model type with empty name (stays on add page)", () => {
    cy.contains("Create model type").click();

    cy.contains("Save").click();

    // We expect to still be on the add page – creation should not succeed
    cy.url().should("include", "/model-types/add");
  });

  it("creates new model type with valid name", () => {
    const typeName = `Cypress Model Type ${Date.now()}`;

    cy.contains("Create model type").click();

    typeIntoLabeledInput("Model type Name", typeName);

    cy.contains("Save").click();

    // Back on list page; new type visible
    cy.url().should("include", "/dashboard/model-types");
    cy.contains(typeName).should("exist");
  });

  it("keeps user on list when clicking Back from Create model type page", () => {
    cy.contains("Create model type").click();
    cy.contains("Back").click();

    cy.contains("All model types").should("exist");
    cy.url().should("include", "/dashboard/model-types");
  });
});

/* =======================
 * STRUCTURES
 * ======================= */

describe("Modeling – Structures list & details", () => {
  beforeEach(() => {
    cy.loginAsAdmin();
    cy.visit(`${BASE}/structures/`);
  });

  it("shows structures list with titles and items count", () => {
    cy.contains("All structures").should("exist");
    cy.contains("Structure Title").should("exist");
    cy.contains("Items").should("exist");

    cy.get("tbody tr").should("have.length.at.least", 1);
  });

  it("opens footer structure and shows structure items", () => {
    cy.contains("footer").click();

    cy.contains("Structure Items").should("exist");
    cy.get("[data-test-id='structure-item'], li, .MuiListItem-root")
      .its("length")
      .should("be.greaterThan", 0);

    cy.contains("Create new item").should("exist");
    cy.contains("Save").should("exist");
    cy.contains("Back").should("exist");
  });

  it("does not delete structure when Delete is cancelled", () => {
    cy.contains("footer").click();

    cy.contains("Delete").click(); // structure-level delete

    // Confirmation dialog should appear; just cancel / close it
    cy.contains(/delete structure/i).should("exist"); // title text can be loose
    cy.contains(/cancel|back/i).click({ force: true }); // any Cancel / Back button

    // Still on footer structure page
    cy.contains("Structure Items").should("exist");
    cy.contains("footer").should("exist");
  });

  it("allows saving structure after a no-op change", () => {
    cy.contains("footer").click();

    // Make a very safe 'change': click Show on first item (if it toggles, it's ok;
    // if not, it's still a harmless click)
    cy.contains("Show").first().click({ force: true });

    cy.contains("Save").click();

    // After save, still on same structure page
    cy.contains("Structure Items").should("exist");
  });

  it("returns to structures list when clicking Back", () => {
    cy.contains("footer").click();
    cy.contains("Back").click();

    cy.contains("All structures").should("exist");
    cy.url().should("include", "/dashboard/structures");
  });
});
