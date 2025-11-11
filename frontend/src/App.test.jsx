/**
 * Comprehensive test suite for App component
 * 
 * Tests rendering, user interactions, API integration,
 * error handling, and accessibility features.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

// Mock API URL to match test expectations
vi.mock('./App.jsx', async () => {
  const actual = await vi.importActual('./App.jsx')
  return actual
})

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockClear()
    // Set environment variable for tests
    import.meta.env.VITE_API_URL = 'http://localhost:8000'
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial Render', () => {
    it('renders the main heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i, level: 1 })
      expect(heading).toBeInTheDocument()
    })

    it('renders the subtitle', () => {
      render(<App />)
      expect(screen.getByText(/green theme fullstack application/i)).toBeInTheDocument()
    })

    it('renders the fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('does not show loading, error, or success messages initially', () => {
      render(<App />)
      expect(screen.queryByText(/fetching data/i)).not.toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(screen.queryByText(/response from backend/i)).not.toBeInTheDocument()
    })
  })

  describe('Successful API Call', () => {
    it('displays loading state when button is clicked', async () => {
      const user = userEvent.setup()
      
      // Mock successful API response with delay
      fetch.mockImplementation(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({
              message: 'Hello World from Backend!',
              timestamp: '2024-01-15T10:30:00.000Z'
            })
          }), 100)
        )
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Check loading state appears
      expect(screen.getByText(/fetching data from backend/i)).toBeInTheDocument()
      expect(screen.getByRole('status')).toBeInTheDocument()
      expect(button).toBeDisabled()
      expect(button).toHaveTextContent(/loading/i)
    })

    it('displays backend message and timestamp on successful fetch', async () => {
      const user = userEvent.setup()
      const mockTimestamp = '2024-01-15T10:30:00.000Z'
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: mockTimestamp
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Wait for success message to appear
      await waitFor(() => {
        expect(screen.getByText(/response from backend/i)).toBeInTheDocument()
      })

      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      expect(screen.getByText(/timestamp/i)).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('calls the correct API endpoint with environment variable', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        // Should use environment variable or default to localhost:8000
        expect(fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/hello'),
          expect.objectContaining({ signal: expect.any(AbortSignal) })
        )
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message when fetch fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Wait for error message to appear
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      expect(screen.getByText(/unable to connect to backend/i)).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('displays error message when API returns non-200 status', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      expect(screen.getByText(/http error.*500/i)).toBeInTheDocument()
    })

    it('displays timeout error when request takes too long', async () => {
      const user = userEvent.setup()
      
      // Mock fetch that simulates an abort error when aborted
      fetch.mockImplementation((url, options) => {
        return new Promise((resolve, reject) => {
          // Listen for abort signal
          if (options?.signal) {
            options.signal.addEventListener('abort', () => {
              const abortError = new Error('The user aborted a request.')
              abortError.name = 'AbortError'
              reject(abortError)
            })
          }
          // Don't resolve - simulate a hanging request
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Wait for timeout (5 seconds + buffer)
      await waitFor(
        () => {
          expect(screen.getByRole('alert')).toBeInTheDocument()
          expect(screen.getByText(/request timed out/i)).toBeInTheDocument()
        },
        { timeout: 6000 }
      )
    }, 10000)

    it('clears previous success message when new error occurs', async () => {
      const user = userEvent.setup()
      
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Second fetch fails
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      expect(screen.queryByText('Hello World from Backend!')).not.toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    it('has proper ARIA labels on button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label', 'Get Message from Backend')
    })

    it('has proper ARIA live regions for dynamic content', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Check loading state has aria-live
      const loadingStatus = screen.getByRole('status')
      expect(loadingStatus).toHaveAttribute('aria-live', 'polite')
      
      // Wait for success message
      await waitFor(() => {
        const successStatus = screen.getByRole('status')
        expect(successStatus).toHaveAttribute('aria-live', 'polite')
      })
    })

    it('error messages use role="alert"', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        const alert = screen.getByRole('alert')
        expect(alert).toBeInTheDocument()
      })
    })
  })

  describe('Button State Management', () => {
    it('disables button during fetch operation', async () => {
      const user = userEvent.setup()
      
      fetch.mockImplementation(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({
              message: 'Hello World from Backend!',
              timestamp: '2024-01-15T10:30:00.000Z'
            })
          }), 100)
        )
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      expect(button).not.toBeDisabled()
      
      await user.click(button)
      expect(button).toBeDisabled()
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('re-enables button after successful fetch', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(button).toHaveTextContent(/get message from backend/i)
      })
    })

    it('re-enables button after error', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Multiple Interactions', () => {
    it('allows multiple successful fetches', async () => {
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
      
      // First fetch
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Second fetch
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      expect(fetch).toHaveBeenCalledTimes(2)
    })
  })
})
