/**
 * Comprehensive tests for React Frontend
 * 
 * Tests component rendering, user interactions, API integration,
 * loading states, error handling for both existing and new features.
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
      expect(screen.getByText(/purple theme react application/i)).toBeInTheDocument()
    })

    it('renders existing fetch button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('renders name input field', () => {
      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      expect(input).toBeInTheDocument()
      expect(input).toHaveAttribute('type', 'text')
      expect(input).toHaveAttribute('placeholder', 'Your name')
    })

    it('renders greet me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toBeInTheDocument()
      expect(button).not.toBeDisabled()
    })

    it('does not show any messages initially', () => {
      render(<App />)
      expect(screen.queryAllByRole('status')).toHaveLength(0)
      expect(screen.queryAllByRole('alert')).toHaveLength(0)
    })
  })

  describe('User Greet Feature - Input Behavior', () => {
    it('allows typing in name input', async () => {
      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      
      await userEvent.type(input, 'Alice')
      
      expect(input).toHaveValue('Alice')
    })

    it('shows validation error when greet button clicked with empty input', async () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
      expect(screen.getByRole('alert')).toHaveTextContent(/please enter your name/i)
    })

    it('shows validation error when greet button clicked with whitespace-only input', async () => {
      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, '   ')
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument()
      })
      expect(screen.getByRole('alert')).toHaveTextContent(/please enter your name/i)
    })

    it('allows submitting with Enter key', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Alice! Welcome to our purple-themed app!', 
            timestamp: new Date().toISOString() 
          })
        })
      )

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      
      await userEvent.type(input, 'Alice{Enter}')
      
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/greet'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: 'Alice' })
        })
      )
    })
  })

  describe('User Greet Feature - Successful Greeting', () => {
    it('displays personalized greeting on successful API call', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Alice! Welcome to our purple-themed app!', 
            timestamp: '2024-01-01T12:00:00.000Z' 
          })
        })
      )

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Alice')
      await userEvent.click(button)
      
      await waitFor(() => {
        const statuses = screen.getAllByRole('status')
        expect(statuses.some(status => 
          status.textContent.includes('Hello, Alice')
        )).toBe(true)
      })
    })

    it('calls correct API endpoint with POST method', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Bob! Welcome to our purple-themed app!', 
            timestamp: new Date().toISOString() 
          })
        })
      )

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Bob')
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/greet'),
          expect.objectContaining({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: 'Bob' })
          })
        )
      })
    })

    it('clears input field after successful greeting', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Charlie! Welcome to our purple-themed app!', 
            timestamp: new Date().toISOString() 
          })
        })
      )

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Charlie')
      await userEvent.click(button)
      
      await waitFor(() => {
        const statuses = screen.getAllByRole('status')
        expect(statuses.some(status => 
          status.textContent.includes('Hello, Charlie')
        )).toBe(true)
      })
      
      expect(input).toHaveValue('')
    })

    it('shows loading state during API call', async () => {
      global.fetch = vi.fn(() => new Promise(() => {}))

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Alice')
      await userEvent.click(button)
      
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
      expect(button).toBeDisabled()
      expect(input).toBeDisabled()
    })

    it('button returns to normal state after successful greeting', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, David! Welcome to our purple-themed app!', 
            timestamp: new Date().toISOString() 
          })
        })
      )

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'David')
      await userEvent.click(button)
      
      await waitFor(() => {
        const statuses = screen.getAllByRole('status')
        expect(statuses.some(status => 
          status.textContent.includes('Hello, David')
        )).toBe(true)
      })
      
      expect(button).not.toBeDisabled()
      expect(input).not.toBeDisabled()
    })
  })

  describe('User Greet Feature - Error Handling', () => {
    it('displays error message on network failure', async () => {
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Alice')
      await userEvent.click(button)
      
      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.some(alert => 
          alert.textContent.includes('Failed to get greeting')
        )).toBe(true)
      })
    })

    it('displays error message on HTTP error', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: false,
          status: 400,
          json: async () => ({ detail: 'Name cannot be empty' })
        })
      )

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Alice')
      await userEvent.click(button)
      
      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.some(alert => 
          alert.textContent.includes('Failed to get greeting')
        )).toBe(true)
      })
    })

    it('clears error on new successful fetch', async () => {
      // First fetch fails
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))

      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Alice')
      await userEvent.click(button)
      
      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.some(alert => 
          alert.textContent.includes('Failed to get greeting')
        )).toBe(true)
      })

      // Second fetch succeeds
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Bob! Welcome to our purple-themed app!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      await userEvent.type(input, 'Bob')
      await userEvent.click(button)
      
      await waitFor(() => {
        const statuses = screen.getAllByRole('status')
        expect(statuses.some(status => 
          status.textContent.includes('Hello, Bob')
        )).toBe(true)
      })
      
      // Error should be cleared
      const alerts = screen.queryAllByRole('alert')
      expect(alerts.every(alert => 
        !alert.textContent.includes('Failed to get greeting')
      )).toBe(true)
    })
  })

  describe('Existing Feature - Backend Message Button', () => {
    it('shows loading state when button is clicked', async () => {
      global.fetch = vi.fn(() => new Promise(() => {}))
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
      expect(button).toBeDisabled()
    })

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
        const statuses = screen.getAllByRole('status')
        expect(statuses.some(status => 
          status.textContent.includes('Hello World from Backend')
        )).toBe(true)
      })
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

    it('displays error message on network failure', async () => {
      global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
      
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        const alerts = screen.getAllByRole('alert')
        expect(alerts.some(alert => 
          alert.textContent.includes('Failed to fetch')
        )).toBe(true)
      })
    })
  })

  describe('Multiple Features Working Together', () => {
    it('can use greet feature and backend message feature independently', async () => {
      global.fetch = vi.fn((url) => {
        if (url.includes('/api/greet')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ 
              greeting: 'Hello, Alice! Welcome to our purple-themed app!', 
              timestamp: new Date().toISOString() 
            })
          })
        }
        if (url.includes('/api/hello')) {
          return Promise.resolve({
            ok: true,
            json: async () => ({ 
              message: 'Hello World from Backend!', 
              timestamp: new Date().toISOString() 
            })
          })
        }
      })

      render(<App />)
      
      // Use greet feature
      const input = screen.getByLabelText(/enter your name/i)
      const greetButton = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Alice')
      await userEvent.click(greetButton)
      
      await waitFor(() => {
        const statuses = screen.getAllByRole('status')
        expect(statuses.some(status => 
          status.textContent.includes('Hello, Alice')
        )).toBe(true)
      })

      // Use backend message feature
      const backendButton = screen.getByRole('button', { name: /get message from backend/i })
      await userEvent.click(backendButton)
      
      await waitFor(() => {
        const statuses = screen.getAllByRole('status')
        expect(statuses.some(status => 
          status.textContent.includes('Hello World from Backend')
        )).toBe(true)
      })
      
      // Both messages should be visible
      const allStatuses = screen.getAllByRole('status')
      expect(allStatuses.length).toBe(2)
    })
  })

  describe('Accessibility', () => {
    it('name input has accessible label', () => {
      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      expect(input).toHaveAttribute('aria-label')
    })

    it('greet button has accessible label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      expect(button).toHaveAttribute('aria-label')
    })

    it('backend button has accessible label', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /get message from backend/i })
      expect(button).toHaveAttribute('aria-label')
    })

    it('success messages have status role', async () => {
      global.fetch = vi.fn(() => 
        Promise.resolve({
          ok: true,
          json: async () => ({ 
            greeting: 'Hello, Alice! Welcome to our purple-themed app!', 
            timestamp: new Date().toISOString() 
          })
        })
      )
      
      render(<App />)
      const input = screen.getByLabelText(/enter your name/i)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.type(input, 'Alice')
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getAllByRole('status').length).toBeGreaterThan(0)
      })
    })

    it('error messages have alert role', async () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /greet me/i })
      
      await userEvent.click(button)
      
      await waitFor(() => {
        expect(screen.getAllByRole('alert').length).toBeGreaterThan(0)
      })
    })
  })
})
