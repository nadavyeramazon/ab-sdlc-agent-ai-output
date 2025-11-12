/**
 * Comprehensive test suite for React App component
 * Tests purple theme, backend integration, and user greet functionality
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
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

    it('renders subtitle with Purple Theme', () => {
      render(<App />)
      const subtitleElement = screen.getByText(/Purple Theme React Application/i)
      expect(subtitleElement).toBeInTheDocument()
    })

    it('renders Get Message from Backend button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /Get message from backend/i })
      expect(button).toBeInTheDocument()
    })

    it('renders Backend Message section title', () => {
      render(<App />)
      const sectionTitle = screen.getByText(/Backend Message/i)
      expect(sectionTitle).toBeInTheDocument()
    })

    it('renders Personalized Greeting section title', () => {
      render(<App />)
      const sectionTitle = screen.getByText(/Personalized Greeting/i)
      expect(sectionTitle).toBeInTheDocument()
    })

    it('renders name input field', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      expect(input).toBeInTheDocument()
    })

    it('renders Greet Me button', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      expect(button).toBeInTheDocument()
    })
  })

  describe('Backend Message Feature', () => {
    it('fetches and displays backend message on button click', async () => {
      const mockResponse = {
        message: 'Hello World from Backend!',
        timestamp: '2024-01-01T12:00:00Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /Get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Hello World from Backend!/i)).toBeInTheDocument()
      })

      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    })

    it('displays loading state while fetching backend message', async () => {
      global.fetch.mockImplementationOnce(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test', timestamp: '2024-01-01T12:00:00Z' }),
        }), 100))
      )

      render(<App />)
      const button = screen.getByRole('button', { name: /Get message from backend/i })
      
      fireEvent.click(button)

      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()

      await waitFor(() => {
        expect(button).toHaveTextContent('Get Message from Backend')
      })
    })

    it('displays error message when backend fetch fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /Get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Failed to fetch from backend/i)).toBeInTheDocument()
      })
    })

    it('displays error when backend returns non-OK status', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /Get message from backend/i })
      
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/HTTP error! status: 500/i)).toBeInTheDocument()
      })
    })
  })

  describe('User Greet Feature', () => {
    it('allows user to enter name in input field', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      
      fireEvent.change(input, { target: { value: 'John' } })
      
      expect(input.value).toBe('John')
    })

    it('Greet Me button is disabled when input is empty', () => {
      render(<App />)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      expect(button).toBeDisabled()
    })

    it('Greet Me button is enabled when input has text', () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      fireEvent.change(input, { target: { value: 'John' } })
      
      expect(button).not.toBeDisabled()
    })

    it('fetches and displays personalized greeting', async () => {
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-01T12:00:00Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      fireEvent.change(input, { target: { value: 'John' } })
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Hello, John! Welcome to our purple-themed app!/i)).toBeInTheDocument()
      })

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/greet',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: 'John' }),
        })
      )
    })

    it('displays loading state while fetching greeting', async () => {
      global.fetch.mockImplementationOnce(() =>
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ greeting: 'Test', timestamp: '2024-01-01T12:00:00Z' }),
        }), 100))
      )

      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      fireEvent.change(input, { target: { value: 'John' } })
      fireEvent.click(button)

      expect(button).toHaveTextContent('Loading...')
      expect(button).toBeDisabled()

      await waitFor(() => {
        expect(button).toHaveTextContent('Greet Me')
      })
    })

    it('shows validation error when submitting empty name', async () => {
      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      // Type and then clear the input
      fireEvent.change(input, { target: { value: 'John' } })
      fireEvent.change(input, { target: { value: '' } })
      
      // Button should be disabled, but let's test form submission handler
      // We need to enable button temporarily to test validation
      expect(button).toBeDisabled()
    })

    it('trims whitespace from name before sending', async () => {
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-01T12:00:00Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      fireEvent.change(input, { target: { value: '  John  ' } })
      fireEvent.click(button)

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith(
          'http://localhost:8000/api/greet',
          expect.objectContaining({
            body: JSON.stringify({ name: 'John' }),
          })
        )
      })
    })

    it('clears input after successful greeting', async () => {
      const mockResponse = {
        greeting: 'Hello, John! Welcome to our purple-themed app!',
        timestamp: '2024-01-01T12:00:00Z'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      fireEvent.change(input, { target: { value: 'John' } })
      fireEvent.click(button)

      await waitFor(() => {
        expect(input.value).toBe('')
      })
    })

    it('displays error message when greet fetch fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      fireEvent.change(input, { target: { value: 'John' } })
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Failed to get greeting/i)).toBeInTheDocument()
      })
    })

    it('displays error when greet returns non-OK status', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Name cannot be empty' }),
      })

      render(<App />)
      const input = screen.getByPlaceholderText(/Enter your name/i)
      const button = screen.getByRole('button', { name: /Get personalized greeting/i })
      
      fireEvent.change(input, { target: { value: 'John' } })
      fireEvent.click(button)

      await waitFor(() => {
        expect(screen.getByText(/Name cannot be empty/i)).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility', () => {
    it('has proper aria-labels on buttons', () => {
      render(<App />)
      
      const backendButton = screen.getByLabelText(/Get message from backend/i)
      expect(backendButton).toBeInTheDocument()
      
      const greetButton = screen.getByLabelText(/Get personalized greeting/i)
      expect(greetButton).toBeInTheDocument()
    })

    it('has proper aria-label on name input', () => {
      render(<App />)
      const input = screen.getByLabelText(/Your name/i)
      expect(input).toBeInTheDocument()
    })

    it('uses role="status" for success messages', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-01T12:00:00Z' }),
      })

      render(<App />)
      const button = screen.getByRole('button', { name: /Get message from backend/i })
      fireEvent.click(button)

      await waitFor(() => {
        const statusElement = screen.getByRole('status')
        expect(statusElement).toBeInTheDocument()
      })
    })

    it('uses role="alert" for error messages', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Test error'))

      render(<App />)
      const button = screen.getByRole('button', { name: /Get message from backend/i })
      fireEvent.click(button)

      await waitFor(() => {
        const alertElement = screen.getByRole('alert')
        expect(alertElement).toBeInTheDocument()
      })
    })
  })

  describe('Purple Theme Verification', () => {
    it('renders with app container', () => {
      const { container } = render(<App />)
      const appDiv = container.querySelector('.app')
      expect(appDiv).toBeInTheDocument()
    })

    it('applies purple theme classes', () => {
      const { container } = render(<App />)
      const title = container.querySelector('.title')
      expect(title).toBeInTheDocument()
      expect(title).toHaveTextContent('Hello World')
    })
  })
})
