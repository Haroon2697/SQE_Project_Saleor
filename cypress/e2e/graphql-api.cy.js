/**
 * GraphQL API Tests (Black-box API Testing via UI)
 * 
 * Tests GraphQL API endpoints through the UI
 */

describe('GraphQL API', () => {
  beforeEach(() => {
    // Wait for API to be ready
    cy.waitForAPI();
  });

  it('should access GraphQL playground', () => {
    // Visit GraphQL playground on backend (port 8000)
    cy.visit('http://localhost:8000/graphql/');
    
    // Check if GraphQL interface is loaded
    cy.get('body').should('contain', 'GraphQL');
  });

  it('should execute shop query', () => {
    // Make GraphQL request to backend API (port 8000)
    cy.request({
      method: 'POST',
      url: 'http://localhost:8000/graphql/',
      body: {
        query: `
          query {
            shop {
              name
              version
              description
            }
          }
        `
      }
    }).then((response) => {
      // Verify response
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('data');
      if (response.body.data && response.body.data.shop) {
        expect(response.body.data.shop).to.have.property('name');
      } else {
        // Handle case where shop might be null
        expect(response.body.data).to.exist;
      }
    });
  });

  it('should execute products query', () => {
    // Make GraphQL request for products to backend API (port 8000)
    cy.request({
      method: 'POST',
      url: 'http://localhost:8000/graphql/',
      body: {
        query: `
          query {
            products(first: 5) {
              edges {
                node {
                  id
                  name
                  slug
                }
              }
            }
          }
        `
      }
    }).then((response) => {
      // Verify response
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('data');
      expect(response.body.data).to.have.property('products');
    });
  });

  it('should handle invalid GraphQL query', () => {
    // Make invalid GraphQL request to backend API (port 8000)
    cy.request({
      method: 'POST',
      url: 'http://localhost:8000/graphql/',
      body: {
        query: `
          query {
            invalidField {
              name
            }
          }
        `
      },
      failOnStatusCode: false
    }).then((response) => {
      // GraphQL returns 200 even with errors, but some servers return 400
      expect([200, 400]).to.include(response.status);
      // If status is 200, should have errors property
      if (response.status === 200) {
        expect(response.body).to.have.property('errors');
      }
    });
  });
});

