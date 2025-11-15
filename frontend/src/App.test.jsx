/**
 * Comprehensive test suite for App component.
 * Tests UI rendering, user interactions, API integration, and error handling.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockReset()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial Rendering', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i, level: 1 })
      expect(heading).toBeInTheDocument()
    })

    it('renders subtitle', () => {
      render(<App />)
      const subtitle = screen.getByText(/green theme fullstack application/i)
      expect(subtitle).toBeInTheDocument()
    })

    it('renders fetch button with correct text', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('Get Message from Backend')
    })

    it('renders footer', () => {
      render(<App />)
      const footer = screen.getByText(/powered by react \+ fastapi/i)
      expect(footer).toBeInTheDocument()
    })

    it('button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('no backend message displayed initially', () => {
      render(<App />)
      const responseHeading = screen.queryByText(/response from backend/i)
      expect(responseHeading).not.toBeInTheDocument()
    })
  })

  describe('Button Click and Loading State', () => {
    it('shows loading state when button is clicked', async () => {
      // Mock a delayed response with longer delay to ensure loading state is visible
      fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test message', timestamp: new Date().toISOString() })
        }), 500))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      // Check loading state appears - look for the button text change first
      await waitFor(() => {
        const loadingButton = screen.getByRole('button', { name: /loading/i })
        expect(loadingButton).toBeInTheDocument()
      }, { timeout: 1000 })
      
      // Also check the loading paragraph
      expect(screen.getByText('Loading...')).toBeInTheDocument()
    })

    it('button is disabled during loading', async () => {
      fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test message', timestamp: new Date().toISOString() })
        }), 500))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(button).toBeDisabled()
      })
    })

    it('displays spinner during loading', async () => {
      fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test message', timestamp: new Date().toISOString() })
        }), 500))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        const spinner = document.querySelector('.spinner')
        expect(spinner).toBeInTheDocument()
      })
    })
  })

  describe('Successful API Response', () => {
    it('displays backend message on successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/response from backend/i)).toBeInTheDocument()
      })
      
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
    })

    it('displays formatted timestamp', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/timestamp:/i)).toBeInTheDocument()
      })
    })

    it('hides loading state after successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
      
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
    })

    it('re-enables button after successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message on fetch failure', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch data from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error on non-OK HTTP response', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch data from backend/i)).toBeInTheDocument()
      })
    })

    it('hides loading state after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText(/failed to fetch data from backend/i)).toBeInTheDocument()
      })
      
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
    })

    it('re-enables button after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('clears previous message on error', async () => {
      // First successful call
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!', timestamp: new Date().toISOString() })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      // Second call with error
      fetch.mockRejectedValueOnce(new Error('Network error'))
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByText('Hello World from Backend!')).not.toBeInTheDocument()
      })
    })
  })

  describe('API Call Details', () => {
    it('calls correct API endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: new Date().toISOString() })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
      })
    })

    it('makes GET request', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: new Date().toISOString() })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledTimes(1)
      })
    })
  })

  describe('Accessibility', () => {
    it('button has aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label')
    })

    it('loading state has role status', async () => {
      fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test', timestamp: new Date().toISOString() })
        }), 500))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        const loadingElement = screen.getByRole('status', { name: /loading/i })
        expect(loadingElement).toBeInTheDocument()
      })
    })

    it('error message has role alert', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        const errorElement = screen.getByRole('alert')
        expect(errorElement).toBeInTheDocument()
      })
    })
  })
})
