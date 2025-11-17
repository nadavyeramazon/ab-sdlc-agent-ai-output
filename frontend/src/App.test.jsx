/**
 * Comprehensive tests for App component
 * 
 * Tests cover:
 * - Component rendering
 * - User interactions
 * - API integration
 * - Error handling
 * - Loading states
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
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

  describe('Initial Render', () => {
    it('renders Hello World heading', () => {
      render(<App />)
      const heading = screen.getByRole('heading', { name: /hello world/i })
      expect(heading).toBeInTheDocument()
    })

    it('renders subtitle text', () => {
      render(<App />)
      const subtitle = screen.getByText(/green-themed react frontend/i)
      expect(subtitle).toBeInTheDocument()
    })

    it('renders fetch button with correct label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('button is enabled initially', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).not.toBeDisabled()
    })

    it('does not show backend message initially', () => {
      render(<App />)
      const message = screen.queryByText(/hello world from backend/i)
      expect(message).not.toBeInTheDocument()
    })
  })

  describe('Successful API Call', () => {
    it('fetches and displays backend message on button click', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })
    })

    it('displays timestamp from backend', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/timestamp: 2024-01-15T10:30:00Z/i)).toBeInTheDocument()
      })
    })

    it('calls correct API endpoint', async () => {
      const user = userEvent.setup()
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T10:30:00Z'
      }

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
      })
    })
  })

  describe('Loading State', () => {
    it('shows loading text while fetching', async () => {
      const user = userEvent.setup()
      
      // Create a promise that we control
      let resolvePromise
      const promise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(promise)

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Should show loading text
      expect(screen.getByText('Loading...')).toBeInTheDocument()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:00Z' })
      })

      // Wait for loading to disappear
      await waitFor(() => {
        expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
      })
    })

    it('disables button while loading', async () => {
      const user = userEvent.setup()
      
      let resolvePromise
      const promise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(promise)

      render(<App />)
      const button = screen.getByRole('button')
      
      await user.click(button)

      // Button should be disabled
      expect(button).toBeDisabled()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:00Z' })
      })

      // Wait for button to be enabled again
      await waitFor(() => {
        expect(button).not.toBeDisabled()
      })
    })

    it('changes button text to Loading... during fetch', async () => {
      const user = userEvent.setup()
      
      let resolvePromise
      const promise = new Promise((resolve) => {
        resolvePromise = resolve
      })

      fetch.mockReturnValueOnce(promise)

      render(<App />)
      let button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      // Button text should change
      button = screen.getByRole('button', { name: /loading/i })
      expect(button).toBeInTheDocument()

      // Resolve the promise
      resolvePromise({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-15T10:30:00Z' })
      })

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /get message from backend/i })).toBeInTheDocument()
      })
    })
  })

  describe('Error Handling', () => {
    it('displays error message when fetch fails', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message/i)).toBeInTheDocument()
      })
    })

    it('displays error message for non-OK response', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/failed to fetch message/i)).toBeInTheDocument()
      })
    })

    it('includes helpful message about backend in error', async () => {
      const user = userEvent.setup()
      
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText(/make sure the backend is running on port 8000/i)).toBeInTheDocument()
      })
    })

    it('clears previous message when new fetch starts', async () => {
      const user = userEvent.setup()
      
      // First successful fetch
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'First message', timestamp: '2024-01-15T10:30:00Z' })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.getByText('First message')).toBeInTheDocument()
      })

      // Second fetch that fails
      fetch.mockRejectedValueOnce(new Error('Network error'))
      
      await user.click(button)

      await waitFor(() => {
        expect(screen.queryByText('First message')).not.toBeInTheDocument()
        expect(screen.getByText(/failed to fetch message/i)).toBeInTheDocument()
      })
    })
  })

  describe('Multiple Clicks', () => {
    it('handles multiple successful fetches', async () => {
      const user = userEvent.setup()
      
      fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-15T10:30:00Z' })
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      // Click multiple times
      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      await user.click(button)
      await waitFor(() => {
        expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
      })

      expect(fetch).toHaveBeenCalledTimes(2)
    })
  })
})
