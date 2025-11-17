/**
 * Comprehensive tests for App component
 * 
 * Tests cover:
 * - Component rendering
 * - Static content display
 * - Button functionality
 * - API integration (both /api/hello and /api/greet)
 * - Loading states
 * - Error handling
 * - Form validation
 * - Responsive behavior
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  describe('Static Content', () => {
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

    it('Get Message button is initially enabled', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('renders greeting input field', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      expect(input).toBeInTheDocument()
    })

    it('renders Greet Me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toBeInTheDocument()
    })

    it('Greet Me button is initially enabled', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('API Integration - /api/hello', () => {
    it('fetches and displays backend message on button click', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
      expect(fetch).toHaveBeenCalledTimes(1)
    })

    it('displays timestamp from backend response', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/received at:/i)).toBeInTheDocument()
      })
    })
  })

  describe('API Integration - /api/greet', () => {
    it('fetches and displays greeting on button click', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Hello, John! Welcome to our purple-themed app!/)).toBeInTheDocument()
      })

      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: 'John' }),
      })
    })

    it('displays greeting timestamp', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/greeted at:/i)).toBeInTheDocument()
      })
    })

    it('clears input field after successful greeting', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

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

    it('trims whitespace from name before sending', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, '  John  ')
      await user.click(button)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/greet', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name: 'John' }),
        })
      })
    })
  })

  describe('Form Validation - Greeting', () => {
    it('shows error when submitting empty name', async () => {
      const user = userEvent.setup()

      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })

      // Should not call API
      expect(fetch).not.toHaveBeenCalled()
    })

    it('shows error when submitting whitespace-only name', async () => {
      const user = userEvent.setup()

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, '   ')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })

      // Should not call API
      expect(fetch).not.toHaveBeenCalled()
    })
  })

  describe('Loading State', () => {
    it('shows loading text while fetching hello message', async () => {
      const user = userEvent.setup()
      
      // Create a promise that we can control
      let resolvePromise
      const fetchPromise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(fetchPromise)

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Wait for loading state to appear
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /loading/i })).toBeInTheDocument()
      })
      
      expect(button).toBeDisabled()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        }),
      })

      // Wait for loading to complete
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /get message from backend/i })).toBeInTheDocument()
      })
    })

    it('shows loading text while fetching greeting', async () => {
      const user = userEvent.setup()
      
      let resolvePromise
      const fetchPromise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(fetchPromise)

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      await user.click(button)

      // Wait for loading state to appear
      await waitFor(() => {
        const buttons = screen.getAllByRole('button', { name: /loading/i })
        expect(buttons.length).toBeGreaterThan(0)
      })
      
      expect(button).toBeDisabled()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:00.000Z'
        }),
      })

      // Wait for loading to complete
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /greet me/i })).toBeInTheDocument()
      })
    })

    it('disables hello button during loading', async () => {
      const user = userEvent.setup()
      
      let resolvePromise
      const fetchPromise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(fetchPromise)

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(button).toBeDisabled()
      })

      resolvePromise({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        }),
      })

      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('disables greeting input and button during loading', async () => {
      const user = userEvent.setup()
      
      let resolvePromise
      const fetchPromise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(fetchPromise)

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      await user.click(button)

      await waitFor(() => {
        expect(input).toBeDisabled()
        expect(button).toBeDisabled()
      })

      resolvePromise({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:00.000Z'
        }),
      })

      await waitFor(() => {
        expect(input).not.toBeDisabled()
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message when hello fetch fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.length).toBeGreaterThan(0)
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error message when hello response is not ok', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error message when greeting fetch fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch greeting/i)).toBeInTheDocument()
      })
    })

    it('clears previous hello messages when new fetch starts', async () => {
      const user = userEvent.setup()
      
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        }),
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Second fetch that fails
      fetch.mockRejectedValueOnce(new Error('Network error'))
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText('Hello World from Backend!')).not.toBeInTheDocument()
      })
    })

    it('clears previous greeting messages when new fetch starts', async () => {
      const user = userEvent.setup()
      
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:00.000Z'
        }),
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Hello, John! Welcome to our purple-themed app!/)).toBeInTheDocument()
      })

      // Second fetch that fails
      fetch.mockRejectedValueOnce(new Error('Network error'))
      
      await user.type(input, 'Jane')
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/Hello, John! Welcome to our purple-themed app!/)).not.toBeInTheDocument()
      })
    })
  })

  describe('Integration - Both Features', () => {
    it('both features work independently', async () => {
      const user = userEvent.setup()
      
      // Mock hello endpoint
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        }),
      })

      render(<App />)
      const helloButton = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(helloButton)

      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Mock greet endpoint
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Alice! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:31:00.000Z'
        }),
      })

      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Alice')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/Hello, Alice! Welcome to our purple-themed app!/)).toBeInTheDocument()
      })

      // Both messages should be visible
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      expect(screen.getByText(/Hello, Alice! Welcome to our purple-themed app!/)).toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    it('hello button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByLabelText('Get Message from Backend')
      expect(button).toBeInTheDocument()
    })

    it('greet button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByLabelText('Greet Me')
      expect(button).toBeInTheDocument()
    })

    it('greeting input has proper aria-label', () => {
      render(<App />)
      const input = screen.getByLabelText('Enter your name')
      expect(input).toBeInTheDocument()
    })

    it('error messages have alert role', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.length).toBeGreaterThan(0)
      })
    })
  })
})
