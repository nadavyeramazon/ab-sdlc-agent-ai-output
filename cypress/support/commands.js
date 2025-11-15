// Custom Cypress commands for reusable test functionality

// Example: Add custom command to check if backend is healthy
Cypress.Commands.add('checkBackendHealth', () => {
  cy.request('http://localhost:8000/health').then((response) => {
    expect(response.status).to.eq(200)
    expect(response.body).to.have.property('status', 'healthy')
  })
})