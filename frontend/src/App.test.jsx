/**
 * Comprehensive tests for App component.
 * 
 * Tests:
 * - Component rendering
 * - Button interactions
 * - API call handling
 * - Loading states
 * - Error handling
 * - Backend response display
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
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

  describe('Initial Render', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
    })

    it('renders fetch button with correct label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('does not display backend message initially', () => {
      render(<App />)
      const message = screen.queryByText(/hello world from backend/i)
      expect(message).not.toBeInTheDocument()
    })

    it('does not display error message initially', () => {
      render(<App />)
      const error = screen.queryByText(/failed to fetch/i)
      expect(error).not.toBeInTheDocument()
    })
  })

  describe('Button Click and API Call', () => {
    it('shows loading state when button is clicked', async () => {
      // Mock a delayed response
      fetch.mockImplementationOnce(() => 
        new Promise(resolve => {
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({
              message: 'Hello World from Backend!',
              timestamp: '2024-01-15T10:30:00.123456Z'
            })
          }), 100)
        })
      )

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      // Check loading state
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
      expect(button).toBeDisabled()
    })

    it('calls backend API with correct URL', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.123456Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
      })
    })
  })

  describe('Successful API Response', () => {
    it('displays backend message after successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
    })

    it('displays timestamp after successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/timestamp: 2024-01-15T10:30:00.123456Z/i)).toBeInTheDocument()
      })
    })

    it('hides loading state after successful fetch', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.123456Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message when fetch fails', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error message when response is not ok', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch from backend/i)).toBeInTheDocument()
      })
    })

    it('does not display backend message on error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        const message = screen.queryByText(/hello world from backend/i)
        expect(message).not.toBeInTheDocument()
      })
    })

    it('hides loading state after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Multiple API Calls', () => {
    it('clears error message on subsequent successful fetch', async () => {
      // First call fails
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument()
      })

      // Second call succeeds
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.123456Z'
        })
      })

      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
    })

    it('updates message on multiple successful fetches', async () => {
      // First call
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.123456Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Second call with different timestamp
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T11:30:00.789012Z'
        })
      })

      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/timestamp: 2024-01-15T11:30:00.789012Z/i)).toBeInTheDocument()
      })
    })
  })
})
