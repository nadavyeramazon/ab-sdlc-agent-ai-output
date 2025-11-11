/**
 * Comprehensive tests for App component.
 * 
 * Tests cover:
 * - Component rendering
 * - Static content display
 * - Button interactions
 * - API integration
 * - Loading states
 * - Error handling
 * - Accessibility
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockClear()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial Rendering', () => {
    it('renders the main heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i, level: 1 })
      expect(heading).toBeInTheDocument()
    })

    it('renders the fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('does not show loading indicator initially', () => {
      render(<App />)
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
    })

    it('does not show error message initially', () => {
      render(<App />)
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    })

    it('does not show success message initially', () => {
      render(<App />)
      expect(screen.queryByText(/hello world from backend/i)).not.toBeInTheDocument()
    })
  })

  describe('Button Click and Loading State', () => {
    it('shows loading state when button is clicked', async () => {
      // Mock delayed response
      fetch.mockImplementation(() => new Promise(resolve => {
        setTimeout(() => {
          resolve({
            ok: true,
            json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-15T10:30:00.000Z' })
          })
        }, 100)
      }))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      // Should show loading state
      expect(screen.getByRole('status')).toBeInTheDocument()
      expect(screen.getByText(/fetching message from backend/i)).toBeInTheDocument()
    })

    it('disables button during loading', async () => {
      fetch.mockImplementation(() => new Promise(resolve => {
        setTimeout(() => {
          resolve({
            ok: true,
            json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-15T10:30:00.000Z' })
          })
        }, 100)
      }))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      expect(button).toBeDisabled()
      expect(button).toHaveTextContent(/loading/i)
    })
  })

  describe('Successful API Response', () => {
    it('displays backend message on successful fetch', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: '2024-01-15T10:30:00.000Z' 
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
    })

    it('displays timestamp on successful fetch', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: '2024-01-15T10:30:00.000Z' 
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/timestamp:/i)).toBeInTheDocument()
      })
    })

    it('hides loading state after successful fetch', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: '2024-01-15T10:30:00.000Z' 
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      })
    })

    it('re-enables button after successful fetch', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: '2024-01-15T10:30:00.000Z' 
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message on network failure', async () => {
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        const errorElement = screen.getByRole('alert')
        expect(errorElement).toBeInTheDocument()
        expect(errorElement).toHaveTextContent(/unable to connect to backend/i)
      })
    })

    it('displays error message on HTTP error status', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        const errorElement = screen.getByRole('alert')
        expect(errorElement).toBeInTheDocument()
        expect(errorElement).toHaveTextContent(/error.*500/i)
      })
    })

    it('displays timeout error on request timeout', async () => {
      fetch.mockRejectedValueOnce(Object.assign(new Error('Aborted'), { name: 'AbortError' }))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        const errorElement = screen.getByRole('alert')
        expect(errorElement).toBeInTheDocument()
        expect(errorElement).toHaveTextContent(/timed out/i)
      })
    })

    it('hides loading state after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      })
    })

    it('re-enables button after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Multiple Requests', () => {
    it('clears previous message when fetching again', async () => {
      // First successful response
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'First message', 
          timestamp: '2024-01-15T10:30:00.000Z' 
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      await waitFor(() => {
        expect(screen.getByText('First message')).toBeInTheDocument()
      })

      // Second request with delayed response
      fetch.mockImplementation(() => new Promise(resolve => {
        setTimeout(() => {
          resolve({
            ok: true,
            json: async () => ({ message: 'Second message', timestamp: '2024-01-15T10:31:00.000Z' })
          })
        }, 100)
      }))

      await userEvent.click(button)
      
      // Previous message should be cleared during loading
      expect(screen.queryByText('First message')).not.toBeInTheDocument()
    })

    it('clears previous error when fetching again', async () => {
      // First request fails
      fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      // Second request succeeds
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: '2024-01-15T10:30:00.000Z' 
        })
      })

      await userEvent.click(button)
      
      // Error should be cleared
      await waitFor(() => {
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      })
    })
  })

  describe('API Call Details', () => {
    it('calls correct API endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: '2024-01-15T10:30:00.000Z' 
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
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
})
