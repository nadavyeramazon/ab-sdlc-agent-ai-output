import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    vi.clearAllMocks()
    // Reset window.API_CONFIG
    delete window.API_CONFIG
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the main heading', () => {
    render(<App />)
    const heading = screen.getByRole('heading', { name: /hello world/i })
    expect(heading).toBeInTheDocument()
  })

  it('renders the fetch button', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toBeInTheDocument()
    expect(button).not.toBeDisabled()
  })

  it('shows loading state when button is clicked', async () => {
    // Mock a delayed response
    global.fetch.mockImplementation(() => 
      new Promise(resolve => 
        setTimeout(() => resolve({
          ok: true,
          json: async () => ({ message: 'Test', timestamp: '2024-01-01T00:00:00Z' })
        }), 100)
      )
    )

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    // Button should show loading text and be disabled
    expect(button).toHaveTextContent(/loading/i)
    expect(button).toBeDisabled()
  })

  it('displays backend message on successful fetch', async () => {
    const mockData = {
      message: 'Hello World from Backend!',
      timestamp: '2024-01-15T10:30:00Z'
    }

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    })

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    // Wait for message to appear
    await waitFor(() => {
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
    })
    
    // Check timestamp is displayed
    expect(screen.getByText(/received at:/i)).toBeInTheDocument()
  })

  it('displays error message on network failure', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Failed to fetch'))

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument()
    })
    
    expect(screen.getByText(/cannot connect to backend/i)).toBeInTheDocument()
  })

  it('displays error message on HTTP error', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    })

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument()
    })
    
    expect(screen.getByText(/http error! status: 500/i)).toBeInTheDocument()
  })

  it('displays timeout error on request timeout', async () => {
    // Mock AbortError
    const abortError = new Error('Aborted')
    abortError.name = 'AbortError'
    global.fetch.mockRejectedValueOnce(abortError)

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument()
    })
    
    expect(screen.getByText(/request timed out/i)).toBeInTheDocument()
  })

  it('uses window.API_CONFIG.apiUrl when available', async () => {
    window.API_CONFIG = { apiUrl: 'http://backend:8000' }
    
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'Test', timestamp: '2024-01-01T00:00:00Z' })
    })

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://backend:8000/api/hello',
        expect.any(Object)
      )
    })
  })

  it('uses localhost fallback when API_CONFIG is not set', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'Test', timestamp: '2024-01-01T00:00:00Z' })
    })

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/hello',
        expect.any(Object)
      )
    })
  })

  it('clears previous messages when fetching new data', async () => {
    const mockData1 = {
      message: 'First message',
      timestamp: '2024-01-01T00:00:00Z'
    }
    const mockData2 = {
      message: 'Second message',
      timestamp: '2024-01-02T00:00:00Z'
    }

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData1
    })

    render(<App />)
    const button = screen.getByRole('button')
    
    // First fetch
    fireEvent.click(button)
    await waitFor(() => {
      expect(screen.getByText('First message')).toBeInTheDocument()
    })
    
    // Second fetch
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData2
    })
    
    fireEvent.click(button)
    await waitFor(() => {
      expect(screen.getByText('Second message')).toBeInTheDocument()
    })
    
    // First message should not be present
    expect(screen.queryByText('First message')).not.toBeInTheDocument()
  })

  it('formats timestamp correctly', async () => {
    const mockData = {
      message: 'Test message',
      timestamp: '2024-01-15T10:30:00Z'
    }

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    })

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    await waitFor(() => {
      const timestampElement = screen.getByText(/received at:/i)
      expect(timestampElement).toBeInTheDocument()
      // Check that timestamp is formatted (not raw ISO string)
      expect(timestampElement.textContent).not.toContain('2024-01-15T10:30:00Z')
    })
  })

  it('has proper accessibility attributes', () => {
    render(<App />)
    const button = screen.getByRole('button')
    
    expect(button).toHaveAttribute('aria-live', 'polite')
  })

  it('error container has alert role', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Test error'))

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    await waitFor(() => {
      const errorContainer = screen.getByRole('alert')
      expect(errorContainer).toBeInTheDocument()
    })
  })

  it('message container has proper aria-label', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'Test', timestamp: '2024-01-01T00:00:00Z' })
    })

    render(<App />)
    const button = screen.getByRole('button')
    
    fireEvent.click(button)
    
    await waitFor(() => {
      const messageContainer = screen.getByRole('region', { name: /backend response/i })
      expect(messageContainer).toBeInTheDocument()
    })
  })
})
