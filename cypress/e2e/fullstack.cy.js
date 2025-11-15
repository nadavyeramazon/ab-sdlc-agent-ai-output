/**
 * Comprehensive E2E tests for Purple Theme Hello World fullstack application.
 * 
 * Tests:
 * - Frontend accessibility
 * - Backend API integration
 * - Purple theme verification
 * - Existing "Get Message from Backend" feature
 * - New personalized greeting feature
 * - Input validation
 * - Error handling
 * - Concurrent feature usage
 */

describe('Purple Theme Hello World Fullstack Application', () => {
  // Setup: Visit the application before each test
  beforeEach(() => {
    cy.visit('http://localhost:3000')
  })

  describe('Static Content and Theme', () => {
    it('should display the Hello World heading', () => {
      cy.contains('h1', 'Hello World').should('be.visible')
    })

    it('should have purple theme colors', () => {
      // Check heading color (purple)
      cy.get('h1').should('have.css', 'color', 'rgb(155, 89, 182)') // #9b59b6
    })

    it('should have purple gradient background', () => {
      cy.get('.app').should('have.css', 'background-image')
        .and('include', 'linear-gradient')
    })

    it('should display Get Message from Backend button', () => {
      cy.get('[data-testid="get-message-button"]').should('be.visible')
      cy.get('[data-testid="get-message-button"]').should('contain', 'Get Message from Backend')
    })
  })

  describe('Existing Feature - Get Message from Backend', () => {
    it('should fetch and display message when button is clicked', () => {
      // Click the button
      cy.get('[data-testid="get-message-button"]').click()

      // Wait for loading state
      cy.get('[data-testid="get-message-button"]').should('contain', 'Loading...')
      cy.get('[data-testid="get-message-button"]').should('be.disabled')

      // Wait for and verify message appears
      cy.get('[data-testid="backend-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello World from Backend!')
    })

    it('should show loading state during API call', () => {
      cy.get('[data-testid="get-message-button"]').click()
      cy.get('[data-testid="get-message-button"]').should('contain', 'Loading...')
      cy.get('[data-testid="get-message-button"]').should('be.disabled')
    })

    it('should make correct API call to backend', () => {
      cy.intercept('GET', '**/api/hello').as('getHello')
      
      cy.get('[data-testid="get-message-button"]').click()
      
      cy.wait('@getHello').then((interception) => {
        expect(interception.response.statusCode).to.eq(200)
        expect(interception.response.body).to.have.property('message')
        expect(interception.response.body).to.have.property('timestamp')
      })
    })

    it('should display message with purple theme styling', () => {
      cy.get('[data-testid="get-message-button"]').click()
      cy.get('[data-testid="backend-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('have.class', 'message')
    })
  })

  describe('New Feature - Personalized Greeting', () => {
    it('should display name input field', () => {
      cy.get('[data-testid="name-input"]').should('be.visible')
      cy.get('[data-testid="name-input"]').should('have.attr', 'placeholder', 'Enter your name')
    })

    it('should display Greet Me button', () => {
      cy.get('[data-testid="greet-button"]').should('be.visible')
      cy.get('[data-testid="greet-button"]').should('contain', 'Greet Me')
    })

    it('should have accessible input label', () => {
      cy.get('[data-testid="name-input"]').should('have.attr', 'aria-label', 'Enter your name')
    })

    it('should fetch and display personalized greeting', () => {
      // Type name in input
      cy.get('[data-testid="name-input"]').type('John')

      // Click Greet Me button
      cy.get('[data-testid="greet-button"]').click()

      // Wait for loading state
      cy.get('[data-testid="greet-button"]').should('contain', 'Loading...')
      cy.get('[data-testid="greet-button"]').should('be.disabled')

      // Verify personalized greeting appears
      cy.get('[data-testid="greeting-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello, John! Welcome to our purple-themed app!')
    })

    it('should make correct API call for greeting', () => {
      cy.intercept('POST', '**/api/greet').as('postGreet')
      
      cy.get('[data-testid="name-input"]').type('Jane')
      cy.get('[data-testid="greet-button"]').click()
      
      cy.wait('@postGreet').then((interception) => {
        expect(interception.request.body).to.deep.equal({ name: 'Jane' })
        expect(interception.response.statusCode).to.eq(200)
        expect(interception.response.body).to.have.property('greeting')
        expect(interception.response.body).to.have.property('timestamp')
      })
    })

    it('should display greeting with purple gradient styling', () => {
      cy.get('[data-testid="name-input"]').type('Test')
      cy.get('[data-testid="greet-button"]').click()
      
      cy.get('[data-testid="greeting-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('have.class', 'greeting')
    })

    it('should allow submission with Enter key', () => {
      cy.get('[data-testid="name-input"]').type('Bob{enter}')
      
      cy.get('[data-testid="greeting-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello, Bob! Welcome to our purple-themed app!')
    })
  })

  describe('Input Validation', () => {
    it('should show validation error for empty name', () => {
      // Click button without entering name
      cy.get('[data-testid="greet-button"]').click()

      // Verify validation error appears
      cy.get('[data-testid="validation-error"]')
        .should('be.visible')
        .and('contain', 'Please enter your name')
    })

    it('should show validation error for whitespace-only name', () => {
      // Enter only spaces
      cy.get('[data-testid="name-input"]').type('     ')
      cy.get('[data-testid="greet-button"]').click()

      // Verify validation error appears
      cy.get('[data-testid="validation-error"]')
        .should('be.visible')
        .and('contain', 'Please enter your name')
    })

    it('should clear validation error when user starts typing', () => {
      // Trigger validation error
      cy.get('[data-testid="greet-button"]').click()
      cy.get('[data-testid="validation-error"]').should('be.visible')

      // Start typing
      cy.get('[data-testid="name-input"]').type('A')

      // Validation error should be cleared
      cy.get('[data-testid="validation-error"]').should('not.exist')
    })

    it('should trim whitespace from name', () => {
      cy.intercept('POST', '**/api/greet').as('postGreet')
      
      // Enter name with surrounding whitespace
      cy.get('[data-testid="name-input"]').type('  Alice  ')
      cy.get('[data-testid="greet-button"]').click()
      
      // Verify trimmed name is sent
      cy.wait('@postGreet').then((interception) => {
        expect(interception.request.body).to.deep.equal({ name: 'Alice' })
      })
    })

    it('should not make API call when validation fails', () => {
      cy.intercept('POST', '**/api/greet').as('postGreet')
      
      // Try to submit empty name
      cy.get('[data-testid="greet-button"]').click()
      
      // Wait a moment to ensure no API call is made
      cy.wait(500)
      
      // Verify no API call was made
      cy.get('@postGreet.all').should('have.length', 0)
    })
  })

  describe('Concurrent Feature Usage', () => {
    it('should allow using both features independently', () => {
      // Use existing feature first
      cy.get('[data-testid="get-message-button"]').click()
      cy.get('[data-testid="backend-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello World from Backend!')

      // Use new feature
      cy.get('[data-testid="name-input"]').type('Charlie')
      cy.get('[data-testid="greet-button"]').click()
      cy.get('[data-testid="greeting-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello, Charlie! Welcome to our purple-themed app!')

      // Both messages should still be visible
      cy.get('[data-testid="backend-message"]').should('be.visible')
      cy.get('[data-testid="greeting-message"]').should('be.visible')
    })

    it('should allow using features in reverse order', () => {
      // Use new feature first
      cy.get('[data-testid="name-input"]').type('Diana')
      cy.get('[data-testid="greet-button"]').click()
      cy.get('[data-testid="greeting-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello, Diana! Welcome to our purple-themed app!')

      // Use existing feature
      cy.get('[data-testid="get-message-button"]').click()
      cy.get('[data-testid="backend-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello World from Backend!')

      // Both messages should be visible
      cy.get('[data-testid="greeting-message"]').should('be.visible')
      cy.get('[data-testid="backend-message"]').should('be.visible')
    })

    it('should handle multiple greeting submissions', () => {
      // First greeting
      cy.get('[data-testid="name-input"]').type('Eve')
      cy.get('[data-testid="greet-button"]').click()
      cy.get('[data-testid="greeting-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello, Eve! Welcome to our purple-themed app!')

      // Clear input and enter new name
      cy.get('[data-testid="name-input"]').clear().type('Frank')
      cy.get('[data-testid="greet-button"]').click()
      cy.get('[data-testid="greeting-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Hello, Frank! Welcome to our purple-themed app!')
    })
  })

  describe('Backend API Health', () => {
    it('should have healthy backend service', () => {
      cy.request('http://localhost:8000/health').then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body).to.have.property('status', 'healthy')
      })
    })

    it('should have functioning /api/hello endpoint', () => {
      cy.request('GET', 'http://localhost:8000/api/hello').then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body).to.have.property('message', 'Hello World from Backend!')
        expect(response.body).to.have.property('timestamp')
      })
    })

    it('should have functioning /api/greet endpoint', () => {
      cy.request('POST', 'http://localhost:8000/api/greet', { name: 'Test' }).then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body).to.have.property('greeting')
        expect(response.body.greeting).to.include('Test')
        expect(response.body.greeting).to.include('purple-themed app')
        expect(response.body).to.have.property('timestamp')
      })
    })
  })

  describe('Responsive Design', () => {
    it('should be responsive on mobile viewport', () => {
      cy.viewport('iphone-x')
      
      cy.contains('h1', 'Hello World').should('be.visible')
      cy.get('[data-testid="get-message-button"]').should('be.visible')
      cy.get('[data-testid="name-input"]').should('be.visible')
      cy.get('[data-testid="greet-button"]').should('be.visible')
    })

    it('should be responsive on tablet viewport', () => {
      cy.viewport('ipad-2')
      
      cy.contains('h1', 'Hello World').should('be.visible')
      cy.get('[data-testid="get-message-button"]').should('be.visible')
      cy.get('[data-testid="name-input"]').should('be.visible')
      cy.get('[data-testid="greet-button"]').should('be.visible')
    })
  })
})
