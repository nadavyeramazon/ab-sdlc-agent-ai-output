/**
 * Frontend Component Tests
 * 
 * Comprehensive test suite for the App component using React Testing Library.
 * Tests user interactions, API calls, loading states, and error handling.
 * Includes tests for both existing hello endpoint and new greeting feature.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  describe('Initial Render', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i, level: 1 })
      expect(heading).toBeInTheDocument()
    })

    it('renders subtitle text with purple theme', () => {
      render(<App />)
      const subtitle = screen.getByText(/purple theme fullstack application/i)
      expect(subtitle).toBeInTheDocument()
    })

    it('renders fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('renders greeting section', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /get your personalized greeting/i, level: 3 })
      expect(heading).toBeInTheDocument()
    })

    it('renders name input field', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      expect(input).toBeInTheDocument()
    })

    it('renders greet me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toBeInTheDocument()
    })

    it('name input has proper label', () => {
      render(<App />)
      const label = screen.getByText(/your name/i)
      expect(label).toBeInTheDocument()
    })

    it('buttons are enabled initially', () => {
      render(<App />)
      const fetchButton = screen.getByRole('button', { name: /get message from backend/i })
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      expect(fetchButton).not.toBeDisabled()
      expect(greetButton).not.toBeDisabled()
    })
  })

  describe('Existing Hello Endpoint (Preserved Functionality)', () => {
    it('shows loading state when fetch button is clicked', async () => {
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/loading/i)).toBeInTheDocument()
      })
    })

    it('displays backend message on successful fetch', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
    })

    it('makes API call to /api/hello endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/hello',
          expect.objectContaining({
            signal: expect.any(AbortSignal)
          })
        )
      })
    })
  })

  describe('Greeting Input Field', () => {
    it('allows user to type in name input', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByPlaceholderText(/enter your name/i)
      await user.type(input, 'John')
      
      expect(input).toHaveValue('John')
    })

    it('input field is a controlled component', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByPlaceholderText(/enter your name/i)
      await user.type(input, 'Alice')
      
      expect(input.value).toBe('Alice')
    })

    it('input has accessible label', () => {
      render(<App />)
      const input = screen.getByLabelText(/your name/i)
      expect(input).toBeInTheDocument()
    })
  })

  describe('Client-Side Validation', () => {
    it('shows validation error when greet button clicked with empty name', async () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })
    })

    it('shows validation error for whitespace-only name', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, '   ')
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })
    })

    it('clears validation error when user starts typing', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      // Trigger validation error
      fireEvent.click(button)
      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })

      // Start typing
      await user.type(input, 'J')
      
      // Validation error should be cleared
      expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
    })

    it('does not make API call when validation fails', async () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })

      // Fetch should not have been called
      expect(fetch).not.toHaveBeenCalledWith(
        'http://localhost:8000/api/greet',
        expect.anything()
      )
    })
  })

  describe('Greeting API Integration', () => {
    it('makes POST request to /api/greet with valid name', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: 'John' }),
            signal: expect.any(AbortSignal)
          })
        )
      })
    })

    it('sends trimmed name to backend', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, '  John  ')
      fireEvent.click(button)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            body: JSON.stringify({ name: 'John' })
          })
        )
      })
    })

    it('displays personalized greeting from backend', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Alice! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Alice')
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Hello, Alice! Welcome to our purple-themed app!/i)).toBeInTheDocument()
      })
    })

    it('displays greeting with purple theme styling', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        // Use more specific query - look for the heading with level 4
        expect(screen.getByRole('heading', { name: /your personalized greeting/i, level: 4 })).toBeInTheDocument()
      })
    })
  })

  describe('Greeting Loading State', () => {
    it('shows loading indicator during greeting API call', async () => {
      const user = userEvent.setup()
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/getting your personalized greeting/i)).toBeInTheDocument()
      })
    })

    it('disables greet button during loading', async () => {
      const user = userEvent.setup()
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(button).toBeDisabled()
      })
    })

    it('disables input field during loading', async () => {
      const user = userEvent.setup()
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(input).toBeDisabled()
      })
    })

    it('re-enables button after successful greeting fetch', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('hides loading indicator after successful fetch', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/getting your personalized greeting/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Greeting Error Handling', () => {
    it('displays network error message when fetch fails', async () => {
      const user = userEvent.setup()
      fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
      })
    })

    it('displays backend validation error for empty name', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Name cannot be empty' })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      // Type space to bypass client validation
      await user.type(input, 'a')
      await user.clear(input)
      await user.type(input, 'a') // Add something to pass validation
      
      fireEvent.click(button)

      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.length).toBeGreaterThan(0)
      })
    })

    it('re-enables button after error', async () => {
      const user = userEvent.setup()
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('State Management', () => {
    it('clears previous greeting when new request is submitted', async () => {
      const user = userEvent.setup()
      
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Hello, John!/i)).toBeInTheDocument()
      })

      // Clear input and submit again
      await user.clear(input)
      await user.type(input, 'Alice')
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Alice! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Hello, Alice!/i)).toBeInTheDocument()
      })
    })

    it('clears previous error when new request is submitted', async () => {
      const user = userEvent.setup()
      
      // First fetch fails
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      // Second successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('greeting form has proper structure', () => {
      render(<App />)
      const input = screen.getByLabelText(/your name/i)
      expect(input).toBeInTheDocument()
    })

    it('validation error has proper role', async () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        const error = screen.getByText(/please enter your name/i)
        expect(error).toHaveAttribute('role', 'alert')
      })
    })

    it('loading indicator has proper role for greeting', async () => {
      const user = userEvent.setup()
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(button)

      await waitFor(() => {
        const loadingStatuses = screen.getAllByRole('status')
        expect(loadingStatuses.length).toBeGreaterThan(0)
      })
    })
  })

  describe('Multiple Features Working Together', () => {
    it('both hello and greeting features work independently', async () => {
      const user = userEvent.setup()
      
      // Test hello endpoint
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const helloButton = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(helloButton)

      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Test greeting endpoint
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, John! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'John')
      fireEvent.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/Hello, John!/i)).toBeInTheDocument()
      })

      // Both messages should be visible
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      expect(screen.getByText(/Hello, John!/i)).toBeInTheDocument()
    })
  })
})
