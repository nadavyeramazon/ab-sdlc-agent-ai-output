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
      cy.contains('button', 'Get Message from Backend').should('be.visible')
    })
  })

  describe('Existing Feature - Get Message from Backend', () => {
    it('should fetch and display message when button is clicked', () => {
      // Click the button
      cy.contains('button', 'Get Message from Backend').click()

      // Wait for loading state
      cy.contains('button', 'Loading...').should('be.visible')

      // Wait for and verify message appears
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')
    })

    it('should show loading state during API call', () => {
      cy.contains('button', 'Get Message from Backend').click()
      cy.contains('button', 'Loading...').should('be.visible')
      cy.contains('button', 'Loading...').should('be.disabled')
    })

    it('should make correct API call to backend', () => {
      cy.intercept('GET', '**/api/hello').as('getHello')
      
      cy.contains('button', 'Get Message from Backend').click()
      
      cy.wait('@getHello').then((interception) => {
        expect(interception.response.statusCode).to.eq(200)
        expect(interception.response.body).to.have.property('message')
        expect(interception.response.body).to.have.property('timestamp')
      })
    })

    it('should display message with purple theme styling', () => {
      cy.contains('button', 'Get Message from Backend').click()
      cy.contains('Hello World from Backend!', { timeout: 10000 })
        .should('be.visible')
        .parent()
        .should('have.class', 'message')
    })
  })

  describe('New Feature - Personalized Greeting', () => {
    it('should display name input field', () => {
      cy.get('input[placeholder="Enter your name"]').should('be.visible')
    })

    it('should display Greet Me button', () => {
      cy.contains('button', 'Greet Me').should('be.visible')
    })

    it('should have accessible input label', () => {
      cy.get('input[aria-label="Enter your name"]').should('exist')
    })

    it('should fetch and display personalized greeting', () => {
      // Type name in input
      cy.get('input[placeholder="Enter your name"]').type('John')

      // Click Greet Me button
      cy.contains('button', 'Greet Me').click()

      // Wait for loading state
      cy.contains('button', 'Loading...').should('be.visible')

      // Verify personalized greeting appears
      cy.contains('Hello, John! Welcome to our purple-themed app!', { timeout: 10000 })
        .should('be.visible')
    })

    it('should make correct API call for greeting', () => {
      cy.intercept('POST', '**/api/greet').as('postGreet')
      
      cy.get('input[placeholder="Enter your name"]').type('Jane')
      cy.contains('button', 'Greet Me').click()
      
      cy.wait('@postGreet').then((interception) => {
        expect(interception.request.body).to.deep.equal({ name: 'Jane' })
        expect(interception.response.statusCode).to.eq(200)
        expect(interception.response.body).to.have.property('greeting')
        expect(interception.response.body).to.have.property('timestamp')
      })
    })

    it('should display greeting with purple gradient styling', () => {
      cy.get('input[placeholder="Enter your name"]').type('Test')
      cy.contains('button', 'Greet Me').click()
      
      cy.contains('Hello, Test! Welcome to our purple-themed app!', { timeout: 10000 })
        .should('be.visible')
        .parent()
        .should('have.class', 'greeting')
    })

    it('should allow submission with Enter key', () => {
      cy.get('input[placeholder="Enter your name"]').type('Bob{enter}')
      
      cy.contains('Hello, Bob! Welcome to our purple-themed app!', { timeout: 10000 })
        .should('be.visible')
    })
  })

  describe('Input Validation', () => {
    it('should show validation error for empty name', () => {
      // Click button without entering name
      cy.contains('button', 'Greet Me').click()

      // Verify validation error appears
      cy.contains('Please enter your name').should('be.visible')
    })

    it('should show validation error for whitespace-only name', () => {
      // Enter only spaces
      cy.get('input[placeholder="Enter your name"]').type('     ')
      cy.contains('button', 'Greet Me').click()

      // Verify validation error appears
      cy.contains('Please enter your name').should('be.visible')
    })

    it('should clear validation error when user starts typing', () => {
      // Trigger validation error
      cy.contains('button', 'Greet Me').click()
      cy.contains('Please enter your name').should('be.visible')

      // Start typing
      cy.get('input[placeholder="Enter your name"]').type('A')

      // Validation error should be cleared
      cy.contains('Please enter your name').should('not.exist')
    })

    it('should trim whitespace from name', () => {
      cy.intercept('POST', '**/api/greet').as('postGreet')
      
      // Enter name with surrounding whitespace
      cy.get('input[placeholder="Enter your name"]').type('  Alice  ')
      cy.contains('button', 'Greet Me').click()
      
      // Verify trimmed name is sent
      cy.wait('@postGreet').then((interception) => {
        expect(interception.request.body).to.deep.equal({ name: 'Alice' })
      })
    })

    it('should not make API call when validation fails', () => {
      cy.intercept('POST', '**/api/greet').as('postGreet')
      
      // Try to submit empty name
      cy.contains('button', 'Greet Me').click()
      
      // Wait a moment to ensure no API call is made
      cy.wait(500)
      
      // Verify no API call was made
      cy.get('@postGreet.all').should('have.length', 0)
    })
  })

  describe('Concurrent Feature Usage', () => {
    it('should allow using both features independently', () => {
      // Use existing feature first
      cy.contains('button', 'Get Message from Backend').click()
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')

      // Use new feature
      cy.get('input[placeholder="Enter your name"]').type('Charlie')
      cy.contains('button', 'Greet Me').click()
      cy.contains('Hello, Charlie! Welcome to our purple-themed app!', { timeout: 10000 })
        .should('be.visible')

      // Both messages should still be visible
      cy.contains('Hello World from Backend!').should('be.visible')
      cy.contains('Hello, Charlie! Welcome to our purple-themed app!').should('be.visible')
    })

    it('should allow using features in reverse order', () => {
      // Use new feature first
      cy.get('input[placeholder="Enter your name"]').type('Diana')
      cy.contains('button', 'Greet Me').click()
      cy.contains('Hello, Diana! Welcome to our purple-themed app!', { timeout: 10000 })
        .should('be.visible')

      // Use existing feature
      cy.contains('button', 'Get Message from Backend').click()
      cy.contains('Hello World from Backend!', { timeout: 10000 }).should('be.visible')

      // Both messages should be visible
      cy.contains('Hello, Diana! Welcome to our purple-themed app!').should('be.visible')
      cy.contains('Hello World from Backend!').should('be.visible')
    })

    it('should handle multiple greeting submissions', () => {
      // First greeting
      cy.get('input[placeholder="Enter your name"]').type('Eve')
      cy.contains('button', 'Greet Me').click()
      cy.contains('Hello, Eve! Welcome to our purple-themed app!', { timeout: 10000 })
        .should('be.visible')

      // Clear input and enter new name
      cy.get('input[placeholder="Enter your name"]').clear().type('Frank')
      cy.contains('button', 'Greet Me').click()
      cy.contains('Hello, Frank! Welcome to our purple-themed app!', { timeout: 10000 })
        .should('be.visible')
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
      cy.contains('button', 'Get Message from Backend').should('be.visible')
      cy.get('input[placeholder="Enter your name"]').should('be.visible')
      cy.contains('button', 'Greet Me').should('be.visible')
    })

    it('should be responsive on tablet viewport', () => {
      cy.viewport('ipad-2')
      
      cy.contains('h1', 'Hello World').should('be.visible')
      cy.contains('button', 'Get Message from Backend').should('be.visible')
      cy.get('input[placeholder="Enter your name"]').should('be.visible')
      cy.contains('button', 'Greet Me').should('be.visible')
    })
  })
})
