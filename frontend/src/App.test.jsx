import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
    // Reset fetch mock
    global.fetch = vi.fn()
  })

  describe('Initial Render', () => {
    it('renders the Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toHaveTextContent('Hello World')
    })

    it('renders the Get Message from Backend button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('renders the name input field', () => {
      render(<App />)
      const input = screen.getByLabelText(/name/i)
      expect(input).toBeInTheDocument()
      expect(input).toHaveAttribute('placeholder', 'Enter your name')
    })

    it('renders the Greet Me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toBeInTheDocument()
    })

    it('does not show any messages initially', () => {
      render(<App />)
      expect(screen.queryByText(/hello world from backend/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/welcome to our purple-themed app/i)).not.toBeInTheDocument()
    })
  })

  describe('Get Message from Backend Feature', () => {
    it('fetches and displays message from backend on button click', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.123Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /get message from backend/i })

      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
      })

      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    })

    it('shows loading state while fetching message', async () => {
      global.fetch.mockImplementationOnce(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:00.123Z' })
        }), 100))
      )

      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /get message from backend/i })

      await user.click(button)

      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()
    })

    it('displays error message when fetch fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /get message from backend/i })

      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/cannot connect to backend/i)).toBeInTheDocument()
      })
    })

    it('displays error when backend returns non-ok response', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /get message from backend/i })

      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/cannot connect to backend/i)).toBeInTheDocument()
      })
    })
  })

  describe('Greet Me Feature', () => {
    it('allows user to enter a name', async () => {
      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)

      await user.type(input, 'Alice')

      expect(input).toHaveValue('Alice')
    })

    it('sends greet request with valid name', async () => {
      const mockResponse = {
        greeting: 'Hello, Alice! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Alice')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, alice! welcome to our purple-themed app!/i)).toBeInTheDocument()
      })

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/greet',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: 'Alice' })
        })
      )
    })

    it('shows client-side validation error for empty name', async () => {
      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.click(button)

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('shows client-side validation error for whitespace-only name', async () => {
      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, '   ')
      await user.click(button)

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('shows loading state while greeting', async () => {
      global.fetch.mockImplementationOnce(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Test! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T10:30:00.123456Z'
          })
        }), 100))
      )

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(button)

      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()
      expect(input).toBeDisabled()
    })

    it('handles server validation error (400 response)', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Name cannot be empty' })
      })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/name cannot be empty/i)).toBeInTheDocument()
      })
    })

    it('handles network error when greeting', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
      })
    })

    it('clears previous greeting when submitting new request', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            greeting: 'Hello, Alice! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T10:30:00.123456Z'
          })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            greeting: 'Hello, Bob! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T10:31:00.123456Z'
          })
        })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      // First greeting
      await user.clear(input)
      await user.type(input, 'Alice')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, alice/i)).toBeInTheDocument()
      })

      // Second greeting
      await user.clear(input)
      await user.type(input, 'Bob')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, bob/i)).toBeInTheDocument()
        expect(screen.queryByText(/hello, alice/i)).not.toBeInTheDocument()
      })
    })

    it('trims whitespace from name before sending', async () => {
      const mockResponse = {
        greeting: 'Hello, Alice! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, '  Alice  ')
      await user.click(button)

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            body: JSON.stringify({ name: 'Alice' })
          })
        )
      })
    })

    it('supports keyboard submission with Enter key', async () => {
      const mockResponse = {
        greeting: 'Hello, Test! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)

      await user.type(input, 'Test{Enter}')

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.any(Object)
        )
      })
    })
  })

  describe('Accessibility', () => {
    it('has accessible label for name input', () => {
      render(<App />)
      const input = screen.getByLabelText(/name/i)
      expect(input).toHaveAttribute('id', 'name-input')
    })

    it('associates error message with input using aria-describedby', async () => {
      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.click(button)

      const input = screen.getByLabelText(/name/i)
      const errorMessage = screen.getByRole('alert')
      expect(input).toHaveAttribute('aria-describedby', 'greet-error')
      expect(errorMessage).toHaveAttribute('id', 'greet-error')
    })

    it('error message has role="alert" for screen readers', async () => {
      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.click(button)

      const errorMessage = screen.getByRole('alert')
      expect(errorMessage).toBeInTheDocument()
    })
  })

  describe('Feature Independence', () => {
    it('both features work independently without interference', async () => {
      // Mock both API calls
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'Hello World from Backend!',
            timestamp: '2024-01-15T10:30:00.123Z'
          })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            greeting: 'Hello, Test! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T10:31:00.123456Z'
          })
        })

      render(<App />)
      const user = userEvent.setup()

      // Test hello message feature
      const helloButton = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(helloButton)

      await waitFor(() => {
        expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
      })

      // Test greeting feature
      const input = screen.getByLabelText(/name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/hello, test! welcome to our purple-themed app!/i)).toBeInTheDocument()
      })

      // Both messages should be visible
      expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
      expect(screen.getByText(/hello, test! welcome to our purple-themed app!/i)).toBeInTheDocument()
    })

    it('greeting error does not affect hello message display', async () => {
      // Mock successful hello, failed greet
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'Hello World from Backend!',
            timestamp: '2024-01-15T10:30:00.123Z'
          })
        })
        .mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()

      // Get hello message
      const helloButton = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(helloButton)

      await waitFor(() => {
        expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
      })

      // Try to greet (will fail)
      const input = screen.getByLabelText(/name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
      })

      // Hello message should still be visible
      expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
    })
  })

  describe('Loading States', () => {
    it('disables both button and input during greeting request', async () => {
      global.fetch.mockImplementationOnce(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({
            greeting: 'Hello, Test! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T10:30:00.123456Z'
          })
        }), 100))
      )

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(button)

      // Check disabled states
      expect(button).toBeDisabled()
      expect(input).toBeDisabled()

      // Wait for completion
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(input).not.toBeDisabled()
      })
    })

    it('re-enables controls after greeting error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
      })

      // Controls should be re-enabled
      expect(button).not.toBeDisabled()
      expect(input).not.toBeDisabled()
    })
  })

  describe('Error State Management', () => {
    it('clears greeting error when user starts typing', async () => {
      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      // Trigger validation error
      await user.click(button)
      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()

      // Start typing
      await user.type(input, 'A')

      // Error should be cleared
      expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
    })

    it('clears previous greeting when new error occurs', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            greeting: 'Hello, Alice! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T10:30:00.123456Z'
          })
        })
        .mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      // Successful greeting
      await user.type(input, 'Alice')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, alice/i)).toBeInTheDocument()
      })

      // Failed greeting
      await user.clear(input)
      await user.type(input, 'Bob')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
      })

      // Previous greeting should be cleared
      expect(screen.queryByText(/hello, alice/i)).not.toBeInTheDocument()
    })

    it('clears error when new successful greeting received', async () => {
      global.fetch
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            greeting: 'Hello, Bob! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T10:31:00.123456Z'
          })
        })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      // Failed greeting
      await user.type(input, 'Alice')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
      })

      // Successful greeting
      await user.clear(input)
      await user.type(input, 'Bob')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, bob/i)).toBeInTheDocument()
      })

      // Error should be cleared
      expect(screen.queryByText(/unable to connect to server/i)).not.toBeInTheDocument()
    })
  })

  describe('Multiple Names', () => {
    it('handles different names correctly', async () => {
      const names = ['Alice', 'Bob', 'Charlie']
      
      for (const name of names) {
        global.fetch.mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            greeting: `Hello, ${name}! Welcome to our purple-themed app!`,
            timestamp: '2024-01-15T10:30:00.123456Z'
          })
        })
      }

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      for (const name of names) {
        await user.clear(input)
        await user.type(input, name)
        await user.click(button)

        await waitFor(() => {
          expect(screen.getByText(new RegExp(`hello, ${name}`, 'i'))).toBeInTheDocument()
        })
      }
    })

    it('handles names with special characters', async () => {
      const mockResponse = {
        greeting: "Hello, José O'Brien! Welcome to our purple-themed app!",
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, "José O'Brien")
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/josé o'brien/i)).toBeInTheDocument()
      })
    })
  })

  describe('Regression Tests - Existing Functionality', () => {
    it('hello message feature still works after greeting feature added', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.123Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /get message from backend/i })

      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
      })

      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
      expect(global.fetch).toHaveBeenCalledTimes(1)
    })

    it('hello message loading state works correctly', async () => {
      global.fetch.mockImplementationOnce(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({
            message: 'Hello World from Backend!',
            timestamp: '2024-01-15T10:30:00.123Z'
          })
        }), 100))
      )

      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /get message from backend/i })

      await user.click(button)

      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()

      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('hello message error handling works correctly', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const button = screen.getByRole('button', { name: /get message from backend/i })

      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/cannot connect to backend/i)).toBeInTheDocument()
      })
    })
  })

  describe('State Management', () => {
    it('maintains separate state for hello and greeting features', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            message: 'Hello World from Backend!',
            timestamp: '2024-01-15T10:30:00.123Z'
          })
        })

      render(<App />)
      const user = userEvent.setup()

      // Get hello message
      const helloButton = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(helloButton)

      await waitFor(() => {
        expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
      })

      // Greeting validation error should not affect hello message
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      await user.click(greetButton)

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
    })
  })

  describe('Input Validation Edge Cases', () => {
    it('validates tab characters as whitespace', async () => {
      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, '\t\t\t')
      await user.click(button)

      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('accepts single character names', async () => {
      const mockResponse = {
        greeting: 'Hello, A! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'A')
      await user.click(button)

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalled()
      })
    })

    it('accepts names with multiple spaces', async () => {
      const mockResponse = {
        greeting: 'Hello, John   Doe! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'John   Doe')
      await user.click(button)

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            body: JSON.stringify({ name: 'John   Doe' })
          })
        )
      })
    })
  })

  describe('Performance', () => {
    it('handles rapid successive greeting requests', async () => {
      render(<App />)
      const user = userEvent.setup()
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })

      // Mock multiple responses
      for (let i = 0; i < 3; i++) {
        global.fetch.mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            greeting: `Hello, Test${i}! Welcome to our purple-themed app!`,
            timestamp: '2024-01-15T10:30:00.123456Z'
          })
        })
      }

      // Rapid clicks
      for (let i = 0; i < 3; i++) {
        await user.clear(input)
        await user.type(input, `Test${i}`)
        await user.click(button)
        
        await waitFor(() => {
          expect(screen.getByText(new RegExp(`test${i}`, 'i'))).toBeInTheDocument()
        })
      }

      // All requests should have been made
      expect(global.fetch).toHaveBeenCalledTimes(3)
    })
  })
})
