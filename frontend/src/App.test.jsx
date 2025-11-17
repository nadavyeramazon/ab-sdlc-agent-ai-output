/**
 * Comprehensive test suite for App component
 * 
 * Tests:
 * - Component rendering
 * - Button functionality
 * - API integration
 * - Loading states
 * - Error handling
 * - Styling and theme
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
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

  describe('Initial Render', () => {
    it('renders Hello World heading correctly', () => {
      render(<App />)
      
      const heading = screen.getByRole('heading', { name: /hello world/i, level: 1 })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveTextContent('Hello World')
    })

    it('renders subtitle with correct text', () => {
      render(<App />)
      
      const subtitle = screen.getByText(/yellow theme fullstack application/i)
      expect(subtitle).toBeInTheDocument()
    })

    it('renders fetch button with correct label', () => {
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('Get Message from Backend')
    })

    it('renders info section with tech stack details', () => {
      render(<App />)
      
      expect(screen.getByText(/frontend: react \+ vite/i)).toBeInTheDocument()
      expect(screen.getByText(/backend: fastapi/i)).toBeInTheDocument()
      expect(screen.getByText(/theme: yellow/i)).toBeInTheDocument()
    })

    it('does not show backend response initially', () => {
      render(<App />)
      
      const backendResponse = screen.queryByText(/backend response:/i)
      expect(backendResponse).not.toBeInTheDocument()
    })
  })

  describe('Button Click and API Call', () => {
    it('shows loading state when button is clicked', async () => {
      // Mock a delayed response
      fetch.mockImplementation(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({
              message: 'Hello World from Backend!',
              timestamp: '2024-01-15T10:30:00.000Z'
            })
          }), 100)
        )
      )

      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(button)

      // Check loading state appears
      await waitFor(() => {
        expect(screen.getByText(/loading\.\.\.?/i)).toBeInTheDocument()
      })

      // Check loading message
      expect(screen.getByText(/fetching data from backend/i)).toBeInTheDocument()

      // Check button is disabled during loading
      expect(button).toBeDisabled()
    })

    it('fetches data from backend on button click', async () => {
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
        expect(fetch).toHaveBeenCalledTimes(1)
      })

      // Verify fetch was called with correct URL
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/hello')
      )
    })

    it('displays backend response correctly', async () => {
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

      // Wait for response to be displayed
      await waitFor(() => {
        expect(screen.getByText(/backend response:/i)).toBeInTheDocument()
      })

      expect(screen.getByText(mockResponse.message)).toBeInTheDocument()
      expect(screen.getByText(/timestamp:/i)).toBeInTheDocument()
    })

    it('formats timestamp correctly in response', async () => {
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

      // Verify timestamp is displayed (format may vary by locale)
      const timestampElement = screen.getByText(/timestamp:/i)
      expect(timestampElement).toBeInTheDocument()
    })
  })

  describe('Error Handling', () => {
    it('displays error message when API call fails', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(button)

      // Wait for error message
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch data from backend/i)).toBeInTheDocument()
    })

    it('displays error message when response is not ok', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(button)

      // Wait for error message
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch data from backend/i)).toBeInTheDocument()
    })

    it('clears previous error when new request is made', async () => {
      // First request fails
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      // Second request succeeds
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      fireEvent.click(button)

      // Error should be cleared
      await waitFor(() => {
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      })
    })
  })

  describe('Loading State', () => {
    it('shows spinner during loading', async () => {
      fetch.mockImplementation(() => 
        new Promise(resolve => 
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({
              message: 'Hello World from Backend!',
              timestamp: '2024-01-15T10:30:00.000Z'
            })
          }), 100)
        )
      )

      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(button)

      // Check spinner appears
      await waitFor(() => {
        const spinner = document.querySelector('.spinner')
        expect(spinner).toBeInTheDocument()
      })
    })

    it('hides loading state after successful response', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000Z'
        })
      })

      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(button)

      // Wait for response
      await waitFor(() => {
        expect(screen.getByText(/backend response:/i)).toBeInTheDocument()
      })

      // Loading should be gone
      expect(screen.queryByText(/fetching data from backend/i)).not.toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('hides loading state after error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      fireEvent.click(button)

      // Wait for error
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })

      // Loading should be gone
      expect(screen.queryByText(/fetching data from backend/i)).not.toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })
  })

  describe('Styling and Theme', () => {
    it('applies yellow theme to main heading', () => {
      render(<App />)
      
      const heading = screen.getByRole('heading', { name: /hello world/i, level: 1 })
      expect(heading).toHaveClass('main-heading')
    })

    it('applies correct classes to fetch button', () => {
      render(<App />)
      
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveClass('fetch-button')
    })

    it('applies correct classes to container', () => {
      render(<App />)
      
      const container = document.querySelector('.container')
      expect(container).toBeInTheDocument()
    })
  })
})
