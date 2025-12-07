# Saleor Cypress Clean Project

## 1. Install dependencies

```bash
npm install
```

## 2. Make sure Saleor dashboard is running

The Cypress tests assume Saleor dashboard is available at:

- http://localhost:9000

You already have a superuser from `populatedb`:

- Email: `admin@example.com`
- Password: `admin`

## 3. Optional: set different admin credentials

Create a file called `cypress.env.json` in this folder if you changed the admin:

```json
{
  "ADMIN_EMAIL": "admin@example.com",
  "ADMIN_PASSWORD": "admin"
}
```

## 4. Run tests

Interactive mode:

```bash
npx cypress open
```

Headless mode (for CI):

```bash
npx cypress run
```

The specs live in:

- `cypress/e2e/auth_navigation.cy.js`
- `cypress/e2e/products.cy.js`
- `cypress/e2e/inventory.cy.js`
