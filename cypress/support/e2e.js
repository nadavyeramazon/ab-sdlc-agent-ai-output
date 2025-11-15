// Cypress support file for E2E tests
// Add custom commands and global configurations here

// Disable screenshot on failure for faster test execution
Cypress.Screenshot.defaults({
  screenshotOnRunFailure: false,
})

// Increase default timeout for backend calls
Cypress.config('defaultCommandTimeout', 10000)