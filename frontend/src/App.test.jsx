import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component - Existing Features', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
  })

  it('renders Hello World heading', () => {
    render(<App />)
    const heading = screen.getByText('Hello World')
    expect(heading).toBeInTheDocument()
    expect(heading.tagName).toBe('H1')
  })

  it('renders Get Message from Backend button', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toBeInTheDocument()
  })

  it('displays loading state when fetching message', async () => {
    // Mock a delayed response
    fetch.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-01T12:00:00Z' })
      }), 100))
    )

    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    
    fireEvent.click(button)
    
    // Check loading state
    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(button).toBeDisabled()
  })

  it('displays message from backend on successful fetch', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ 
        message: 'Hello World from Backend!', 
        timestamp: '2024-01-01T12:00:00Z' 
      })
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
    })
  })

  it('displays error message when fetch fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch message. Please try again.')).toBeInTheDocument()
    })
  })

  it('calls correct API endpoint for hello message', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-01T12:00:00Z' })
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/hello')
    })
  })
})

describe('App Component - New Greeting Feature', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders greeting input field', () => {
    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    expect(input).toBeInTheDocument()
    expect(input.type).toBe('text')
  })

  it('renders Greet Me button', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /greet me/i })
    expect(button).toBeInTheDocument()
  })

  it('updates input value when user types', () => {
    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    
    fireEvent.change(input, { target: { value: 'Alice' } })
    
    expect(input.value).toBe('Alice')
  })

  it('displays validation error for empty name', async () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Please enter your name')).toBeInTheDocument()
    })
    
    // Should not make API call
    expect(fetch).not.toHaveBeenCalled()
  })

  it('displays validation error for whitespace-only name', async () => {
    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: '   ' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Please enter your name')).toBeInTheDocument()
    })
    
    expect(fetch).not.toHaveBeenCalled()
  })

  it('displays loading state when fetching greeting', async () => {
    fetch.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({ 
          greeting: 'Hello, Bob! Welcome to our purple-themed app!', 
          timestamp: '2024-01-01T12:00:00Z' 
        })
      }), 100))
    )

    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: 'Bob' } })
    fireEvent.click(button)
    
    // Check loading state
    const buttons = screen.getAllByText('Loading...')
    expect(buttons.length).toBeGreaterThan(0)
  })

  it('displays personalized greeting on successful request', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ 
        greeting: 'Hello, Charlie! Welcome to our purple-themed app!', 
        timestamp: '2024-01-01T12:00:00Z' 
      })
    })

    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: 'Charlie' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Hello, Charlie! Welcome to our purple-themed app!')).toBeInTheDocument()
    })
  })

  it('displays error message when greeting request fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: 'David' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Unable to fetch greeting. Please try again.')).toBeInTheDocument()
    })
  })

  it('calls correct API endpoint for greeting', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ 
        greeting: 'Hello, Emma! Welcome to our purple-themed app!', 
        timestamp: '2024-01-01T12:00:00Z' 
      })
    })

    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: 'Emma' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        '/api/greet',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: 'Emma' })
        })
      )
    })
  })

  it('trims whitespace from name before sending', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ 
        greeting: 'Hello, Frank! Welcome to our purple-themed app!', 
        timestamp: '2024-01-01T12:00:00Z' 
      })
    })

    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: '  Frank  ' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        '/api/greet',
        expect.objectContaining({
          body: JSON.stringify({ name: 'Frank' })
        })
      )
    })
  })

  it('handles 400 error from backend validation', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({ detail: 'Name cannot be empty' })
    })

    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: 'Test' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Unable to fetch greeting. Please try again.')).toBeInTheDocument()
    })
  })
})

describe('App Component - Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('both features work independently without interference', async () => {
    // Mock both API calls
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-01T12:00:00Z' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, Grace! Welcome to our purple-themed app!', timestamp: '2024-01-01T12:00:00Z' })
      })

    render(<App />)
    
    // Test existing feature
    const helloButton = screen.getByRole('button', { name: /get message from backend/i })
    fireEvent.click(helloButton)
    
    await waitFor(() => {
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
    })
    
    // Test new feature
    const input = screen.getByPlaceholderText('Enter your name')
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: 'Grace' } })
    fireEvent.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText('Hello, Grace! Welcome to our purple-themed app!')).toBeInTheDocument()
    })
    
    // Both messages should be visible
    expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
    expect(screen.getByText('Hello, Grace! Welcome to our purple-themed app!')).toBeInTheDocument()
  })

  it('greeting error does not affect hello message', async () => {
    // First fetch succeeds (hello), second fails (greet)
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Hello World from Backend!', timestamp: '2024-01-01T12:00:00Z' })
      })
      .mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    
    // Get hello message
    const helloButton = screen.getByRole('button', { name: /get message from backend/i })
    fireEvent.click(helloButton)
    
    await waitFor(() => {
      expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
    })
    
    // Try greeting (will fail)
    const input = screen.getByPlaceholderText('Enter your name')
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    fireEvent.change(input, { target: { value: 'Test' } })
    fireEvent.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText('Unable to fetch greeting. Please try again.')).toBeInTheDocument()
    })
    
    // Hello message should still be visible
    expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
  })

  it('multiple greeting requests work correctly', async () => {
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, Henry! Welcome to our purple-themed app!', timestamp: '2024-01-01T12:00:00Z' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ greeting: 'Hello, Ivy! Welcome to our purple-themed app!', timestamp: '2024-01-01T12:00:00Z' })
      })

    render(<App />)
    const input = screen.getByPlaceholderText('Enter your name')
    const button = screen.getByRole('button', { name: /greet me/i })
    
    // First greeting
    fireEvent.change(input, { target: { value: 'Henry' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Hello, Henry! Welcome to our purple-themed app!')).toBeInTheDocument()
    })
    
    // Second greeting
    fireEvent.change(input, { target: { value: 'Ivy' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('Hello, Ivy! Welcome to our purple-themed app!')).toBeInTheDocument()
    })
    
    // First greeting should be replaced
    expect(screen.queryByText('Hello, Henry! Welcome to our purple-themed app!')).not.toBeInTheDocument()
  })
})

describe('App Component - Purple Theme', () => {
  it('renders with purple-themed styling', () => {
    const { container } = render(<App />)
    const app = container.querySelector('.App')
    expect(app).toBeInTheDocument()
    
    // Check that CSS classes are applied (actual color values tested via visual/E2E tests)
    const input = screen.getByPlaceholderText('Enter your name')
    expect(input).toHaveClass('greeting-input')
    
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    expect(greetButton).toHaveClass('greet-button')
  })
})
