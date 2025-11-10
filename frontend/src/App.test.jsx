/**
 * Frontend Component Tests
 * 
 * Comprehensive test suite for the App component using React Testing Library.
 * Tests user interactions, API calls, loading states, and error handling.
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

    it('renders subtitle text', () => {
      render(<App />)
      const subtitle = screen.getByText(/green theme fullstack application/i)
      expect(subtitle).toBeInTheDocument()
    })

    it('renders fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('does not show message initially', () => {
      render(<App />)
      const messageHeading = screen.queryByText(/response from backend/i)
      expect(messageHeading).not.toBeInTheDocument()
    })

    it('does not show loading indicator initially', () => {
      render(<App />)
      const loadingText = screen.queryByText(/fetching data from backend/i)
      expect(loadingText).not.toBeInTheDocument()
    })

    it('does not show error initially', () => {
      render(<App />)
      const errorText = screen.queryByRole('alert')
      expect(errorText).not.toBeInTheDocument()
    })
  })

  describe('Button Click and API Call', () => {
    it('shows loading state when button is clicked', async () => {
      // Mock fetch to simulate pending request
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      // Check loading state
      await waitFor(() => {
        expect(screen.getByText(/loading/i)).toBeInTheDocument()
      })

      expect(screen.getByText(/fetching data from backend/i)).toBeInTheDocument()
      expect(screen.getByRole('status')).toBeInTheDocument()
    })

    it('disables button during loading', async () => {
      // Mock fetch to simulate pending request
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(button).toBeDisabled()
      })
    })

    it('makes API call to correct endpoint', async () => {
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

  describe('Successful API Response', () => {
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

    it('displays formatted timestamp', async () => {
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
        expect(screen.getByText(/timestamp:/i)).toBeInTheDocument()
      })
    })

    it('hides loading indicator after successful fetch', async () => {
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
        expect(screen.queryByText(/fetching data from backend/i)).not.toBeInTheDocument()
      })
    })

    it('re-enables button after successful fetch', async () => {
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
        expect(button).not.toBeDisabled()
      })
    })

    it('allows multiple fetches', async () => {
      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First fetch
      fireEvent.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Second fetch
      fireEvent.click(button)
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledTimes(2)
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message when fetch fails', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })

    it('displays specific error for failed to connect', async () => {
      fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument()
      })
    })

    it('displays error for HTTP errors', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Internal server error' })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
    })

    it('hides loading indicator when error occurs', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/fetching data from backend/i)).not.toBeInTheDocument()
      })
    })

    it('re-enables button when error occurs', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('handles timeout errors', async () => {
      // Mock fetch to simulate timeout
      fetch.mockImplementationOnce(() => {
        const error = new Error('The operation was aborted')
        error.name = 'AbortError'
        return Promise.reject(error)
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/request timeout/i)).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByLabelText(/get message from backend/i)
      expect(button).toBeInTheDocument()
    })

    it('loading indicator has proper role and aria-live', async () => {
      fetch.mockImplementationOnce(() => new Promise(() => {}))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        const loadingStatus = screen.getByRole('status')
        expect(loadingStatus).toBeInTheDocument()
      })
    })

    it('error message has proper role', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        const errorAlert = screen.getByRole('alert')
        expect(errorAlert).toBeInTheDocument()
      })
    })
  })

  describe('State Management', () => {
    it('clears previous message when fetching again', async () => {
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'First message',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText('First message')).toBeInTheDocument()
      })

      // Second fetch that will show loading
      fetch.mockImplementationOnce(() => new Promise(() => {}))
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.queryByText('First message')).not.toBeInTheDocument()
      })
    })

    it('clears previous error when fetching again', async () => {
      // First fetch fails
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      // Second successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:45.123456Z'
        })
      })

      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      })
    })
  })
})
