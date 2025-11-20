import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import App from './App'

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
    // Reset fetch mock
    global.fetch = vi.fn()
  })

  describe('Initial Rendering', () => {
    it('should render the title', () => {
      render(<App />)
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument()
    })

    it('should render the button with correct initial text', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('should not display any message, error, or loading state initially', () => {
      render(<App />)
      expect(screen.queryByText(/backend response:/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
    })
  })

  describe('Button Click Interactions', () => {
    it('should be clickable and trigger fetch on click', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledTimes(1)
      })
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    })

    it('should disable button during loading', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Button should be disabled while loading
      await waitFor(() => {
        expect(button).toBeDisabled()
        expect(button).toHaveTextContent(/loading/i)
      })
    })
  })

  describe('Loading States', () => {
    it('should display loading text in button when API call is in progress', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).toHaveTextContent(/loading/i)
        expect(screen.getAllByText(/loading/i).length).toBeGreaterThan(0)
      })
    })

    it('should display loading paragraph when API call is in progress', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Should show loading paragraph
      await waitFor(() => {
        const loadingParagraphs = screen.getAllByText(/loading/i)
        expect(loadingParagraphs.length).toBeGreaterThanOrEqual(2) // Button + paragraph
      })
    })

    it('should clear loading state after API call completes', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(button).toHaveTextContent(/get message from backend/i)
      })
    })
  })

  describe('Error Handling', () => {
    it('should display error message when fetch fails with network error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: network error/i)).toBeInTheDocument()
      })
    })

    it('should display error message when API returns non-OK status', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 500
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: http error! status: 500/i)).toBeInTheDocument()
      })
    })

    it('should display error message for 404 status', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 404
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: http error! status: 404/i)).toBeInTheDocument()
      })
    })

    it('should clear previous error when new request is made', async () => {
      const user = userEvent.setup()
      // First call fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: network error/i)).toBeInTheDocument()
      })

      // Second call succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success!' })
        })
      )

      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
        expect(screen.getByText(/success!/i)).toBeInTheDocument()
      })
    })

    it('should re-enable button after error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(button).toHaveTextContent(/get message from backend/i)
      })
    })
  })

  describe('Successful API Responses', () => {
    it('should display backend message on successful API call', async () => {
      const user = userEvent.setup()
      const mockMessage = 'Hello from the backend!'
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: mockMessage })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/backend response:/i)).toBeInTheDocument()
        expect(screen.getByText(mockMessage)).toBeInTheDocument()
      })
    })

    it('should handle response with different message content', async () => {
      const user = userEvent.setup()
      const mockMessage = 'Custom server response'
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: mockMessage })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(mockMessage)).toBeInTheDocument()
      })
    })

    it('should stringify JSON data if message field is not present', async () => {
      const user = userEvent.setup()
      const mockData = { status: 'ok', data: 'test' }
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData)
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(JSON.stringify(mockData))).toBeInTheDocument()
      })
    })

    it('should clear previous message when new request is made', async () => {
      const user = userEvent.setup()
      const firstMessage = 'First message'
      const secondMessage = 'Second message'
      
      // First call
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: firstMessage })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(firstMessage)).toBeInTheDocument()
      })

      // Second call
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: secondMessage })
        })
      )

      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(firstMessage)).not.toBeInTheDocument()
        expect(screen.getByText(secondMessage)).toBeInTheDocument()
      })
    })

    it('should display response section only after successful fetch', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      // Initially no response section
      expect(screen.queryByText(/backend response:/i)).not.toBeInTheDocument()
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        })
      )

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)
      
      // After fetch, response section should appear
      await waitFor(() => {
        expect(screen.getByText(/backend response:/i)).toBeInTheDocument()
      })
    })
  })

  describe('State Management', () => {
    it('should clear error and message when starting new request', async () => {
      const user = userEvent.setup()
      
      // First call fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Error')))
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument()
      })

      // Second call succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success' })
        })
      )
      
      await user.click(button)
      
      // During loading, neither error nor old message should be visible
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
      })
    })

    it('should handle multiple rapid clicks gracefully', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Response' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click multiple times
      await user.click(button)
      await user.click(button)
      await user.click(button)
      
      // Should still work correctly
      await waitFor(() => {
        expect(screen.getByText('Response')).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('should have accessible button with proper role', () => {
      render(<App />)
      // Fixed: Specify which button to query by using the button name
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('should have accessible heading with proper role', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveTextContent(/hello world/i)
    })

    it('should properly disable button during loading for accessibility', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test' })
        }), 50))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Button should be disabled and not clickable
      await waitFor(() => {
        expect(button).toBeDisabled()
      })
    })
  })

  describe('Greeting Feature', () => {
    describe('Initial Rendering', () => {
      it('should render greeting section with heading, input field, and button', () => {
        render(<App />)
        
        expect(screen.getByRole('heading', { name: /personalized greeting/i })).toBeInTheDocument()
        expect(screen.getByPlaceholderText(/enter your name/i)).toBeInTheDocument()
        expect(screen.getByRole('button', { name: /greet me/i })).toBeInTheDocument()
      })

      it('should render input field with proper attributes', () => {
        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        expect(input).toHaveAttribute('type', 'text')
        expect(input).toHaveAttribute('maxLength', '100')
        expect(input).toHaveAttribute('aria-label', 'Enter your name')
        expect(input).toHaveValue('')
      })

      it('should render greet button in enabled state initially', () => {
        render(<App />)
        
        const button = screen.getByRole('button', { name: /greet me/i })
        expect(button).toBeInTheDocument()
        expect(button).not.toBeDisabled()
      })

      it('should not display greeting or error messages initially', () => {
        render(<App />)
        
        expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
        expect(screen.queryByText(/hello/i)).not.toBeInTheDocument()
      })
    })

    describe('Input Field Functionality', () => {
      it('should update input value when user types', async () => {
        const user = userEvent.setup()
        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        await user.type(input, 'John')
        
        expect(input).toHaveValue('John')
      })

      it('should handle typing different names', async () => {
        const user = userEvent.setup()
        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        await user.type(input, 'Alice Smith')
        
        expect(input).toHaveValue('Alice Smith')
      })

      it('should enforce maxLength attribute of 100 characters', async () => {
        const user = userEvent.setup()
        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        expect(input).toHaveAttribute('maxLength', '100')
        
        // Verify it's a valid HTML constraint
        const longName = 'A'.repeat(150)
        await user.type(input, longName)
        
        // Browser will enforce maxLength, so value should be truncated to 100
        expect(input.value.length).toBeLessThanOrEqual(100)
      })

      it('should clear input value after successful greeting', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        expect(input).toHaveValue('John')
        
        await user.click(button)
        
        await waitFor(() => {
          expect(input).toHaveValue('')
        })
      })
    })

    describe('Button Click and API Call', () => {
      it('should trigger fetch with POST method when button is clicked with valid name', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(global.fetch).toHaveBeenCalledTimes(1)
        })
        
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: 'John' })
          }
        )
      })

      it('should send trimmed name in API request', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, '  John  ')
        await user.click(button)
        
        await waitFor(() => {
          expect(global.fetch).toHaveBeenCalledWith(
            'http://localhost:8000/api/greet',
            expect.objectContaining({
              body: JSON.stringify({ name: 'John' })
            })
          )
        })
      })

      it('should include correct Content-Type header in request', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Alice!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'Alice')
        await user.click(button)
        
        await waitFor(() => {
          expect(global.fetch).toHaveBeenCalledWith(
            expect.any(String),
            expect.objectContaining({
              headers: {
                'Content-Type': 'application/json',
              }
            })
          )
        })
      })
    })

    describe('Loading State', () => {
      it('should disable button and show loading text during API call', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          new Promise((resolve) => setTimeout(() => resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          }), 100))
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(button).toBeDisabled()
          expect(button).toHaveTextContent(/loading/i)
        })
      })

      it('should re-enable button after API call completes', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(button).not.toBeDisabled()
          expect(button).toHaveTextContent(/greet me/i)
        })
      })

      it('should show loading state for the correct button only', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn((url) => {
          if (url.includes('/api/greet')) {
            return new Promise((resolve) => setTimeout(() => resolve({
              ok: true,
              json: () => Promise.resolve({ greeting: 'Hello, John!' })
            }), 100))
          }
          return Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ message: 'Test' })
          })
        })

        render(<App />)
        
        const greetInput = screen.getByPlaceholderText(/enter your name/i)
        const greetButton = screen.getByRole('button', { name: /greet me/i })
        const fetchButton = screen.getByRole('button', { name: /get message from backend/i })
        
        await user.type(greetInput, 'John')
        await user.click(greetButton)
        
        await waitFor(() => {
          expect(greetButton).toBeDisabled()
          expect(fetchButton).not.toBeDisabled()
        })
      })
    })

    describe('Successful Response Handling', () => {
      it('should display greeting message on successful API response', async () => {
        const user = userEvent.setup()
        const mockGreeting = 'Hello, John! Nice to meet you!'
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: mockGreeting })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(mockGreeting)).toBeInTheDocument()
        })
      })

      it('should display greeting with correct styling class', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Alice!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'Alice')
        await user.click(button)
        
        await waitFor(() => {
          const greetingElement = screen.getByText('Hello, Alice!')
          expect(greetingElement).toHaveClass('success')
        })
      })

      it('should handle different greeting responses', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Greetings, Bob! Welcome!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'Bob')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Greetings, Bob! Welcome!')).toBeInTheDocument()
        })
      })
    })

    describe('Error Handling - Empty Name Validation', () => {
      it('should display error message when name is empty', async () => {
        const user = userEvent.setup()
        render(<App />)
        
        const button = screen.getByRole('button', { name: /greet me/i })
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
        })
      })

      it('should display error message when name contains only whitespace', async () => {
        const user = userEvent.setup()
        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, '   ')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
        })
      })

      it('should not call API when name is empty', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn()
        
        render(<App />)
        
        const button = screen.getByRole('button', { name: /greet me/i })
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
        })
        
        expect(global.fetch).not.toHaveBeenCalled()
      })

      it('should display error with correct styling class', async () => {
        const user = userEvent.setup()
        render(<App />)
        
        const button = screen.getByRole('button', { name: /greet me/i })
        await user.click(button)
        
        await waitFor(() => {
          const errorElement = screen.getByText(/please enter your name/i)
          expect(errorElement).toHaveClass('error')
        })
      })
    })

    describe('Error Handling - Network Errors', () => {
      it('should display error message when network request fails', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() => Promise.reject(new Error('Network failure')))

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/network failure/i)).toBeInTheDocument()
        })
      })

      it('should display generic error when fetch fails without error message', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() => Promise.reject({}))

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/failed to connect to server/i)).toBeInTheDocument()
        })
      })

      it('should re-enable button after network error', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(button).not.toBeDisabled()
          expect(button).toHaveTextContent(/greet me/i)
        })
      })
    })

    describe('Error Handling - API Errors (400 Response)', () => {
      it('should display error message when API returns 400 with detail', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: false,
            status: 400,
            json: () => Promise.resolve({ detail: 'Name is required' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/name is required/i)).toBeInTheDocument()
        })
      })

      it('should display generic error when API returns 400 without detail', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: false,
            status: 400,
            json: () => Promise.resolve({})
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/failed to get greeting/i)).toBeInTheDocument()
        })
      })

      it('should handle 500 server error', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: false,
            status: 500,
            json: () => Promise.resolve({ detail: 'Internal server error' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/internal server error/i)).toBeInTheDocument()
        })
      })
    })

    describe('State Management - Clearing Previous Messages', () => {
      it('should clear previous error when new valid request is made', async () => {
        const user = userEvent.setup()
        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        // First click with empty name to trigger error
        await user.click(button)
        await waitFor(() => {
          expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
        })

        // Second click with valid name
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
          expect(screen.getByText('Hello, John!')).toBeInTheDocument()
        })
      })

      it('should clear previous greeting when new request is made', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        // First successful greeting
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Hello, John!')).toBeInTheDocument()
        })

        // Second greeting with different name
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Alice!' })
          })
        )
        
        await user.type(input, 'Alice')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.queryByText('Hello, John!')).not.toBeInTheDocument()
          expect(screen.getByText('Hello, Alice!')).toBeInTheDocument()
        })
      })

      it('should clear previous API error when new request is made', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        // First request fails
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/network error/i)).toBeInTheDocument()
        })

        // Clear input and type new name
        await user.clear(input)
        await user.type(input, 'Alice')

        // Second request succeeds
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Alice!' })
          })
        )
        
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.queryByText(/network error/i)).not.toBeInTheDocument()
          expect(screen.getByText('Hello, Alice!')).toBeInTheDocument()
        })
      })

      it('should clear both error and greeting at start of new request', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Hello, John!')).toBeInTheDocument()
        })

        // Make new request - during loading, neither should be visible
        await user.type(input, 'Alice')
        
        global.fetch = vi.fn(() =>
          new Promise((resolve) => setTimeout(() => resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Alice!' })
          }), 50))
        )
        
        await user.click(button)
        
        // Check that old greeting is cleared immediately
        expect(screen.queryByText('Hello, John!')).not.toBeInTheDocument()
      })
    })

    describe('Multiple Submissions', () => {
      it('should handle multiple successful submissions in sequence', async () => {
        const user = userEvent.setup()
        
        render(<App />)
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        // First submission
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Hello, John!')).toBeInTheDocument()
          expect(input).toHaveValue('')
        })

        // Second submission
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Alice!' })
          })
        )
        
        await user.type(input, 'Alice')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Hello, Alice!')).toBeInTheDocument()
          expect(input).toHaveValue('')
        })

        // Third submission
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Bob!' })
          })
        )
        
        await user.type(input, 'Bob')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Hello, Bob!')).toBeInTheDocument()
          expect(input).toHaveValue('')
        })
      })

      it('should handle alternating success and error submissions', async () => {
        const user = userEvent.setup()
        
        render(<App />)
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        // Success
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          })
        )
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Hello, John!')).toBeInTheDocument()
        })

        // Error
        global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
        
        await user.type(input, 'Alice')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(/network error/i)).toBeInTheDocument()
        })

        // Success again
        global.fetch = vi.fn(() =>
          Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, Bob!' })
          })
        )
        
        await user.type(input, 'Bob')
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText('Hello, Bob!')).toBeInTheDocument()
          expect(screen.queryByText(/network error/i)).not.toBeInTheDocument()
        })
      })

      it('should not allow submission while request is in progress', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          new Promise((resolve) => setTimeout(() => resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          }), 100))
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        // Button should be disabled
        await waitFor(() => {
          expect(button).toBeDisabled()
        })
        
        // Try to click again while loading
        await user.click(button)
        
        // Should only have called fetch once
        expect(global.fetch).toHaveBeenCalledTimes(1)
      })
    })

    describe('Accessibility', () => {
      it('should have proper aria-label on input field', () => {
        render(<App />)
        
        const input = screen.getByLabelText(/enter your name/i)
        expect(input).toBeInTheDocument()
        expect(input).toHaveAttribute('aria-label', 'Enter your name')
      })

      it('should have accessible heading with proper level', () => {
        render(<App />)
        
        const heading = screen.getByRole('heading', { name: /personalized greeting/i })
        expect(heading).toBeInTheDocument()
        expect(heading.tagName).toBe('H2')
      })

      it('should have accessible button with proper role', () => {
        render(<App />)
        
        const button = screen.getByRole('button', { name: /greet me/i })
        expect(button).toBeInTheDocument()
      })

      it('should properly disable button during loading for keyboard users', async () => {
        const user = userEvent.setup()
        global.fetch = vi.fn(() =>
          new Promise((resolve) => setTimeout(() => resolve({
            ok: true,
            json: () => Promise.resolve({ greeting: 'Hello, John!' })
          }), 100))
        )

        render(<App />)
        
        const input = screen.getByPlaceholderText(/enter your name/i)
        const button = screen.getByRole('button', { name: /greet me/i })
        
        await user.type(input, 'John')
        await user.click(button)
        
        await waitFor(() => {
          expect(button).toBeDisabled()
          expect(button).toHaveAttribute('disabled')
        })
      })
    })
  })
})
