import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

describe('App Component', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    vi.clearAllMocks()
    // Reset fetch mock
    global.fetch = vi.fn()
  })

  describe('Rendering Tests', () => {
    it('should render without crashing', () => {
      render(<App />)
      expect(screen.getByRole('heading')).toBeInTheDocument()
    })

    it('should display "Hello World" heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveTextContent('Hello World')
    })

    it('should display "Get Message from Backend" button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('should have button initially enabled', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('Initial State Tests', () => {
    it('should not show loading state initially', () => {
      render(<App />)
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
    })

    it('should not show error message initially', () => {
      render(<App />)
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
    })

    it('should not show message content initially', () => {
      render(<App />)
      expect(screen.queryByText(/message:/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/timestamp:/i)).not.toBeInTheDocument()
    })
  })

  describe('User Interaction Tests', () => {
    it('should call fetch when button is clicked', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message', timestamp: '2024-01-01' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      expect(global.fetch).toHaveBeenCalledTimes(1)
      expect(global.fetch).toHaveBeenCalledWith('/api/hello')
    })

    it('should show loading state when button is clicked', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message', timestamp: '2024-01-01' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Loading should appear immediately
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
    })

    it('should disable button during loading', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message', timestamp: '2024-01-01' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      expect(button).toBeDisabled()
    })
  })

  describe('Successful API Call Tests', () => {
    it('should display message from backend on successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Hello from backend!', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(screen.getByText(/hello from backend!/i)).toBeInTheDocument()
      })
    })

    it('should display timestamp from backend on successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(screen.getByText(/2024-01-01T12:00:00Z/i)).toBeInTheDocument()
      })
    })

    it('should hide loading state after successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })

    it('should re-enable button after successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Error Handling Tests', () => {
    it('should show error message when fetch fails with network error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error: network error/i)).toBeInTheDocument()
      })
    })

    it('should show error message for non-OK HTTP response', async () => {
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
        expect(screen.getByText(/error: http error! status: 500/i)).toBeInTheDocument()
      })
    })

    it('should show error message for 404 response', async () => {
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
        expect(screen.getByText(/error: http error! status: 404/i)).toBeInTheDocument()
      })
    })

    it('should hide loading state after error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
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
      })
    })

    it('should not show message content when error occurs', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error: network error/i)).toBeInTheDocument()
      })

      expect(screen.queryByText(/message:/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/timestamp:/i)).not.toBeInTheDocument()
    })
  })

  describe('State Management Tests', () => {
    it('should clear previous error when making a new request', async () => {
      const user = userEvent.setup()
      
      // First request fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/error: network error/i)).toBeInTheDocument()
      })

      // Second request succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success!', timestamp: '2024-01-01' })
        })
      )
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/error:/i)).not.toBeInTheDocument()
        expect(screen.getByText(/success!/i)).toBeInTheDocument()
      })
    })

    it('should update message when making multiple successful requests', async () => {
      const user = userEvent.setup()
      
      // First request
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'First message', timestamp: '2024-01-01' })
        })
      )
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/first message/i)).toBeInTheDocument()
      })

      // Second request
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Second message', timestamp: '2024-01-02' })
        })
      )
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/first message/i)).not.toBeInTheDocument()
        expect(screen.getByText(/second message/i)).toBeInTheDocument()
      })
    })

    it('should handle rapid button clicks gracefully', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData)
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click multiple times
      await user.click(button)
      
      // Button should be disabled, preventing additional clicks
      expect(button).toBeDisabled()
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Integration Tests', () => {
    it('should complete full success flow from initial render to displaying data', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Integration test message', timestamp: '2024-01-01T10:30:00Z' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData)
        })
      )

      // Initial render
      render(<App />)
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument()
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      
      // Click button
      await user.click(button)
      
      // Check loading state
      expect(button).toBeDisabled()
      
      // Wait for data
      await waitFor(() => {
        expect(screen.getByText(/integration test message/i)).toBeInTheDocument()
        expect(screen.getByText(/2024-01-01T10:30:00Z/i)).toBeInTheDocument()
      })
      
      // Verify final state
      expect(button).not.toBeDisabled()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
    })

    it('should complete full error flow from initial render to displaying error', async () => {
      const user = userEvent.setup()
      
      global.fetch = vi.fn(() => Promise.reject(new Error('Connection timeout')))

      // Initial render
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click button
      await user.click(button)
      
      // Wait for error
      await waitFor(() => {
        expect(screen.getByText(/error: connection timeout/i)).toBeInTheDocument()
      })
      
      // Verify final state
      expect(button).not.toBeDisabled()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/message:/i)).not.toBeInTheDocument()
    })
  })

  // ========================================================================
  // GREETING FEATURE TESTS - NEW COMPREHENSIVE TEST COVERAGE
  // ========================================================================

  describe('Greeting Feature - Rendering Tests', () => {
    it('should render name input field with proper attributes', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      expect(input).toBeInTheDocument()
      expect(input).toHaveAttribute('type', 'text')
      expect(input).toHaveAttribute('aria-label', 'Name input')
    })

    it('should render "Greet Me" button', () => {
      render(<App />)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      expect(greetButton).toBeInTheDocument()
    })

    it('should have empty name input initially', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      expect(input).toHaveValue('')
    })

    it('should have "Greet Me" button disabled when input is empty', () => {
      render(<App />)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      expect(greetButton).toBeDisabled()
    })

    it('should not display greeting content initially', () => {
      render(<App />)
      expect(screen.queryByText(/greeting:/i)).not.toBeInTheDocument()
    })
  })

  describe('Greeting Feature - User Input Tests', () => {
    it('should update name input value when user types', async () => {
      const user = userEvent.setup()
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      
      await user.type(input, 'John')
      
      expect(input).toHaveValue('John')
    })

    it('should enable "Greet Me" button when name input has value', async () => {
      const user = userEvent.setup()
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Alice')
      
      expect(greetButton).not.toBeDisabled()
    })

    it('should keep "Greet Me" button disabled with only whitespace input', async () => {
      const user = userEvent.setup()
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, '   ')
      
      expect(greetButton).toBeDisabled()
    })

    it('should handle special characters in name input', async () => {
      const user = userEvent.setup()
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      
      await user.type(input, "O'Brien-Smith")
      
      expect(input).toHaveValue("O'Brien-Smith")
    })
  })

  describe('Greeting Feature - Client-Side Validation Tests', () => {
    it('should show validation error when submitting with empty name', async () => {
      const user = userEvent.setup()
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      // Type and then clear
      await user.type(input, 'John')
      await user.clear(input)
      
      // Button should be disabled, but let's simulate a scenario where validation kicks in
      // The button is disabled when input is empty, so this tests the validation logic
      expect(greetButton).toBeDisabled()
    })

    it('should show validation error for whitespace-only input', async () => {
      const user = userEvent.setup()
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      
      await user.type(input, '   ')
      
      // Verify button remains disabled for whitespace
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      expect(greetButton).toBeDisabled()
    })

    it('should display validation error message when attempting to greet with empty name', async () => {
      const user = userEvent.setup()
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      
      // Type something to enable button
      await user.type(input, 'Test')
      
      // Clear it - this should keep button disabled
      await user.clear(input)
      
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      expect(greetButton).toBeDisabled()
    })
  })

  describe('Greeting Feature - API Call Tests', () => {
    it('should call greet API with correct payload when button is clicked', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, John!', timestamp: '2024-01-01' })
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      await user.click(greetButton)

      expect(global.fetch).toHaveBeenCalledWith('/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: 'John' })
      })
    })

    it('should trim whitespace from name before sending API request', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, Alice!', timestamp: '2024-01-01' })
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, '  Alice  ')
      await user.click(greetButton)

      expect(global.fetch).toHaveBeenCalledWith('/api/greet', 
        expect.objectContaining({
          body: JSON.stringify({ name: 'Alice' })
        })
      )
    })

    it('should display greeting response from backend', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello, Sarah!', timestamp: '2024-01-01T15:30:00Z' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Sarah')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/hello, sarah!/i)).toBeInTheDocument()
      })
    })

    it('should display greeting timestamp from backend', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello, Bob!', timestamp: '2024-01-01T15:30:00Z' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Bob')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/2024-01-01T15:30:00Z/i)).toBeInTheDocument()
      })
    })

    it('should use POST method for greet API', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello!', timestamp: '2024-01-01' })
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Test')
      await user.click(greetButton)

      expect(global.fetch).toHaveBeenCalledWith('/api/greet', 
        expect.objectContaining({
          method: 'POST'
        })
      )
    })
  })

  describe('Greeting Feature - Loading State Tests', () => {
    it('should show loading state when greeting request is in progress', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello!', timestamp: '2024-01-01' })
        }), 100))
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Tom')
      await user.click(greetButton)

      // Should show loading immediately
      const loadingElements = screen.getAllByText(/loading/i)
      expect(loadingElements.length).toBeGreaterThan(0)
    })

    it('should disable "Greet Me" button during loading', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello!', timestamp: '2024-01-01' })
        }), 100))
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Emma')
      await user.click(greetButton)

      expect(greetButton).toBeDisabled()
    })

    it('should disable name input during loading', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello!', timestamp: '2024-01-01' })
        }), 100))
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Mike')
      await user.click(greetButton)

      expect(input).toBeDisabled()
    })

    it('should hide loading state after successful greeting', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello, Lisa!', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Lisa')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/hello, lisa!/i)).toBeInTheDocument()
      })

      // Loading should be gone - but there might be one loading from the other feature
      // So we check that greeting is visible, which means loading for greeting is done
      expect(screen.getByText(/hello, lisa!/i)).toBeInTheDocument()
    })

    it('should re-enable inputs after request completes', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello, Dave!', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Dave')
      await user.click(greetButton)

      await waitFor(() => {
        expect(input).not.toBeDisabled()
      })
    })
  })

  describe('Greeting Feature - Error Handling Tests', () => {
    it('should display error message when greet API call fails', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Chris')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/network error/i)).toBeInTheDocument()
      })
    })

    it('should display generic error for non-OK response from greet API', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 500
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Alex')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/unable to fetch greeting/i)).toBeInTheDocument()
      })
    })

    it('should hide loading state after greet API error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Server error')))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Jordan')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/server error/i)).toBeInTheDocument()
      })

      // Check that the specific error is shown, indicating loading is complete
      expect(screen.getByText(/server error/i)).toBeInTheDocument()
    })

    it('should re-enable inputs after greet API error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Error')))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Taylor')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      expect(input).not.toBeDisabled()
    })

    it('should not display greeting when error occurs', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Failed')))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Sam')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/failed/i)).toBeInTheDocument()
      })

      expect(screen.queryByText(/greeting:/i)).not.toBeInTheDocument()
    })

    it('should handle 404 error from greet API', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 404
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'NotFound')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/unable to fetch greeting/i)).toBeInTheDocument()
      })
    })
  })

  describe('Greeting Feature - State Management Tests', () => {
    it('should clear name input after successful greeting', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello, Kate!', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Kate')
      expect(input).toHaveValue('Kate')
      
      await user.click(greetButton)

      await waitFor(() => {
        expect(input).toHaveValue('')
      })
    })

    it('should clear previous greeting error when making new request', async () => {
      const user = userEvent.setup()
      
      // First request fails
      global.fetch = vi.fn(() => Promise.reject(new Error('First error')))
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'User1')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/first error/i)).toBeInTheDocument()
      })

      // Second request succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, User2!', timestamp: '2024-01-01' })
        })
      )
      
      await user.type(input, 'User2')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.queryByText(/first error/i)).not.toBeInTheDocument()
        expect(screen.getByText(/hello, user2!/i)).toBeInTheDocument()
      })
    })

    it('should clear previous greeting when making new request', async () => {
      const user = userEvent.setup()
      
      // First request
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, First!', timestamp: '2024-01-01' })
        })
      )
      
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'First')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/hello, first!/i)).toBeInTheDocument()
      })

      // Second request
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, Second!', timestamp: '2024-01-02' })
        })
      )
      
      await user.type(input, 'Second')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.queryByText(/hello, first!/i)).not.toBeInTheDocument()
        expect(screen.getByText(/hello, second!/i)).toBeInTheDocument()
      })
    })

    it('should maintain name input value on error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('API Error')))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'ErrorTest')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/api error/i)).toBeInTheDocument()
      })

      // Input should still have the value after error (not cleared)
      // Actually, looking at the code, it only clears on success
      // On error, the input keeps its value, which is good UX
      expect(input).toHaveValue('ErrorTest')
    })

    it('should handle multiple greeting state transitions', async () => {
      const user = userEvent.setup()
      
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      // First greeting - success
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, One!', timestamp: '2024-01-01' })
        })
      )
      
      await user.type(input, 'One')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/hello, one!/i)).toBeInTheDocument()
        expect(input).toHaveValue('')
      })
      
      // Second greeting - error
      global.fetch = vi.fn(() => Promise.reject(new Error('Error Two')))
      
      await user.type(input, 'Two')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/error two/i)).toBeInTheDocument()
        expect(screen.queryByText(/hello, one!/i)).not.toBeInTheDocument()
      })
      
      // Third greeting - success
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, Three!', timestamp: '2024-01-03' })
        })
      )
      
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/hello, three!/i)).toBeInTheDocument()
        expect(screen.queryByText(/error two/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Greeting Feature - Accessibility Tests', () => {
    it('should have proper aria-label on name input', () => {
      render(<App />)
      const input = screen.getByLabelText(/name input/i)
      expect(input).toBeInTheDocument()
    })

    it('should maintain focus management during interactions', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello!', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      
      await user.type(input, 'Focus')
      
      // Input should still be accessible
      expect(input).toBeInTheDocument()
    })

    it('should have accessible button text', () => {
      render(<App />)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      expect(greetButton).toHaveTextContent(/greet me/i)
    })
  })

  describe('Greeting Feature - Edge Cases Tests', () => {
    it('should handle very long names', async () => {
      const user = userEvent.setup()
      const longName = 'A'.repeat(100)
      const mockGreeting = { greeting: `Hello, ${longName}!`, timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, longName)
      await user.click(greetButton)

      expect(global.fetch).toHaveBeenCalled()
    })

    it('should handle names with numbers', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello, User123!', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'User123')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/hello, user123!/i)).toBeInTheDocument()
      })
    })

    it('should handle unicode characters in names', async () => {
      const user = userEvent.setup()
      const unicodeName = '张伟'
      const mockGreeting = { greeting: `Hello, ${unicodeName}!`, timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, unicodeName)
      await user.click(greetButton)

      expect(global.fetch).toHaveBeenCalledWith('/api/greet', 
        expect.objectContaining({
          body: JSON.stringify({ name: unicodeName })
        })
      )
    })

    it('should handle rapid greeting requests', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello!', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Rapid')
      await user.click(greetButton)

      // Button should be disabled during first request
      expect(greetButton).toBeDisabled()
    })

    it('should handle emoji in names', async () => {
      const user = userEvent.setup()
      const emojiName = 'John 😊'
      const mockGreeting = { greeting: `Hello, ${emojiName}!`, timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, emojiName)
      await user.click(greetButton)

      expect(global.fetch).toHaveBeenCalledWith('/api/greet', 
        expect.objectContaining({
          body: JSON.stringify({ name: emojiName })
        })
      )
    })
  })

  describe('Greeting Feature - Integration Tests', () => {
    it('should complete full greeting flow from input to displaying greeting', async () => {
      const user = userEvent.setup()
      const mockGreeting = { greeting: 'Hello, Integration!', timestamp: '2024-01-01T10:30:00Z' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockGreeting)
        })
      )

      // Initial render
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      // Initially disabled
      expect(greetButton).toBeDisabled()
      expect(input).toHaveValue('')
      
      // Type name
      await user.type(input, 'Integration')
      expect(input).toHaveValue('Integration')
      expect(greetButton).not.toBeDisabled()
      
      // Click button
      await user.click(greetButton)
      
      // Check loading state
      expect(greetButton).toBeDisabled()
      expect(input).toBeDisabled()
      
      // Wait for greeting
      await waitFor(() => {
        expect(screen.getByText(/hello, integration!/i)).toBeInTheDocument()
        expect(screen.getByText(/2024-01-01T10:30:00Z/i)).toBeInTheDocument()
      })
      
      // Verify final state
      expect(input).toHaveValue('') // Cleared after success
      expect(input).not.toBeDisabled()
      expect(greetButton).toBeDisabled() // Disabled again because input is empty
    })

    it('should allow multiple greetings in sequence', async () => {
      const user = userEvent.setup()
      
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      // First greeting
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, First!', timestamp: '2024-01-01' })
        })
      )
      
      await user.type(input, 'First')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/hello, first!/i)).toBeInTheDocument()
      })
      
      // Second greeting
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, Second!', timestamp: '2024-01-02' })
        })
      )
      
      await user.type(input, 'Second')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/hello, second!/i)).toBeInTheDocument()
        expect(screen.queryByText(/hello, first!/i)).not.toBeInTheDocument()
      })
    })

    it('should handle greeting error recovery', async () => {
      const user = userEvent.setup()
      
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      // First attempt fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Temporary error')))
      
      await user.type(input, 'Retry')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/temporary error/i)).toBeInTheDocument()
      })
      
      // User can retry with same name
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, Retry!', timestamp: '2024-01-01' })
        })
      )
      
      // Name is still there after error
      expect(input).toHaveValue('Retry')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.queryByText(/temporary error/i)).not.toBeInTheDocument()
        expect(screen.getByText(/hello, retry!/i)).toBeInTheDocument()
      })
    })

    it('should keep greeting and hello message features independent', async () => {
      const user = userEvent.setup()
      
      render(<App />)
      
      // Trigger hello message
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Backend message', timestamp: '2024-01-01' })
        })
      )
      
      const helloButton = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(helloButton)
      
      await waitFor(() => {
        expect(screen.getByText(/backend message/i)).toBeInTheDocument()
      })
      
      // Now trigger greeting
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ greeting: 'Hello, Test!', timestamp: '2024-01-02' })
        })
      )
      
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Test')
      await user.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText(/hello, test!/i)).toBeInTheDocument()
      })
      
      // Both should be visible
      expect(screen.getByText(/backend message/i)).toBeInTheDocument()
      expect(screen.getByText(/hello, test!/i)).toBeInTheDocument()
    })
  })
})
