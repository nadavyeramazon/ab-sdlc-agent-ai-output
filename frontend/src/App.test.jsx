import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockReset()
  })

  describe('Initial Render - Story 1', () => {
    it('displays Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
      expect(heading).toHaveClass('hello-heading')
    })

    it('displays subtitle', () => {
      render(<App />)
      expect(screen.getByText(/green-themed fullstack application/i)).toBeInTheDocument()
    })

    it('displays fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('displays footer with tech stack info', () => {
      render(<App />)
      expect(screen.getByText(/built with react 18 \+ vite \+ fastapi/i)).toBeInTheDocument()
    })

    it('does not display message or error initially', () => {
      render(<App />)
      expect(screen.queryByText(/backend response/i)).not.toBeInTheDocument()
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
    })
  })

  describe('Backend API Integration - Story 3', () => {
    it('fetches and displays message from backend on button click', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      expect(screen.getByText(/hello world from backend!/i)).toBeInTheDocument()
    })

    it('displays loading state while fetching', async () => {
      const user = userEvent.setup()
      
      // Create a promise that won't resolve immediately
      let resolvePromise
      const promise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(promise)

      render(<App />)
      const button = screen.getByRole('button')
      
      await user.click(button)

      // Button should show loading and be disabled
      expect(button).toHaveTextContent(/loading/i)
      expect(button).toBeDisabled()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:00.000000Z' })
      })

      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('displays error message when API call fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
    })

    it('displays error message when network error occurs', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      expect(screen.getByText(/failed to fetch message from backend/i)).toBeInTheDocument()
    })

    it('clears previous error when making new successful request', async () => {
      const user = userEvent.setup()
      
      // First request fails
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument()
      })

      // Second request succeeds
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText(/error/i)).not.toBeInTheDocument()
      })

      expect(screen.getByText(/backend response/i)).toBeInTheDocument()
    })

    it('formats timestamp in localized format', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00.000000Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      // Check that timestamp is displayed (format will vary by locale)
      const messageText = screen.getByText(/hello world from backend!/i).textContent
      expect(messageText).toMatch(/\(at .+\)/)
    })
  })

  describe('Accessibility', () => {
    it('button has proper aria-label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /fetch message from backend/i })
      expect(button).toHaveAttribute('aria-label', 'Fetch message from backend')
    })

    it('message boxes have role="alert"', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T10:30:00.000000Z'
        })
      })

      render(<App />)
      await user.click(screen.getByRole('button'))

      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.length).toBeGreaterThan(0)
      })
    })
  })

  describe('Multiple Requests', () => {
    it('can fetch multiple times successfully', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: new Date().toISOString()
        })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // First click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      // Second click
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText(/backend response/i)).toBeInTheDocument()
      })

      expect(fetch).toHaveBeenCalledTimes(2)
    })
  })
})
