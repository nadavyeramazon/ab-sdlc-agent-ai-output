import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockReset()
  })

  describe('Initial Render - Story 1: Purple Theme', () => {
    it('displays Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveClass('hello-heading')
    })

    it('displays subtitle with purple theme reference', () => {
      render(<App />)
      expect(screen.getByText(/purple-themed fullstack application/i)).toBeInTheDocument()
    })

    it('displays fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('displays footer with tech stack info', () => {
      render(<App />)
      expect(screen.getByText(/built with react 18 \+ vite \+ fastapi/i)).toBeInTheDocument()
    })

    it('does not display message or error initially', () => {
      render(<App />)
      expect(screen.queryByText(/backend response/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
    })
  })

  describe('Backend API Integration - Story 4: Maintain Existing Functionality', () => {
    it('fetches and displays message from backend on button click', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      expect(screen.getByText(/hello world from backend!/i)).toBeInTheDocument()
    })

    it('displays loading state while fetching', async () => {
      const user = userEvent.setup()
      
      // Create a promise that won't resolve immediately
      let resolvePromise
      const promise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(promise)

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Button should show loading and be disabled
      expect(button).toHaveTextContent(/loading/i)
      expect(button).toBeDisabled()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:00.000000Z' })
      })

      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('displays error message when API call fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
    })

    it('displays error message when network error occurs', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
    })

    it('clears previous error when making new successful request', async () => {
      const user = userEvent.setup()
      
      // First request fails
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      // Second request succeeds
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
      })

      expect(screen.getByText(/backend response/i)).toBeInTheDocument()
    })

    it('formats timestamp in localized format', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      // Check that timestamp is displayed (format will vary by locale)
      const messageText = screen.getByText(/hello world from backend!/i).textContent
      expect(messageText).toMatch(/\(at .+\)/)
    })
  })

  describe('User Greet Feature - Story 3: Frontend User Greeting', () => {
    it('displays greet section heading', () => {
      render(<App />)
      expect(screen.getByRole('heading', { name: /get personalized greeting/i })).toBeInTheDocument()
    })

    it('displays name input field with label', () => {
      render(<App />)
      const input = screen.getByLabelText(/name/i)
      expect(input).toBeInTheDocument()
      expect(input).toHaveAttribute('placeholder', 'Enter your name')
      expect(input).toHaveAttribute('type', 'text')
    })

    it('displays greet me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('displays character counter', () => {
      render(<App />)
      expect(screen.getByText(/0\/100 characters/i)).toBeInTheDocument()
    })

    it('allows typing in name input field', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText(/name/i)
      await user.type(input, 'Alice')
      
      expect(input).toHaveValue('Alice')
    })

    it('updates character counter when typing', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText(/name/i)
      await user.type(input, 'Alice')
      
      expect(screen.getByText(/5\/100 characters/i)).toBeInTheDocument()
    })

    it('shows validation error when name is empty', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /greet me/i })
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })
    })

    it('shows validation error when name is only whitespace', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, '   ')
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })
    })

    it('enforces max length of 100 characters', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText(/name/i)
      expect(input).toHaveAttribute('maxLength', '100')
      
      // Try to type 105 characters
      const longName = 'A'.repeat(105)
      await user.type(input, longName)
      
      // Input should only contain 100 characters
      expect(input.value).toHaveLength(100)
    })

    it('shows validation error when name exceeds max length', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      // Manually set value to bypass maxLength (simulating paste)
      const tooLongName = 'A'.repeat(101)
      input.value = tooLongName
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/name must be 100 characters or less/i)).toBeInTheDocument()
      })
    })

    it('displays personalized greeting on successful API call', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        greeting: 'Hello, Alice! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.000000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Alice')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, alice! welcome to our purple-themed app!/i)).toBeInTheDocument()
      })
    })

    it('displays loading state during greet API call', async () => {
      const user = userEvent.setup()
      
      let resolvePromise
      const promise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(promise)

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Bob')
      await user.click(button)

      // Button should show loading and be disabled
      await waitFor(() => {
        expect(button).toHaveTextContent(/loading/i)
        expect(button).toBeDisabled()
      })

      // Input should be disabled during loading
      expect(input).toBeDisabled()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({ 
          greeting: 'Hello, Bob! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(input).not.toBeDisabled()
      })
    })

    it('displays error message when greet API call fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Server error' })
      })

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Charlie')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })
    })

    it('displays network error message when API call fails completely', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Dave')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
      })
    })

    it('supports Enter key to submit greeting', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        greeting: 'Hello, Eve! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00.000000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      
      await user.type(input, 'Eve')
      await user.keyboard('{Enter}')

      await waitFor(() => {
        expect(screen.getByText(/hello, eve! welcome to our purple-themed app!/i)).toBeInTheDocument()
      })
    })

    it('clears error on successful retry', async () => {
      const user = userEvent.setup()
      
      // First attempt fails
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Name cannot be empty' })
      })

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, 'Frank')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      // Second attempt succeeds
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Frank! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
        expect(screen.getByText(/hello, frank! welcome to our purple-themed app!/i)).toBeInTheDocument()
      })
    })
  })

  describe('Integration - Both Features Work Together', () => {
    it('both greet and backend message features work independently', async () => {
      const user = userEvent.setup()
      
      // Mock greet API call
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Grace! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      render(<App />)
      
      // Use greet feature
      const nameInput = screen.getByLabelText(/name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(nameInput, 'Grace')
      await user.click(greetButton)

      await waitFor(() => {
        expect(screen.getByText(/hello, grace! welcome to our purple-themed app!/i)).toBeInTheDocument()
      })

      // Mock backend message API call
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      // Use backend message feature
      const backendButton = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(backendButton)

      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      // Both messages should be visible
      expect(screen.getByText(/hello, grace! welcome to our purple-themed app!/i)).toBeInTheDocument()
      expect(screen.getByText(/hello world from backend!/i)).toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    it('backend button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /fetch message from backend/i })
      expect(button).toHaveAttribute('aria-label', 'Fetch message from backend')
    })

    it('greet button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get personalized greeting/i })
      expect(button).toHaveAttribute('aria-label', 'Get personalized greeting')
    })

    it('name input has proper aria-label', () => {
      render(<App />)
      const input = screen.getByLabelText(/name/i)
      expect(input).toHaveAttribute('aria-label', 'Name input')
    })

    it('message boxes have role="alert"', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      render(<App />)
      await user.click(screen.getByRole('button', { name: /get message from backend/i }))

      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.length).toBeGreaterThan(0)
      })
    })
  })

  describe('Multiple Requests', () => {
    it('can fetch multiple times successfully', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: new Date().toISOString()
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      // Second click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      expect(fetch).toHaveBeenCalledTimes(2)
    })

    it('can greet multiple different users', async () => {
      const user = userEvent.setup()
      
      // First user
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Alice! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.clear(input)
      await user.type(input, 'Alice')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, alice!/i)).toBeInTheDocument()
      })

      // Second user
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Bob! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T10:31:00.000000Z'
        })
      })

      await user.clear(input)
      await user.type(input, 'Bob')
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello, bob!/i)).toBeInTheDocument()
      })

      expect(fetch).toHaveBeenCalledTimes(2)
    })
  })

  describe('DoS Prevention - Max Length Validation', () => {
    it('accepts name at max length (100 characters)', async () => {
      const user = userEvent.setup()
      const maxLengthName = 'A'.repeat(100)
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: `Hello, ${maxLengthName}! Welcome to our purple-themed app!`,
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      render(<App />)
      const input = screen.getByLabelText(/name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await user.type(input, maxLengthName)
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/hello.*welcome to our purple-themed app!/i)).toBeInTheDocument()
      })
    })

    it('prevents input beyond max length via HTML maxLength attribute', () => {
      render(<App />)
      const input = screen.getByLabelText(/name/i)
      
      // Verify maxLength attribute is set
      expect(input).toHaveAttribute('maxLength', '100')
    })
  })
})
