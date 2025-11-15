import { describe, it, expect, vi, beforeEach } from 'vitest'
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

  describe('Initial Render', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
    })

    it('renders button with correct text', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('Get Message from Backend')
    })

    it('button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('does not show message initially', () => {
      render(<App />)
      const successMessage = screen.queryByText(/hello world from backend/i)
      expect(successMessage).not.toBeInTheDocument()
    })

    it('does not show error initially', () => {
      render(<App />)
      const errorMessage = screen.queryByText(/failed to fetch/i)
      expect(errorMessage).not.toBeInTheDocument()
    })
  })

  describe('Successful API Call', () => {
    it('displays loading state when button is clicked', async () => {
      const user = userEvent.setup()
      
      // Mock successful API response with delay
      fetch.mockImplementationOnce(() =>
        new Promise(resolve => 
          setTimeout(() => 
            resolve({
              ok: true,
              json: async () => ({ 
                message: 'Hello World from Backend!',
                timestamp: '2024-01-15T10:30:00.000Z'
              })
            }), 100
          )
        )
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Check loading state
      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()
      expect(screen.getByText(/fetching message/i)).toBeInTheDocument()
    })

    it('displays backend message after successful fetch', async () => {
      const user = userEvent.setup()
      
      // Mock successful API response
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
      
      // Wait for message to appear
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
      
      // Button should be enabled again
      expect(button).not.toBeDisabled()
      expect(button).toHaveTextContent('Get Message from Backend')
    })

    it('calls correct API endpoint', async () => {
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
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
      expect(fetch).toHaveBeenCalledTimes(1)
    })
  })

  describe('Failed API Call', () => {
    it('displays error message when fetch fails', async () => {
      const user = userEvent.setup()
      
      // Mock network error
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Wait for error message
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
      
      // Button should be enabled again
      expect(button).not.toBeDisabled()
    })

    it('displays error message when response is not ok', async () => {
      const user = userEvent.setup()
      
      // Mock HTTP error response
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Wait for error message
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })

    it('clears previous message when new request fails', async () => {
      const user = userEvent.setup()
      
      // First request succeeds
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

      // Second request fails
      fetch.mockRejectedValueOnce(new Error('Network error'))
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText('Hello World from Backend!')).not.toBeInTheDocument()
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })
  })

  describe('Multiple Requests', () => {
    it('handles multiple successful requests', async () => {
      const user = userEvent.setup()
      
      // Mock two successful responses
      fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!',
            timestamp: '2024-01-15T10:30:00.000Z'
          })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!',
            timestamp: '2024-01-15T10:31:00.000Z'
          })
        })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
      
      // Second click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
      
      expect(fetch).toHaveBeenCalledTimes(2)
    })
  })

  describe('Accessibility', () => {
    it('button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label', 'Get message from backend')
    })

    it('loading indicator has role and aria-live', async () => {
      const user = userEvent.setup()
      
      fetch.mockImplementationOnce(() =>
        new Promise(resolve => 
          setTimeout(() => 
            resolve({
              ok: true,
              json: async () => ({ 
                message: 'Hello World from Backend!',
                timestamp: '2024-01-15T10:30:00.000Z'
              })
            }), 100
          )
        )
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      const loadingIndicator = screen.getByRole('status')
      expect(loadingIndicator).toHaveAttribute('aria-live', 'polite')
    })

    it('success message has role alert and aria-live', async () => {
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
        const successMessage = screen.getByRole('alert', { name: /hello world from backend/i })
        expect(successMessage).toHaveAttribute('aria-live', 'polite')
      })
    })

    it('error message has role alert and aria-live assertive', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        const errorMessage = screen.getByRole('alert', { name: /failed to fetch/i })
        expect(errorMessage).toHaveAttribute('aria-live', 'assertive')
      })
    })
  })
})
