/**
 * Comprehensive tests for React Frontend
 * 
 * Tests component rendering, user interactions, API integration,
 * loading states, and error handling.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    vi.resetAllMocks()
  })

  describe('Initial Render', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
    })

    it('renders subtitle text', () => {
      render(<App />)
      expect(screen.getByText(/green theme react application/i)).toBeInTheDocument()
    })

    it('renders fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('does not show backend message initially', () => {
      render(<App />)
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
    })

    it('does not show error message initially', () => {
      render(<App />)
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    })
  })

  describe('Button Click Behavior', () => {
    it('shows loading state when button is clicked', async () => {
      // Mock fetch to delay response
      global.fetch = vi.fn(() => new Promise(() => {}))
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
      expect(button).toBeDisabled()
    })

    it('button is clickable', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      expect(global.fetch).toHaveBeenCalled()
    })
  })

  describe('Successful API Response', () => {
    it('displays backend message on successful fetch', async () => {
      const mockTimestamp = '2024-01-01T12:00:00.000Z'
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!', 
            timestamp: mockTimestamp 
          })
        })
      )
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toBeInTheDocument()
      })
      
      expect(screen.getByRole('status')).toHaveTextContent(/hello world from backend/i)
    })

    it('calls correct API endpoint', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/hello')
        )
      })
    })

    it('button returns to normal state after successful fetch', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toBeInTheDocument()
      })
      
      expect(button).not.toBeDisabled()
      expect(button).toHaveTextContent(/get message from backend/i)
    })
  })

  describe('Error Handling', () => {
    it('displays error message on network failure', async () => {
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
      
      expect(screen.getByRole('alert')).toHaveTextContent(/failed to fetch/i)
    })

    it('displays error message on HTTP error', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: false,
          status: 500
        })
      )
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
      
      expect(screen.getByRole('alert')).toHaveTextContent(/http error/i)
    })

    it('button returns to normal state after error', async () => {
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
      
      expect(button).not.toBeDisabled()
      expect(button).toHaveTextContent(/get message from backend/i)
    })

    it('clears previous error on new fetch', async () => {
      // First fetch fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
      
      // Second fetch succeeds
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      })
    })
  })

  describe('Multiple Fetches', () => {
    it('can fetch multiple times', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First click
      await userEvent.click(button)
      await waitFor(() => {
        expect(screen.getByRole('status')).toBeInTheDocument()
      })
      
      // Second click
      await userEvent.click(button)
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledTimes(2)
      })
    })
  })

  describe('Accessibility', () => {
    it('button has accessible label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label')
    })

    it('success message has status role', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            message: 'Hello World from Backend!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toBeInTheDocument()
      })
    })

    it('error message has alert role', async () => {
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
    })
  })
})
