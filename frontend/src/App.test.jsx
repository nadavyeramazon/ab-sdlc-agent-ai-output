/**
 * Comprehensive test suite for React frontend
 * 
 * Tests cover:
 * - Component rendering
 * - User interactions
 * - API integration
 * - Error handling
 * - Loading states
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch API
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('Static Content Tests - US-1', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading.tagName).toBe('H1')
    })

    it('renders with correct CSS classes for green theme', () => {
      const { container } = render(<App />)
      expect(container.querySelector('.app-container')).toBeInTheDocument()
      expect(container.querySelector('.main-heading')).toBeInTheDocument()
    })

    it('displays the fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('Get Message from Backend')
    })
  })

  describe('Button Interaction Tests - US-3', () => {
    it('button is clickable and not disabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('shows loading state when button is clicked', async () => {
      // Mock a delayed response
      global.fetch.mockImplementation(() => 
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
      
      await userEvent.click(button)
      
      // Check loading state
      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()
    })
  })

  describe('API Integration Tests - US-2, US-3', () => {
    it('fetches and displays backend message successfully', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      // Wait for message to appear
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Check that timestamp is displayed
      expect(screen.getByText(/received at:/i)).toBeInTheDocument()
    })

    it('calls correct API endpoint', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Test',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/hello',
          expect.objectContaining({
            signal: expect.any(AbortSignal)
          })
        )
      })
    })

    it('formats timestamp in human-readable format', async () => {
      const mockTimestamp = '2024-01-15T10:30:00.000Z'
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: mockTimestamp
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        const timestampElement = screen.getByText(/received at:/i)
        expect(timestampElement).toBeInTheDocument()
        // Timestamp should be formatted (not raw ISO string)
        expect(timestampElement.textContent).not.toContain('2024-01-15T10:30:00.000Z')
      })
    })
  })

  describe('Error Handling Tests - US-3 AC7, AC9', () => {
    it('displays error message when fetch fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect to backend/i)).toBeInTheDocument()
      })
    })

    it('displays error when API returns non-ok response', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/http error/i)).toBeInTheDocument()
      })
    })

    it('handles timeout errors', async () => {
      // Mock a request that never resolves
      global.fetch.mockImplementation(() => 
        new Promise((resolve, reject) => {
          // Simulate abort after timeout
          setTimeout(() => {
            const error = new Error('The operation was aborted')
            error.name = 'AbortError'
            reject(error)
          }, 100)
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/request timed out/i)).toBeInTheDocument()
      }, { timeout: 6000 })
    })

    it('clears previous error when new request is made', async () => {
      // First request fails
      global.fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/unable to connect/i)).toBeInTheDocument()
      })

      // Second request succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      await userEvent.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/unable to connect/i)).not.toBeInTheDocument()
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
    })
  })

  describe('Loading State Tests', () => {
    it('button returns to normal state after successful fetch', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Test',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        expect(button).toHaveTextContent('Get Message from Backend')
        expect(button).not.toBeDisabled()
      })
    })

    it('button returns to normal state after error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)

      await waitFor(() => {
        expect(button).toHaveTextContent('Get Message from Backend')
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Accessibility Tests', () => {
    it('button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label', 'Get message from backend')
    })

    it('heading uses proper semantic HTML', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toBeInTheDocument()
    })
  })
})
