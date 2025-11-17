/**
 * Comprehensive test suite for App component.
 * 
 * Tests:
 * - Component rendering
 * - Static content display
 * - Button interactions
 * - API calls and responses
 * - Loading states
 * - Error handling
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

  describe('Initial Render', () => {
    it('renders without crashing', () => {
      render(<App />)
      expect(screen.getByText('Hello World')).toBeInTheDocument()
    })

    it('displays the main heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveClass('main-heading')
    })

    it('displays the subtitle', () => {
      render(<App />)
      const subtitle = screen.getByText(/welcome to the yellow theme fullstack application/i)
      expect(subtitle).toBeInTheDocument()
    })

    it('displays the fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('does not show backend message initially', () => {
      render(<App />)
      const backendMessage = screen.queryByTestId('backend-message')
      expect(backendMessage).not.toBeInTheDocument()
    })

    it('does not show error message initially', () => {
      render(<App />)
      const errorMessage = screen.queryByTestId('error-message')
      expect(errorMessage).not.toBeInTheDocument()
    })
  })

  describe('Button Click and API Call', () => {
    it('calls fetch with correct URL when button is clicked', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      expect(fetch).toHaveBeenCalledTimes(1)
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    })

    it('displays loading indicator while fetching', async () => {
      fetch.mockImplementationOnce(() => new Promise(() => {})) // Never resolves

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      expect(screen.getByTestId('loading-indicator')).toBeInTheDocument()
      expect(screen.getByText('Loading...')).toBeInTheDocument()
    })

    it('disables button while loading', async () => {
      fetch.mockImplementationOnce(() => new Promise(() => {})) // Never resolves

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      expect(button).toBeDisabled()
    })
  })

  describe('Successful API Response', () => {
    it('displays backend response after successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByTestId('backend-message')).toBeInTheDocument()
      })

      expect(screen.getByText(/hello world from backend!/i)).toBeInTheDocument()
      expect(screen.getByText(/2024-01-15T10:30:00.000Z/i)).toBeInTheDocument()
    })

    it('hides loading indicator after successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByTestId('loading-indicator')).not.toBeInTheDocument()
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message when fetch fails', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByTestId('error-message')).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch from backend/i)).toBeInTheDocument()
      expect(screen.getByText(/network error/i)).toBeInTheDocument()
    })

    it('displays error message when response is not ok', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      })

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByTestId('error-message')).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch from backend/i)).toBeInTheDocument()
      expect(screen.getByText(/500/i)).toBeInTheDocument()
    })

    it('hides loading indicator after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByTestId('loading-indicator')).not.toBeInTheDocument()
      })
    })
  })

  describe('Multiple Clicks', () => {
    it('clears previous messages when button is clicked again', async () => {
      const mockResponse1 = {
        message: 'First message',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      const mockResponse2 = {
        message: 'Second message',
        timestamp: '2024-01-15T10:31:00.000Z'
      }

      fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockResponse1,
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockResponse2,
        })

      const user = userEvent.setup()
      render(<App />)

      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/first message/i)).toBeInTheDocument()
      })

      // Second click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/second message/i)).toBeInTheDocument()
      })

      expect(screen.queryByText(/first message/i)).not.toBeInTheDocument()
    })
  })
})
