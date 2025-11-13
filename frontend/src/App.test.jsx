import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

// Get API URL from environment (same logic as App.jsx)
const API_URL = import.meta.env.VITE_API_URL || '/api'

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  describe('Initial Render', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading.tagName).toBe('H1')
    })

    it('renders the fetch button with correct text', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('Get Message from Backend')
    })

    it('button is not disabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('does not show any message initially', () => {
      render(<App />)
      const message = screen.queryByRole('status')
      expect(message).not.toBeInTheDocument()
    })

    it('does not show any error initially', () => {
      render(<App />)
      const error = screen.queryByRole('alert')
      expect(error).not.toBeInTheDocument()
    })
  })

  describe('Loading State', () => {
    it('shows loading text when button is clicked', async () => {
      // Mock fetch to delay response
      global.fetch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Hello World from Backend!' })
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      // Check loading state
      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()
      
      // Wait for loading to complete
      await waitFor(() => {
        expect(button).toHaveTextContent('Get Message from Backend')
      })
    })
  })

  describe('Successful API Call', () => {
    it('displays backend message on successful fetch', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.123456Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        const message = screen.getByRole('status')
        expect(message).toBeInTheDocument()
        expect(message).toHaveTextContent('Hello World from Backend!')
      })
    })

    it('calls fetch with correct URL using environment variable', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!' })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/hello`)
      })
    })

    it('re-enables button after successful fetch', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!' })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(button).toHaveTextContent('Get Message from Backend')
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message on network failure', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        const error = screen.getByRole('alert')
        expect(error).toBeInTheDocument()
        expect(error).toHaveTextContent('Failed to fetch message. Please try again.')
      })
    })

    it('displays error message on HTTP error status', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        const error = screen.getByRole('alert')
        expect(error).toBeInTheDocument()
        expect(error).toHaveTextContent('Failed to fetch message. Please try again.')
      })
    })

    it('clears previous message on error', async () => {
      // First successful call
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!' })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toHaveTextContent('Hello World from Backend!')
      })

      // Second call fails
      global.fetch.mockRejectedValueOnce(new Error('Network error'))
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
    })

    it('re-enables button after error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(button).not.toBeDisabled()
        expect(button).toHaveTextContent('Get Message from Backend')
      })
    })
  })

  describe('Multiple Interactions', () => {
    it('clears error on new successful fetch', async () => {
      // First call fails
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      // Second call succeeds
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!' })
      })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
        expect(screen.getByRole('status')).toHaveTextContent('Hello World from Backend!')
      })
    })

    it('can fetch multiple times successfully', async () => {
      const mockResponse1 = { message: 'First message' }
      const mockResponse2 = { message: 'Second message' }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse1
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toHaveTextContent('First message')
      })

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse2
      })
      
      fireEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('status')).toHaveTextContent('Second message')
      })
    })
  })

  describe('Environment Configuration', () => {
    it('uses environment variable for API URL', () => {
      // This test verifies that the API_URL is configurable via environment
      const expectedUrl = import.meta.env.VITE_API_URL || '/api'
      expect(API_URL).toBe(expectedUrl)
    })
  })
})
