/**
 * Comprehensive test suite for App component.
 * 
 * Tests:
 * - Static content rendering
 * - Button functionality
 * - API integration
 * - Loading states
 * - Error handling
 * - User interactions
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

describe('App Component', () => {
  // Reset fetch mock before each test
  beforeEach(() => {
    global.fetch = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('Static Content', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
    })

    it('renders button with correct label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('Button Click and API Integration', () => {
    it('displays loading state when button is clicked', async () => {
      // Mock fetch to delay response
      global.fetch = vi.fn(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-15T10:30:00Z' })
          }), 100)
        )
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      // Check loading state
      expect(screen.getByText(/loading\.\.\./i)).toBeInTheDocument()
      expect(button).toBeDisabled()
    })

    it('fetches and displays message from backend on success', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00Z'
      }

      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => mockResponse,
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      // Wait for message to appear
      await waitFor(() => {
        expect(screen.getByText(mockResponse.message)).toBeInTheDocument()
      })

      // Verify fetch was called with correct URL
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    })

    it('displays error message when fetch fails', async () => {
      global.fetch = vi.fn(() =>
        Promise.reject(new Error('Network error'))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      // Wait for error message to appear
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error message when API returns non-OK status', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 500,
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      // Wait for error message to appear
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })
    })

    it('button can be clicked multiple times', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-15T10:30:00Z' }),
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First click
      await userEvent.click(button)
      await waitFor(() => {
        expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
      })

      // Second click
      await userEvent.click(button)
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledTimes(2)
      })
    })
  })

  describe('State Management', () => {
    it('clears previous messages when fetching new data', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => ({ message: 'First message', timestamp: '2024-01-15T10:30:00Z' }),
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      await waitFor(() => {
        expect(screen.getByText('First message')).toBeInTheDocument()
      })

      // Mock new response
      global.fetch = vi.fn(() =>
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({ message: 'Second message', timestamp: '2024-01-15T10:31:00Z' })
          }), 50)
        )
      )

      await userEvent.click(button)
      
      // During loading, first message should be cleared
      await waitFor(() => {
        expect(screen.queryByText('First message')).not.toBeInTheDocument()
      })
    })

    it('clears error when making new request', async () => {
      // First request fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
      })

      // Second request succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Success message', timestamp: '2024-01-15T10:30:00Z' }),
        })
      )

      await userEvent.click(button)
      
      // Error should be cleared during loading
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch message from backend/i)).not.toBeInTheDocument()
      })

      // Success message should appear
      await waitFor(() => {
        expect(screen.getByText('Success message')).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('loading indicator has role status', async () => {
      global.fetch = vi.fn(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:00Z' })
          }), 100)
        )
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      const loadingElement = screen.getByRole('status')
      expect(loadingElement).toBeInTheDocument()
    })

    it('message has role alert', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => ({ message: 'Test message', timestamp: '2024-01-15T10:30:00Z' }),
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.length).toBeGreaterThan(0)
      })
    })

    it('error has role alert', async () => {
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.length).toBeGreaterThan(0)
      })
    })
  })
})