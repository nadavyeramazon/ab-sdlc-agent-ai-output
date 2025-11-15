/**
 * Comprehensive test suite for App component.
 * 
 * Tests:
 * - Static content rendering
 * - Button functionality
 * - API integration (existing and new features)
 * - Loading states
 * - Error handling
 * - User interactions
 * - Validation
 * - Greeting feature
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

    it('renders Get Message from Backend button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('Get Message button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('Existing Feature - Get Message from Backend', () => {
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
      expect(screen.getByText(/loading\.\.\.$/i)).toBeInTheDocument()
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

  describe('New Feature - Personalized Greeting', () => {
    it('renders name input field', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      expect(input).toBeInTheDocument()
    })

    it('renders Greet Me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toBeInTheDocument()
    })

    it('input field has correct placeholder', () => {
      render(<App />)
      const input = screen.getByPlaceholderText('Enter your name')
      expect(input).toHaveAttribute('placeholder', 'Enter your name')
    })

    it('input field has accessible label', () => {
      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      expect(input).toBeInTheDocument()
    })

    it('displays validation error when submitting empty name', async () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })
      
      // Verify no API call was made
      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('displays validation error when submitting whitespace-only name', async () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, '   ')
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })
      
      // Verify no API call was made
      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('clears validation error when user starts typing', async () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      // Trigger validation error
      await userEvent.click(button)
      await waitFor(() => {
        expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
      })
      
      // Start typing
      await userEvent.type(input, 'J')
      
      // Validation error should be cleared
      expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
    })

    it('displays loading state when fetching greeting', async () => {
      global.fetch = vi.fn(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({ 
              greeting: 'Hello, Jane! Welcome to our purple-themed app!', 
              timestamp: '2024-01-15T10:30:00Z' 
            })
          }), 100)
        )
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Jane')
      await userEvent.click(button)
      
      // Check loading state - should find only one "Loading..." (from Greet Me button)
      const loadingButtons = screen.getAllByText(/loading\.\.\.$/i)
      // The greet button should show loading
      expect(button).toBeDisabled()
    })

    it('fetches and displays personalized greeting on success', async () => {
      const mockResponse = {
        greeting: 'Hello, Jane! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T10:30:00Z'
      }

      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => mockResponse,
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Jane')
      await userEvent.click(button)
      
      // Wait for greeting to appear
      await waitFor(() => {
        expect(screen.getByText(mockResponse.greeting)).toBeInTheDocument()
      })

      // Verify fetch was called with correct URL and method
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/greet',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: 'Jane' })
        })
      )
    })

    it('displays error message when greeting fetch fails', async () => {
      global.fetch = vi.fn(() =>
        Promise.reject(new Error('Network error'))
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Test')
      await userEvent.click(button)
      
      // Wait for error message to appear
      await waitFor(() => {
        expect(screen.getByText(/unable to connect\. please try again\./i)).toBeInTheDocument()
      })
    })

    it('trims whitespace from name before sending', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Alice! Welcome to our purple-themed app!', 
            timestamp: '2024-01-15T10:30:00Z' 
          }),
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, '  Alice  ')
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            body: JSON.stringify({ name: 'Alice' })
          })
        )
      })
    })

    it('allows submitting with Enter key', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Bob! Welcome to our purple-themed app!', 
            timestamp: '2024-01-15T10:30:00Z' 
          }),
        })
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/enter your name/i)
      
      await userEvent.type(input, 'Bob{Enter}')
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            method: 'POST'
          })
        )
      })
    })
  })

  describe('Concurrent Feature Usage', () => {
    it('both features work independently', async () => {
      global.fetch = vi.fn((url) => {
        if (url.includes('/api/hello')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-15T10:30:00Z' }),
          })
        } else if (url.includes('/api/greet')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ greeting: 'Hello, Test! Welcome to our purple-themed app!', timestamp: '2024-01-15T10:30:00Z' }),
          })
        }
      })

      render(<App />)
      
      // Use old feature first
      const helloButton = screen.getByRole('button', { name: /get message from backend/i })
      await userEvent.click(helloButton)
      
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
      
      // Use new feature
      const input = screen.getByPlaceholderText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Test')
      await userEvent.click(greetButton)
      
      await waitFor(() => {
        expect(screen.getByText('Hello, Test! Welcome to our purple-themed app!')).toBeInTheDocument()
      })
      
      // Both messages should be visible
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      expect(screen.getByText('Hello, Test! Welcome to our purple-themed app!')).toBeInTheDocument()
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