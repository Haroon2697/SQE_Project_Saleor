const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      return config;
    },
    baseUrl: 'http://localhost:9000',  // Dashboard runs on port 9000
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 15000,
    requestTimeout: 15000,
    responseTimeout: 15000,
    pageLoadTimeout: 30000,
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.js',
    fixturesFolder: 'cypress/fixtures',
    videosFolder: 'cypress/videos',
    screenshotsFolder: 'cypress/screenshots',
    // Memory management to prevent Electron crashes
    experimentalMemoryManagement: true,
    numTestsKeptInMemory: 0, // Keep no tests in memory to prevent crashes
    // Retry failed tests
    retries: {
      runMode: 2,
      openMode: 0
    },
    // Block third-party requests that might cause issues
    blockHosts: [],
  },
  projectId: 'rpaahx',
  // Record key should be set via CYPRESS_RECORD_KEY environment variable
  // or in .cypress.env.json (not committed to git)
});

