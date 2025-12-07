// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands';

// Alternatively you can use CommonJS syntax:
// require('./commands')

// Handle uncaught exceptions
Cypress.on('uncaught:exception', (err, runnable) => {
  // Ignore ResizeObserver errors (common in React apps)
  if (err.message.includes('ResizeObserver loop limit exceeded')) {
    return false;
  }
  // Ignore network errors that might occur during page load
  if (err.message.includes('NetworkError') || err.message.includes('Failed to fetch')) {
    return false;
  }
  // Ignore React hydration warnings
  if (err.message.includes('Hydration') || err.message.includes('hydration')) {
    return false;
  }
  // Ignore ChunkLoadError (webpack chunk loading errors)
  if (err.message.includes('ChunkLoadError') || err.message.includes('Loading chunk')) {
    return false;
  }
  // For other errors, let Cypress handle them
  return true;
});

// Add global error handler for better debugging
Cypress.on('fail', (error, runnable) => {
  // Log the error for debugging
  console.error('Test failed:', error.message);
  throw error;
});

