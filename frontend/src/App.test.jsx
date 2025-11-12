import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  describe('Static UI Elements', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading.tagName).toBe('H1')
    })

    it('renders Get Message from Backend button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).toBeEnabled()
    })

    it('button is not disabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('API Integration - Success Scenarios', () => {
    it('fetches and displays backend message on button click', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:45.123Z',
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      // Wait for the message to appear
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Verify timestamp is also displayed
      expect(screen.getByText(/timestamp:/i)).toBeInTheDocument()
      expect(screen.getByText(/2024-01-15T10:30:45.123Z/i)).toBeInTheDocument()
    })

    it('calls correct API endpoint', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:45.123Z',
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/hello',
          expect.objectContaining({
            signal: expect.any(AbortSignal),
          })
        )
      })
    })
  })

  describe('Loading States', () => {
    it('shows loading indicator during API call', async () => {
      global.fetch.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:45.123Z' }),
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      // Check that button shows "Loading..."
      expect(screen.getByRole('button', { name: /loading/i })).toBeInTheDocument()
      
      // Check that button is disabled during loading
      expect(button).toBeDisabled()

      // Wait for loading to complete
      await waitFor(() => {
        expect(screen.getByText('Test')).toBeInTheDocument()
      })

      // Button should be enabled again
      expect(button).toBeEnabled()
    })
  })

  describe('Error Handling', () => {
    it('displays error message when API call fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/failed to fetch data/i)).toBeInTheDocument()
      })
    })

    it('displays timeout error when request times out', async () => {
      const abortError = new Error('Aborted')
      abortError.name = 'AbortError'
      global.fetch.mockRejectedValueOnce(abortError)

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/request timed out/i)).toBeInTheDocument()
      })
    })

    it('displays error when API returns non-200 status', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/failed to fetch data/i)).toBeInTheDocument()
      })
    })
  })

  describe('State Management', () => {
    it('clears previous error when making new request', async () => {
      // First request fails
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch data/i)).toBeInTheDocument()
      })

      // Second request succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:45.123Z',
        }),
      })

      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch data/i)).not.toBeInTheDocument()
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
    })

    it('clears previous message when making new request', async () => {
      // First request
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'First Message',
          timestamp: '2024-01-15T10:30:45.123Z',
        }),
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText('First Message')).toBeInTheDocument()
      })

      // Second request
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Second Message',
          timestamp: '2024-01-15T10:30:50.456Z',
        }),
      })

      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText('Second Message')).toBeInTheDocument()
        expect(screen.queryByText('First Message')).not.toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('response has proper ARIA live region', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:45.123Z',
        }),
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        const response = screen.getByRole('status')
        expect(response).toHaveAttribute('aria-live', 'polite')
      })
    })

    it('error has proper ARIA alert role', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        const alert = screen.getByRole('alert')
        expect(alert).toHaveAttribute('aria-live', 'assertive')
      })
    })

    it('button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label', 'Get message from backend')
    })
  })
})
