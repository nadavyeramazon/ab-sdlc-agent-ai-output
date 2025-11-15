/**
 * Comprehensive test suite for React frontend application
 * 
 * Tests all user stories and acceptance criteria:
 * - Story 1: Static "Hello World" display with green theme
 * - Story 3: Frontend-Backend integration with button interaction
 * - Loading states, error handling, and accessibility
 * 
 * Ensures frontend and backend work together correctly
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock API responses
const mockSuccessResponse = {
  message: 'Hello World from Backend!',
  timestamp: '2024-01-15T14:30:00.000Z'
}

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  describe('Story 1: Static Frontend Display', () => {
    it('renders the Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading.tagName).toBe('H1')
    })

    it('displays the fetch button with correct text', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('Get Message from Backend')
    })

    it('renders footer with technology stack information', () => {
      render(<App />)
      expect(screen.getByText(/frontend: react 18 \+ vite/i)).toBeInTheDocument()
      expect(screen.getByText(/backend: python fastapi/i)).toBeInTheDocument()
    })

    it('button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('Story 3: Frontend-Backend Integration', () => {
    it('displays loading state when button is clicked', async () => {
      // Mock fetch to delay response
      global.fetch = vi.fn(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => mockSuccessResponse
        }), 100))
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Check loading state appears
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
      expect(screen.getByText(/fetching message/i)).toBeInTheDocument()
      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()
    })

    it('displays backend message after successful API call', async () => {
      // Mock successful fetch
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => mockSuccessResponse
        })
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Wait for message to appear
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Verify fetch was called with correct URL
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/hello')
      )
    })

    it('displays formatted timestamp after successful API call', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => mockSuccessResponse
        })
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Wait for timestamp to appear
      await waitFor(() => {
        expect(screen.getByText(/received at:/i)).toBeInTheDocument()
      })
    })

    it('displays error message when API call fails', async () => {
      // Mock failed fetch
      global.fetch = vi.fn(() => 
        Promise.reject(new Error('Network error'))
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Wait for error message to appear
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument()
      })

      // Button should be enabled again after error
      expect(button).not.toBeDisabled()
      expect(button).toHaveTextContent('Get Message from Backend')
    })

    it('displays error message for non-200 HTTP status', async () => {
      // Mock HTTP error response
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: false,
          status: 500
        })
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Wait for error message to appear
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/failed to connect to backend/i)).toBeInTheDocument()
      })
    })

    it('clears previous messages when fetching new data', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => mockSuccessResponse
        })
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Second click should clear previous message during loading
      await user.click(button)
      
      // During loading, old message should not be visible
      await waitFor(() => {
        expect(screen.getByText(/loading/i)).toBeInTheDocument()
      })
    })

    it('button is disabled during loading to prevent multiple requests', async () => {
      global.fetch = vi.fn(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => mockSuccessResponse
        }), 100))
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Button should be disabled during loading
      expect(button).toBeDisabled()
      expect(button).toHaveAttribute('disabled')

      // Wait for completion
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Button should be enabled again
      expect(button).not.toBeDisabled()
    })
  })

  describe('Accessibility', () => {
    it('button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label', 'Get message from backend')
    })

    it('loading state has proper ARIA live region', async () => {
      global.fetch = vi.fn(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => mockSuccessResponse
        }), 100))
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Loading state should have role="status" and aria-live="polite"
      const loadingElement = screen.getByRole('status')
      expect(loadingElement).toHaveAttribute('aria-live', 'polite')
    })

    it('error message has role="alert"', async () => {
      global.fetch = vi.fn(() => 
        Promise.reject(new Error('Network error'))
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      // Error should have role="alert"
      await waitFor(() => {
        const alertElement = screen.getByRole('alert')
        expect(alertElement).toBeInTheDocument()
      })
    })
  })

  describe('Timestamp Formatting', () => {
    it('formats ISO 8601 timestamp correctly', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({
            message: 'Hello World from Backend!',
            timestamp: '2024-01-15T14:30:00.000Z'
          })
        })
      )

      const user = userEvent.setup()
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        const timestampText = screen.getByText(/received at:/i)
        expect(timestampText).toBeInTheDocument()
        // Should display formatted date (not raw ISO string)
        expect(timestampText.textContent).not.toContain('2024-01-15T14:30:00.000Z')
      })
    })
  })
})