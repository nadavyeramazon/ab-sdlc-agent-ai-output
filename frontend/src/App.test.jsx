import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

// Get API URL from environment variable with fallback (same as App.jsx)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  describe('Initial Render Tests', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
    })

    it('renders Get Message from Backend button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('renders name input field with label', () => {
      render(<App />)
      const label = screen.getByText('Name')
      const input = screen.getByLabelText('Name')
      expect(label).toBeInTheDocument()
      expect(input).toBeInTheDocument()
    })

    it('renders name input with placeholder text', () => {
      render(<App />)
      const input = screen.getByPlaceholderText('Enter your name')
      expect(input).toBeInTheDocument()
    })

    it('renders Greet Me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toBeInTheDocument()
    })
  })

  describe('Get Message from Backend Feature Tests', () => {
    it('fetches and displays backend message on button click', async () => {
      const mockResponse = { message: 'Hello from the backend!' }
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText('Hello from the backend!')).toBeInTheDocument()
      })

      expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/api/hello`)
    })

    it('displays loading state during message fetch', async () => {
      global.fetch.mockImplementationOnce(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Hello from the backend!' }),
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      expect(screen.getByText('Loading...')).toBeInTheDocument()

      await waitFor(() => {
        expect(screen.getByText('Hello from the backend!')).toBeInTheDocument()
      })
    })

    it('displays error message when backend fetch fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText('Unable to connect to server')).toBeInTheDocument()
      })
    })
  })

  describe('Greeting Feature Tests', () => {
    it('submits name and displays greeting', async () => {
      const mockResponse = {
        greeting: 'Hello, Bob! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T14:30:00.000000Z'
      }
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText('Name')
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Bob')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('Hello, Bob! Welcome to our purple-themed app!')).toBeInTheDocument()
      })

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_URL}/api/greet`,
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: 'Bob' }),
        })
      )
    })

    it('displays error when submitting empty name', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /greet me/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('Please enter your name')).toBeInTheDocument()
      })

      // Should not call API
      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('displays error when submitting whitespace-only name', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText('Name')
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, '   ')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('Please enter your name')).toBeInTheDocument()
      })

      // Should not call API
      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('displays loading state during greeting fetch', async () => {
      global.fetch.mockImplementationOnce(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({
            greeting: 'Hello, Alice! Welcome to our purple-themed app!',
            timestamp: '2024-01-15T14:30:00.000000Z'
          }),
        }), 100))
      )

      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText('Name')
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Alice')
      await user.click(button)

      // Check for loading state - the button text changes to "Loading..."
      await waitFor(() => {
        expect(button).toHaveTextContent('Loading...')
      })

      await waitFor(() => {
        expect(screen.getByText('Hello, Alice! Welcome to our purple-themed app!')).toBeInTheDocument()
      })
    })

    it('displays network error message when greeting fetch fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText('Name')
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('Unable to connect to server')).toBeInTheDocument()
      })
    })

    it('clears input after successful greeting submission', async () => {
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T14:30:00.000000Z'
      }
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText('Name')
      const button = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'John')
      expect(input.value).toBe('John')
      
      await user.click(button)

      await waitFor(() => {
        expect(input.value).toBe('')
      })
    })

    it('submits greeting on Enter key press', async () => {
      const mockResponse = {
        greeting: 'Hello, Enter! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T14:30:00.000000Z'
      }
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText('Name')

      await user.type(input, 'Enter{Enter}')

      await waitFor(() => {
        expect(screen.getByText('Hello, Enter! Welcome to our purple-themed app!')).toBeInTheDocument()
      })
    })
  })

  describe('Feature Coexistence Tests', () => {
    it('allows using both features independently', async () => {
      // Mock both API calls
      const helloResponse = { message: 'Hello from the backend!' }
      const greetResponse = {
        greeting: 'Hello, Test! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T14:30:00.000000Z'
      }

      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => helloResponse,
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => greetResponse,
        })

      const user = userEvent.setup()
      render(<App />)
      
      // Use first feature
      const messageButton = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(messageButton)

      await waitFor(() => {
        expect(screen.getByText('Hello from the backend!')).toBeInTheDocument()
      })

      // Use second feature
      const input = screen.getByLabelText('Name')
      const greetButton = screen.getByRole('button', { name: /greet me/i })

      await user.type(input, 'Test')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText('Hello, Test! Welcome to our purple-themed app!')).toBeInTheDocument()
      })

      // Both messages should be visible
      expect(screen.getByText('Hello from the backend!')).toBeInTheDocument()
      expect(screen.getByText('Hello, Test! Welcome to our purple-themed app!')).toBeInTheDocument()
    })
  })

  describe('Accessibility Tests', () => {
    it('has accessible label for name input', () => {
      render(<App />)
      const input = screen.getByLabelText('Name')
      expect(input).toHaveAttribute('id', 'name-input')
    })

    it('buttons are keyboard accessible', () => {
      render(<App />)
      const messageButton = screen.getByRole('button', { name: /get message from backend/i })
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      expect(messageButton).toBeEnabled()
      expect(greetButton).toBeEnabled()
    })

    it('error messages have alert role', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /greet me/i })
      await user.click(button)

      await waitFor(() => {
        const error = screen.getByText('Please enter your name')
        expect(error).toHaveAttribute('role', 'alert')
      })
    })
  })
})