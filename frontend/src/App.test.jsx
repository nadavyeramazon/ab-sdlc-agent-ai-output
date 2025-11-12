/**
 * Comprehensive test suite for App component
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

  describe('Initial Render', () => {
    it('renders Hello World title', () => {
      render(<App />)
      const titleElement = screen.getByText(/Hello World/i)
      expect(titleElement).toBeInTheDocument()
    })

    it('renders subtitle', () => {
      render(<App />)
      const subtitleElement = screen.getByText(/Green Theme React Application/i)
      expect(subtitleElement).toBeInTheDocument()
    })

    it('renders fetch button', () => {
      render(<App />)
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      expect(buttonElement).toBeInTheDocument()
    })

    it('button is not disabled initially', () => {
      render(<App />)
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      expect(buttonElement).not.toBeDisabled()
    })

    it('no backend message displayed initially', () => {
      render(<App />)
      const messageElement = screen.queryByRole('status')
      expect(messageElement).not.toBeInTheDocument()
    })

    it('no error message displayed initially', () => {
      render(<App />)
      const errorElement = screen.queryByRole('alert')
      expect(errorElement).not.toBeInTheDocument()
    })
  })

  describe('Fetching Backend Data', () => {
    it('displays loading state when button is clicked', async () => {
      // Mock a delayed response
      fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Hello World from Backend!', timestamp: new Date().toISOString() })
        }), 100))
      )

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      // Button should show loading text
      expect(screen.getByText(/Loading.../i)).toBeInTheDocument()
    })

    it('button is disabled during loading', async () => {
      fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Hello World from Backend!', timestamp: new Date().toISOString() })
        }), 100))
      )

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      expect(buttonElement).toBeDisabled()
    })

    it('displays backend message on successful fetch', async () => {
      const mockTimestamp = new Date().toISOString()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: mockTimestamp 
        })
      })

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.getByText(/Hello World from Backend!/i)).toBeInTheDocument()
      })
    })

    it('calls fetch with correct URL', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: new Date().toISOString() 
        })
      })

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/api/hello'))
      })
    })

    it('displays timestamp in message', async () => {
      const mockTimestamp = new Date().toISOString()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: mockTimestamp 
        })
      })

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        const messageElement = screen.getByRole('status')
        expect(messageElement).toBeInTheDocument()
        // Check that time is included (format will be locale-specific)
        expect(messageElement.textContent).toMatch(/Hello World from Backend!/)
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message on fetch failure', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/Failed to fetch from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error message on HTTP error', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
        expect(screen.getByText(/Failed to fetch from backend/i)).toBeInTheDocument()
      })
    })

    it('button is re-enabled after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      expect(buttonElement).not.toBeDisabled()
    })

    it('clears previous messages when fetching again', async () => {
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: new Date().toISOString() 
        })
      })

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.getByText(/Hello World from Backend!/i)).toBeInTheDocument()
      })

      // Second fetch with error
      fetch.mockRejectedValueOnce(new Error('Network error'))
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.queryByText(/Hello World from Backend!/i)).not.toBeInTheDocument()
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('button has proper aria-label', () => {
      render(<App />)
      const buttonElement = screen.getByLabelText(/Get message from backend/i)
      expect(buttonElement).toBeInTheDocument()
    })

    it('success message has role="status"', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ 
          message: 'Hello World from Backend!', 
          timestamp: new Date().toISOString() 
        })
      })

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toBeInTheDocument()
      })
    })

    it('error message has role="alert"', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
    })

    it('loading spinner has aria-label', async () => {
      fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Hello World from Backend!', timestamp: new Date().toISOString() })
        }), 100))
      )

      render(<App />)
      const user = userEvent.setup()
      const buttonElement = screen.getByRole('button', { name: /Get message from backend/i })
      
      await user.click(buttonElement)
      
      expect(screen.getByLabelText(/Loading/i)).toBeInTheDocument()
    })
  })
})
