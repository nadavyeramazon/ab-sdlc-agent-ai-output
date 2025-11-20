import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import App from './App'

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
    // Reset fetch mock
    global.fetch = vi.fn()
  })

  describe('Initial Rendering', () => {
    it('should render the title', () => {
      render(<App />)
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument()
    })

    it('should render the button with correct initial text', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('should not display any message, error, or loading state initially', () => {
      render(<App />)
      expect(screen.queryByText(/backend response:/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
    })
  })

  describe('Button Click Interactions', () => {
    it('should be clickable and trigger fetch on click', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledTimes(1)
      })
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    })

    it('should disable button during loading', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Button should be disabled while loading
      await waitFor(() => {
        expect(button).toBeDisabled()
        expect(button).toHaveTextContent(/loading/i)
      })
    })
  })

  describe('Loading States', () => {
    it('should display loading text in button when API call is in progress', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).toHaveTextContent(/loading/i)
        expect(screen.getAllByText(/loading/i).length).toBeGreaterThan(0)
      })
    })

    it('should display loading paragraph when API call is in progress', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Should show loading paragraph
      await waitFor(() => {
        const loadingParagraphs = screen.getAllByText(/loading/i)
        expect(loadingParagraphs.length).toBeGreaterThanOrEqual(2) // Button + paragraph
      })
    })

    it('should clear loading state after API call completes', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(button).toHaveTextContent(/get message from backend/i)
      })
    })
  })

  describe('Error Handling', () => {
    it('should display error message when fetch fails with network error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: network error/i)).toBeInTheDocument()
      })
    })

    it('should display error message when API returns non-OK status', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 500
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: http error! status: 500/i)).toBeInTheDocument()
      })
    })

    it('should display error message for 404 status', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: false,
          status: 404
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: http error! status: 404/i)).toBeInTheDocument()
      })
    })

    it('should clear previous error when new request is made', async () => {
      const user = userEvent.setup()
      // First call fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch: network error/i)).toBeInTheDocument()
      })

      // Second call succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success!' })
        })
      )

      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
        expect(screen.getByText(/success!/i)).toBeInTheDocument()
      })
    })

    it('should re-enable button after error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(button).toHaveTextContent(/get message from backend/i)
      })
    })
  })

  describe('Successful API Responses', () => {
    it('should display backend message on successful API call', async () => {
      const user = userEvent.setup()
      const mockMessage = 'Hello from the backend!'
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: mockMessage })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/backend response:/i)).toBeInTheDocument()
        expect(screen.getByText(mockMessage)).toBeInTheDocument()
      })
    })

    it('should handle response with different message content', async () => {
      const user = userEvent.setup()
      const mockMessage = 'Custom server response'
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: mockMessage })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(mockMessage)).toBeInTheDocument()
      })
    })

    it('should stringify JSON data if message field is not present', async () => {
      const user = userEvent.setup()
      const mockData = { status: 'ok', data: 'test' }
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData)
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(JSON.stringify(mockData))).toBeInTheDocument()
      })
    })

    it('should clear previous message when new request is made', async () => {
      const user = userEvent.setup()
      const firstMessage = 'First message'
      const secondMessage = 'Second message'
      
      // First call
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: firstMessage })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(firstMessage)).toBeInTheDocument()
      })

      // Second call
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: secondMessage })
        })
      )

      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(firstMessage)).not.toBeInTheDocument()
        expect(screen.getByText(secondMessage)).toBeInTheDocument()
      })
    })

    it('should display response section only after successful fetch', async () => {
      const user = userEvent.setup()
      render(<App />)
      
      // Initially no response section
      expect(screen.queryByText(/backend response:/i)).not.toBeInTheDocument()
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message' })
        })
      )

      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)
      
      // After fetch, response section should appear
      await waitFor(() => {
        expect(screen.getByText(/backend response:/i)).toBeInTheDocument()
      })
    })
  })

  describe('State Management', () => {
    it('should clear error and message when starting new request', async () => {
      const user = userEvent.setup()
      
      // First call fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Error')))
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument()
      })

      // Second call succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success' })
        })
      )
      
      await user.click(button)
      
      // During loading, neither error nor old message should be visible
      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
      })
    })

    it('should handle multiple rapid clicks gracefully', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Response' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click multiple times
      await user.click(button)
      await user.click(button)
      await user.click(button)
      
      // Should still work correctly
      await waitFor(() => {
        expect(screen.getByText('Response')).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('should have accessible button with proper role', () => {
      render(<App />)
      // Fixed: Specify which button to query by using the button name
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('should have accessible heading with proper role', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveTextContent(/hello world/i)
    })

    it('should properly disable button during loading for accessibility', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise((resolve) => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test' })
        }), 50))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      
      // Button should be disabled and not clickable
      await waitFor(() => {
        expect(button).toBeDisabled()
      })
    })
  })
})
