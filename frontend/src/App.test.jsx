import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

describe('App Component', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    vi.clearAllMocks()
    // Reset fetch mock
    global.fetch = vi.fn()
  })

  describe('Rendering Tests', () => {
    it('should render without crashing', () => {
      render(<App />)
      expect(screen.getByRole('heading')).toBeInTheDocument()
    })

    it('should display "Hello World" heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveTextContent('Hello World')
    })

    it('should display "Get Message from Backend" button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('should have button initially enabled', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })
  })

  describe('Initial State Tests', () => {
    it('should not show loading state initially', () => {
      render(<App />)
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
    })

    it('should not show error message initially', () => {
      render(<App />)
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
    })

    it('should not show message content initially', () => {
      render(<App />)
      expect(screen.queryByText(/message:/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/timestamp:/i)).not.toBeInTheDocument()
    })
  })

  describe('User Interaction Tests', () => {
    it('should call fetch when button is clicked', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message', timestamp: '2024-01-01' })
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      expect(global.fetch).toHaveBeenCalledTimes(1)
      expect(global.fetch).toHaveBeenCalledWith('/api/hello')
    })

    it('should show loading state when button is clicked', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message', timestamp: '2024-01-01' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Loading should appear immediately
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
    })

    it('should disable button during loading', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Test message', timestamp: '2024-01-01' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      expect(button).toBeDisabled()
    })
  })

  describe('Successful API Call Tests', () => {
    it('should display message from backend on successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Hello from backend!', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(screen.getByText(/hello from backend!/i)).toBeInTheDocument()
      })
    })

    it('should display timestamp from backend on successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(screen.getByText(/2024-01-01T12:00:00Z/i)).toBeInTheDocument()
      })
    })

    it('should hide loading state after successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })

    it('should re-enable button after successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01T12:00:00Z' }
      
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
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Error Handling Tests', () => {
    it('should show error message when fetch fails with network error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error: network error/i)).toBeInTheDocument()
      })
    })

    it('should show error message for non-OK HTTP response', async () => {
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
        expect(screen.getByText(/error: http error! status: 500/i)).toBeInTheDocument()
      })
    })

    it('should show error message for 404 response', async () => {
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
        expect(screen.getByText(/error: http error! status: 404/i)).toBeInTheDocument()
      })
    })

    it('should hide loading state after error', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
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
      })
    })

    it('should not show message content when error occurs', async () => {
      const user = userEvent.setup()
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error: network error/i)).toBeInTheDocument()
      })

      expect(screen.queryByText(/message:/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/timestamp:/i)).not.toBeInTheDocument()
    })
  })

  describe('State Management Tests', () => {
    it('should clear previous error when making a new request', async () => {
      const user = userEvent.setup()
      
      // First request fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/error: network error/i)).toBeInTheDocument()
      })

      // Second request succeeds
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Success!', timestamp: '2024-01-01' })
        })
      )
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/error:/i)).not.toBeInTheDocument()
        expect(screen.getByText(/success!/i)).toBeInTheDocument()
      })
    })

    it('should update message when making multiple successful requests', async () => {
      const user = userEvent.setup()
      
      // First request
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'First message', timestamp: '2024-01-01' })
        })
      )
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/first message/i)).toBeInTheDocument()
      })

      // Second request
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ message: 'Second message', timestamp: '2024-01-02' })
        })
      )
      
      await user.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText(/first message/i)).not.toBeInTheDocument()
        expect(screen.getByText(/second message/i)).toBeInTheDocument()
      })
    })

    it('should handle rapid button clicks gracefully', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-01-01' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData)
        })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click multiple times
      await user.click(button)
      
      // Button should be disabled, preventing additional clicks
      expect(button).toBeDisabled()
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Integration Tests', () => {
    it('should complete full success flow from initial render to displaying data', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Integration test message', timestamp: '2024-01-01T10:30:00Z' }
      
      global.fetch = vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData)
        })
      )

      // Initial render
      render(<App />)
      expect(screen.getByRole('heading', { name: /hello world/i })).toBeInTheDocument()
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      
      // Click button
      await user.click(button)
      
      // Check loading state
      expect(button).toBeDisabled()
      
      // Wait for data
      await waitFor(() => {
        expect(screen.getByText(/integration test message/i)).toBeInTheDocument()
        expect(screen.getByText(/2024-01-01T10:30:00Z/i)).toBeInTheDocument()
      })
      
      // Verify final state
      expect(button).not.toBeDisabled()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
    })

    it('should complete full error flow from initial render to displaying error', async () => {
      const user = userEvent.setup()
      
      global.fetch = vi.fn(() => Promise.reject(new Error('Connection timeout')))

      // Initial render
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click button
      await user.click(button)
      
      // Wait for error
      await waitFor(() => {
        expect(screen.getByText(/error: connection timeout/i)).toBeInTheDocument()
      })
      
      // Verify final state
      expect(button).not.toBeDisabled()
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/message:/i)).not.toBeInTheDocument()
    })
  })
})
