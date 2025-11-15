/**
 * End-to-end tests for Green Theme Hello World application.
 * Tests the complete user flow from frontend to backend integration.
 */

describe('Green Theme Hello World Application', () => {
  beforeEach(() => {
    // Visit the application before each test
    cy.visit('http://localhost:3000')
  })

  describe('Static Content', () => {
    it('displays the Hello World heading', () => {
      cy.get('h1').should('contain', 'Hello World')
    })

    it('has green theme styling', () => {
      cy.get('h1').should('have.css', 'color', 'rgb(46, 204, 113)') // #2ecc71
    })

    it('displays the button', () => {
      cy.get('button').should('contain', 'Get Message from Backend')
    })

    it('button has green background', () => {
      cy.get('button').should('have.css', 'background-color', 'rgb(46, 204, 113)')
    })
  })

  describe('Backend Integration', () => {
    it('fetches and displays message from backend', () => {
      // Click the button
      cy.get('button').click()

      // Verify loading state appears in the button
      cy.get('button').should('contain', 'Loading...')

      // Wait for and verify the backend message appears
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')
    })

    it('can fetch message multiple times', () => {
      // First click
      cy.get('button').click()
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')

      // Second click
      cy.get('button').click()
      cy.get('button').should('contain', 'Loading...')
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')
    })

    it('button is disabled during loading', () => {
      cy.get('button').click()
      cy.get('button').should('be.disabled')
    })
  })

  describe('Error Handling', () => {
    it('displays error message when backend is unavailable', () => {
      // Intercept the API call and force it to fail
      cy.intercept('GET', 'http://localhost:8000/api/hello', {
        forceNetworkError: true
      }).as('getHello')

      // Click the button
      cy.get('button').click()

      // Verify loading state appears in the button
      cy.get('button').should('contain', 'Loading...')
      
      // Verify button is disabled during loading
      cy.get('button').should('be.disabled')

      // Wait for the API call to complete
      cy.wait('@getHello')

      // Verify error message appears
      cy.contains('Failed to fetch message from backend', { timeout: 10000 }).should('be.visible')
    })
  })

  describe('Responsive Design', () => {
    it('works on mobile viewport', () => {
      cy.viewport('iphone-x')
      cy.get('h1').should('be.visible')
      cy.get('button').should('be.visible')
    })

    it('works on tablet viewport', () => {
      cy.viewport('ipad-2')
      cy.get('h1').should('be.visible')
      cy.get('button').should('be.visible')
    })

    it('works on desktop viewport', () => {
      cy.viewport(1920, 1080)
      cy.get('h1').should('be.visible')
      cy.get('button').should('be.visible')
    })
  })
})