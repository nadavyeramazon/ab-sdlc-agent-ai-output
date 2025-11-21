import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'
import { createMockResponse, setupFetchMock, resetFetchMock } from './test/utils'

describe('App Component', () => {
  let fetchMock

  beforeEach(() => {
    fetchMock = setupFetchMock()
  })

  afterEach(() => {
    resetFetchMock()
  })

  describe('Initial Rendering', () => {
    it('should render the app with heading', () => {
      render(<App />)
      expect(screen.getByText('Hello World')).toBeInTheDocument()
    })

    it('should render the fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('should have button enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('should not display any messages initially', () => {
      render(<App />)
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
    })
  })

  describe('User Interactions', () => {
    it('should call fetchMessage when button is clicked', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce(
        createMockResponse({ message: 'Hello from backend', timestamp: '2024-01-01' })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(fetchMock).toHaveBeenCalledTimes(1)
      })
      expect(fetchMock).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    })

    it('should disable button during loading', async () => {
      const user = userEvent.setup()
      fetchMock.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve(
          createMockResponse({ message: 'Hello', timestamp: '2024-01-01' })
        ), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Button should be disabled while loading
      expect(button).toBeDisabled()
      
      // Wait for loading to complete
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Loading State', () => {
    it('should display loading message when fetching data', async () => {
      const user = userEvent.setup()
      fetchMock.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve(
          createMockResponse({ message: 'Hello', timestamp: '2024-01-01' })
        ), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Loading message should appear
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
      
      // Wait for loading to complete
      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })

    it('should hide loading message after successful fetch', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce(
        createMockResponse({ message: 'Hello from backend', timestamp: '2024-01-01' })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })

    it('should hide loading message after failed fetch', async () => {
      const user = userEvent.setup()
      fetchMock.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Successful API Response', () => {
    it('should display message from backend on successful fetch', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Hello from backend', timestamp: '2024-01-01T12:00:00Z' }
      fetchMock.mockResolvedValueOnce(createMockResponse(mockData))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(`${mockData.message} (${mockData.timestamp})`)).toBeInTheDocument()
      })
    })

    it('should display formatted message with timestamp', async () => {
      const user = userEvent.setup()
      const mockData = { message: 'Test message', timestamp: '2024-12-25T10:30:00Z' }
      fetchMock.mockResolvedValueOnce(createMockResponse(mockData))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        const messageElement = screen.getByText(/test message/i)
        expect(messageElement).toHaveTextContent('Test message (2024-12-25T10:30:00Z)')
        expect(messageElement).toHaveClass('message')
      })
    })

    it('should clear previous error when fetch succeeds', async () => {
      const user = userEvent.setup()
      
      // First request fails
      fetchMock.mockRejectedValueOnce(new Error('Network error'))
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument()
      })

      // Second request succeeds
      fetchMock.mockResolvedValueOnce(
        createMockResponse({ message: 'Success', timestamp: '2024-01-01' })
      )
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
        expect(screen.getByText(/success/i)).toBeInTheDocument()
      })
    })
  })

  describe('Error Handling - Network Errors', () => {
    it('should display error message on network failure', async () => {
      const user = userEvent.setup()
      fetchMock.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message: network error/i)).toBeInTheDocument()
      })
    })

    it('should display error with correct CSS class', async () => {
      const user = userEvent.setup()
      fetchMock.mockRejectedValueOnce(new Error('Connection refused'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        const errorElement = screen.getByText(/failed to fetch/i)
        expect(errorElement).toHaveClass('error')
      })
    })

    it('should handle fetch timeout errors', async () => {
      const user = userEvent.setup()
      fetchMock.mockRejectedValueOnce(new Error('Request timeout'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message: request timeout/i)).toBeInTheDocument()
      })
    })
  })

  describe('Error Handling - HTTP Errors', () => {
    it('should display error message on 404 response', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce(
        createMockResponse({}, { ok: false, status: 404 })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message: http error! status: 404/i)).toBeInTheDocument()
      })
    })

    it('should display error message on 500 response', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce(
        createMockResponse({}, { ok: false, status: 500 })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message: http error! status: 500/i)).toBeInTheDocument()
      })
    })

    it('should display error message on 403 response', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce(
        createMockResponse({}, { ok: false, status: 403 })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message: http error! status: 403/i)).toBeInTheDocument()
      })
    })
  })

  describe('State Management', () => {
    it('should clear previous message when starting new fetch', async () => {
      const user = userEvent.setup()
      
      // First successful fetch
      fetchMock.mockResolvedValueOnce(
        createMockResponse({ message: 'First message', timestamp: '2024-01-01' })
      )
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/first message/i)).toBeInTheDocument()
      })

      // Second fetch starts
      fetchMock.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve(
          createMockResponse({ message: 'Second message', timestamp: '2024-01-02' })
        ), 100))
      )
      await user.click(button)

      // Old message should be cleared during loading
      await waitFor(() => {
        expect(screen.queryByText(/first message/i)).not.toBeInTheDocument()
        expect(screen.getByText(/loading/i)).toBeInTheDocument()
      })
    })

    it('should clear previous error when starting new fetch', async () => {
      const user = userEvent.setup()
      
      // First request fails
      fetchMock.mockRejectedValueOnce(new Error('First error'))
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message: first error/i)).toBeInTheDocument()
      })

      // Second request starts
      fetchMock.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve(
          createMockResponse({ message: 'Success', timestamp: '2024-01-01' })
        ), 100))
      )
      await user.click(button)

      // Old error should be cleared during loading
      await waitFor(() => {
        expect(screen.queryByText(/first error/i)).not.toBeInTheDocument()
      })
    })
  })

  describe('Edge Cases', () => {
    it('should handle rapid consecutive clicks gracefully', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValue(
        createMockResponse({ message: 'Response', timestamp: '2024-01-01' })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click button multiple times rapidly
      await user.click(button)
      await user.click(button)
      await user.click(button)

      // Should still work correctly
      await waitFor(() => {
        expect(screen.getByText(/response/i)).toBeInTheDocument()
      })
    })

    it('should handle empty message from backend', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce(
        createMockResponse({ message: '', timestamp: '2024-01-01' })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('(2024-01-01)')).toBeInTheDocument()
      })
    })

    it('should handle missing timestamp in response', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce(
        createMockResponse({ message: 'Hello' })
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        // Use getAllByText to handle multiple elements with "hello" text (heading + message)
        const elements = screen.getAllByText(/hello/i)
        // Verify the message element exists (second occurrence after the heading)
        expect(elements.length).toBeGreaterThan(1)
        // Check that at least one has the message class
        const messageElement = screen.getByText('Hello (undefined)')
        expect(messageElement).toHaveClass('message')
      })
    })

    it('should handle JSON parse errors gracefully', async () => {
      const user = userEvent.setup()
      fetchMock.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => { throw new Error('Invalid JSON') }
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message/i)).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('should have accessible button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('should have proper heading hierarchy', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toHaveTextContent('Hello World')
    })

    it('should communicate loading state to screen readers', async () => {
      const user = userEvent.setup()
      fetchMock.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve(
          createMockResponse({ message: 'Hello', timestamp: '2024-01-01' })
        ), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Loading message is visible to screen readers
      const loadingElement = screen.getByText(/loading/i)
      expect(loadingElement).toBeInTheDocument()
      
      // Wait for loading to complete
      await waitFor(() => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
      })
    })
  })
})
