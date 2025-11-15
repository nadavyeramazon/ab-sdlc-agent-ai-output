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
      // Intercept the API call and add a small delay to make loading state observable
      cy.intercept('GET', 'http://localhost:8000/api/hello', (req) => {
        req.continue((res) => {
          // Add delay to ensure loading state is visible
          res.delay = 200
        })
      }).as('getHello')

      // Click the button
      cy.get('button').click()

      // Verify loading state appears in the button
      cy.get('button').should('contain', 'Loading...')

      // Wait for the API call to complete
      cy.wait('@getHello')

      // Wait for and verify the backend message appears
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')
    })

    it('can fetch message multiple times', () => {
      // Intercept the API call and add a small delay to make loading state observable
      cy.intercept('GET', 'http://localhost:8000/api/hello', (req) => {
        req.continue((res) => {
          res.delay = 200
        })
      }).as('getHello')

      // First click
      cy.get('button').click()
      cy.get('button').should('contain', 'Loading...')
      cy.wait('@getHello')
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')

      // Second click
      cy.get('button').click()
      cy.get('button').should('contain', 'Loading...')
      cy.wait('@getHello')
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')
    })

    it('button is disabled during loading', () => {
      // Intercept the API call and add a small delay to make loading state observable
      cy.intercept('GET', 'http://localhost:8000/api/hello', (req) => {
        req.continue((res) => {
          res.delay = 200
        })
      }).as('getHello')

      cy.get('button').click()
      cy.get('button').should('be.disabled')
      
      // Wait for API call to complete
      cy.wait('@getHello')
    })
  })

  describe('Error Handling', () => {
    it('displays error message when backend is unavailable', () => {
      // Intercept the API call and force it to fail with a delay
      // The delay ensures we can observe the loading state before the error occurs
      cy.intercept('GET', 'http://localhost:8000/api/hello', {
        statusCode: 500,
        body: { error: 'Internal Server Error' },
        delay: 100 // Add a small delay to make loading state observable
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