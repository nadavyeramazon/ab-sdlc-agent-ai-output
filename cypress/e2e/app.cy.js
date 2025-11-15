/**
 * End-to-end tests for Purple Theme Hello World application.
 * Tests the complete user flow from frontend to backend integration.
 * Updated for purple theme and multiple buttons.
 */

describe('Purple Theme Hello World Application', () => {
  beforeEach(() => {
    // Visit the application before each test
    cy.visit('http://localhost:3000')
  })

  describe('Static Content', () => {
    it('displays the Hello World heading', () => {
      cy.get('h1').should('contain', 'Hello World')
    })

    it('has purple theme styling', () => {
      cy.get('h1').should('have.css', 'color', 'rgb(155, 89, 182)') // #9b59b6
    })

    it('displays the Get Message from Backend button', () => {
      cy.get('[data-testid="get-message-button"]').should('be.visible')
      cy.get('[data-testid="get-message-button"]').should('contain', 'Get Message from Backend')
    })

    it('displays the Greet Me button', () => {
      cy.get('[data-testid="greet-button"]').should('be.visible')
      cy.get('[data-testid="greet-button"]').should('contain', 'Greet Me')
    })

    it('button has purple background', () => {
      cy.get('[data-testid="get-message-button"]')
        .should('have.css', 'background-color', 'rgb(155, 89, 182)') // #9b59b6
    })
  })

  describe('Backend Integration', () => {
    it('fetches and displays message from backend', () => {
      // Stub the API call with a mock response
      // This avoids Cypress trying to resolve Docker internal hostnames like 'backend'
      cy.intercept('GET', '**/api/hello', {
        statusCode: 200,
        body: {
          message: 'Hello World from Backend!',
          timestamp: new Date().toISOString()
        },
        delay: 200
      }).as('getHello')

      // Click the specific button using data-testid
      cy.get('[data-testid="get-message-button"]').click()

      // Verify loading state appears in the button
      cy.get('[data-testid="get-message-button"]').should('contain', 'Loading...')
      cy.get('[data-testid="get-message-button"]').should('be.disabled')

      // Wait for the API call to complete
      cy.wait('@getHello')

      // Wait for and verify the backend message appears
      cy.get('[data-testid="backend-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello World from Backend!')
    })

    it('can fetch message multiple times', () => {
      // Stub the API call with a mock response
      cy.intercept('GET', '**/api/hello', {
        statusCode: 200,
        body: {
          message: 'Hello World from Backend!',
          timestamp: new Date().toISOString()
        },
        delay: 200
      }).as('getHello')

      // First click
      cy.get('[data-testid="get-message-button"]').click()
      cy.get('[data-testid="get-message-button"]').should('contain', 'Loading...')
      cy.wait('@getHello')
      cy.get('[data-testid="backend-message"]', { timeout: 10000 }).should('be.visible')

      // Second click
      cy.get('[data-testid="get-message-button"]').click()
      cy.get('[data-testid="get-message-button"]').should('contain', 'Loading...')
      cy.wait('@getHello')
      cy.get('[data-testid="backend-message"]', { timeout: 10000 }).should('be.visible')
    })

    it('button is disabled during loading', () => {
      // Stub the API call with a mock response
      cy.intercept('GET', '**/api/hello', {
        statusCode: 200,
        body: {
          message: 'Hello World from Backend!',
          timestamp: new Date().toISOString()
        },
        delay: 200
      }).as('getHello')

      cy.get('[data-testid="get-message-button"]').click()
      cy.get('[data-testid="get-message-button"]').should('be.disabled')
      
      // Wait for API call to complete
      cy.wait('@getHello')
    })
  })

  describe('Error Handling', () => {
    it('displays error message when backend is unavailable', () => {
      // Stub the API call to return an error
      cy.intercept('GET', '**/api/hello', {
        statusCode: 500,
        body: { error: 'Internal Server Error' },
        delay: 500
      }).as('getHello')

      // Click the specific button
      cy.get('[data-testid="get-message-button"]').click()

      // Verify loading state appears - button should show Loading... text
      cy.get('[data-testid="get-message-button"]').should('contain', 'Loading...')
      cy.get('[data-testid="get-message-button"]').should('be.disabled')
      
      // Wait for the API call to complete
      cy.wait('@getHello')

      // Verify error message appears
      cy.get('[data-testid="backend-error"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Failed to fetch message from backend')
      
      // Verify button is enabled again after error
      cy.get('[data-testid="get-message-button"]').should('not.be.disabled')
    })
  })

  describe('Responsive Design', () => {
    it('works on mobile viewport', () => {
      cy.viewport('iphone-x')
      cy.get('h1').should('be.visible')
      cy.get('[data-testid="get-message-button"]').should('be.visible')
      cy.get('[data-testid="greet-button"]').should('be.visible')
    })

    it('works on tablet viewport', () => {
      cy.viewport('ipad-2')
      cy.get('h1').should('be.visible')
      cy.get('[data-testid="get-message-button"]').should('be.visible')
      cy.get('[data-testid="greet-button"]').should('be.visible')
    })

    it('works on desktop viewport', () => {
      cy.viewport(1920, 1080)
      cy.get('h1').should('be.visible')
      cy.get('[data-testid="get-message-button"]').should('be.visible')
      cy.get('[data-testid="greet-button"]').should('be.visible')
    })
  })
})
