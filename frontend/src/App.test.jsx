/**
 * Comprehensive tests for App component
 * 
 * Tests cover:
 * - Component rendering
 * - Static content display
 * - Button functionality
 * - API integration
 * - Loading states
 * - Error handling
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

    it('button is initially enabled', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('API Integration', () => {
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

  describe('Loading State', () => {
    it('shows loading text while fetching', async () => {
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

    it('disables button during loading', async () => {
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
  })

  describe('Error Handling', () => {
    it('displays error message when fetch fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error message when response is not ok', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })

    it('clears previous messages when new fetch starts', async () => {
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
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByLabelText('Get Message from Backend')
      expect(button).toBeInTheDocument()
    })

    it('error message has alert role', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        const alert = screen.getByRole('alert')
        expect(alert).toBeInTheDocument()
      })
    })
  })
})
