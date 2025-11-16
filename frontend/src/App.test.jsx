/**
 * Comprehensive test suite for the Purple Theme Hello World App
 * 
 * Tests cover:
 * - Existing feature: "Get Message from Backend" button and /api/hello endpoint
 * - New feature: Personalized greeting with /api/greet endpoint
 * - Component rendering and initial state
 * - User interactions (button clicks, input changes)
 * - API integration (successful responses, errors, loading states)
 * - Client-side validation
 * - Error handling (network errors, HTTP errors)
 * - Loading states (spinners, disabled buttons)
 * - Accessibility (ARIA labels, roles, live regions)
 * - Feature independence (both features work without interference)
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component - Initial Rendering', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('renders the Hello World heading', () => {
    render(<App />)
    const heading = screen.getByRole('heading', { name: /hello world/i })
    expect(heading).toBeInTheDocument()
  })

  it('renders the Get Message from Backend button', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toBeInTheDocument()
    expect(button).toBeEnabled()
  })

  it('renders the greeting section with input and button', () => {
    render(<App />)
    
    // Check for greeting section heading
    const greetingHeading = screen.getByRole('heading', { name: /get a personalized greeting/i })
    expect(greetingHeading).toBeInTheDocument()
    
    // Check for input field
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    expect(input).toBeInTheDocument()
    expect(input).toHaveAttribute('placeholder', 'Enter your name')
    
    // Check for greet button
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    expect(greetButton).toBeInTheDocument()
    expect(greetButton).toBeEnabled()
  })

  it('has no messages or errors displayed initially', () => {
    render(<App />)
    
    // No backend message
    expect(screen.queryByText(/hello world from backend/i)).not.toBeInTheDocument()
    
    // No greeting message
    expect(screen.queryByText(/welcome to our purple-themed app/i)).not.toBeInTheDocument()
    
    // No error messages
    expect(screen.queryByText(/failed to fetch/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
  })
})

describe('App Component - Existing Feature: Get Message from Backend', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('fetches and displays message from backend on button click', async () => {
    const user = userEvent.setup()
    
    // Mock successful response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        message: 'Hello World from Backend!',
        timestamp: '2024-01-15T14:30:00.000000Z'
      })
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    
    await user.click(button)

    // Verify fetch was called correctly
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/hello')
    
    // Wait for message to appear
    await waitFor(() => {
      expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
    })
  })

  it('shows loading state during backend fetch', async () => {
    const user = userEvent.setup()
    
    // Mock delayed response
    fetch.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({ message: 'Test', timestamp: '2024-01-15T14:30:00Z' })
      }), 100))
    )

    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    
    await user.click(button)

    // Check for loading indicator
    expect(screen.getByText(/fetching data from backend/i)).toBeInTheDocument()
    expect(button).toHaveTextContent(/loading/i)
    expect(button).toBeDisabled()
    
    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.queryByText(/fetching data from backend/i)).not.toBeInTheDocument()
    })
  })

  it('displays error message when backend fetch fails', async () => {
    const user = userEvent.setup()
    
    // Mock network error
    fetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    
    await user.click(button)

    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/failed to fetch data from backend/i)).toBeInTheDocument()
    })
  })
})

describe('App Component - New Feature: Personalized Greeting', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('allows user to type name in input field', async () => {
    const user = userEvent.setup()
    
    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    
    await user.type(input, 'Alice')
    
    expect(input).toHaveValue('Alice')
  })

  it('shows validation error when submitting empty name', async () => {
    const user = userEvent.setup()
    
    render(<App />)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    // Click without entering name
    await user.click(greetButton)

    // Validation error should appear
    expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
    
    // No API call should be made
    expect(fetch).not.toHaveBeenCalled()
  })

  it('shows validation error when submitting whitespace-only name', async () => {
    const user = userEvent.setup()
    
    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    // Enter only whitespace
    await user.type(input, '   ')
    await user.click(greetButton)

    // Validation error should appear
    expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
    
    // No API call should be made
    expect(fetch).not.toHaveBeenCalled()
  })

  it('clears validation error when user starts typing', async () => {
    const user = userEvent.setup()
    
    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    // Trigger validation error
    await user.click(greetButton)
    expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
    
    // Start typing
    await user.type(input, 'A')
    
    // Error should be cleared
    expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
  })

  it('fetches greeting from backend with valid name', async () => {
    const user = userEvent.setup()
    
    // Mock successful greeting response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        greeting: 'Hello, Bob! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T14:30:00.000000Z'
      })
    })

    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    // Enter name and submit
    await user.type(input, 'Bob')
    await user.click(greetButton)

    // Verify API call
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/greet',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Bob' })
      })
    )
    
    // Wait for greeting to appear
    await waitFor(() => {
      expect(screen.getByText(/hello, bob! welcome to our purple-themed app!/i)).toBeInTheDocument()
    })
  })

  it('shows loading state during greeting fetch', async () => {
    const user = userEvent.setup()
    
    // Mock delayed response
    fetch.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({ greeting: 'Test greeting', timestamp: '2024-01-15T14:30:00Z' })
      }), 100))
    )

    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    await user.type(input, 'Test')
    await user.click(greetButton)

    // Check for loading state
    expect(screen.getByText(/fetching your greeting/i)).toBeInTheDocument()
    expect(greetButton).toHaveTextContent(/loading/i)
    expect(greetButton).toBeDisabled()
    expect(input).toBeDisabled()
    
    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.queryByText(/fetching your greeting/i)).not.toBeInTheDocument()
    })
  })

  it('displays error when greeting fetch fails', async () => {
    const user = userEvent.setup()
    
    // Mock network error
    fetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    await user.type(input, 'TestUser')
    await user.click(greetButton)

    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/failed to fetch greeting/i)).toBeInTheDocument()
    })
  })

  it('clears input field after successful greeting', async () => {
    const user = userEvent.setup()
    
    // Mock successful response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        greeting: 'Hello, Diana! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T14:30:00Z'
      })
    })

    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    await user.type(input, 'Diana')
    expect(input).toHaveValue('Diana')
    
    await user.click(greetButton)

    // Wait for greeting and verify input cleared
    await waitFor(() => {
      expect(screen.getByText(/hello, diana/i)).toBeInTheDocument()
      expect(input).toHaveValue('')
    })
  })

  it('allows submitting via Enter key', async () => {
    const user = userEvent.setup()
    
    // Mock successful response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        greeting: 'Hello, Eve! Welcome to our purple-themed app!',
        timestamp: '2024-01-15T14:30:00Z'
      })
    })

    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    
    await user.type(input, 'Eve{Enter}')

    // Verify API call was made
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/greet',
      expect.objectContaining({
        method: 'POST'
      })
    )
    
    // Wait for greeting to appear
    await waitFor(() => {
      expect(screen.getByText(/hello, eve/i)).toBeInTheDocument()
    })
  })
})

describe('App Component - Feature Independence', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('allows using both features independently', async () => {
    const user = userEvent.setup()
    
    // Mock responses for both features
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T14:30:00Z'
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Frank! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T14:31:00Z'
        })
      })

    render(<App />)
    
    // Use first feature
    const helloButton = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(helloButton)
    
    await waitFor(() => {
      expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
    })
    
    // Use second feature
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    await user.type(input, 'Frank')
    await user.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText(/hello, frank/i)).toBeInTheDocument()
    })
    
    // Both messages should be visible
    expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
    expect(screen.getByText(/hello, frank/i)).toBeInTheDocument()
  })

  it('greeting feature does not clear hello message', async () => {
    const user = userEvent.setup()
    
    // Mock responses
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          message: 'Hello World from Backend!',
          timestamp: '2024-01-15T14:30:00Z'
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Grace! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T14:31:00Z'
        })
      })

    render(<App />)
    
    // Get hello message first
    const helloButton = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(helloButton)
    
    await waitFor(() => {
      expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
    })
    
    // Then get greeting
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    await user.type(input, 'Grace')
    await user.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText(/hello, grace/i)).toBeInTheDocument()
    })
    
    // Hello message should still be visible
    expect(screen.getByText(/hello world from backend/i)).toBeInTheDocument()
  })
})

describe('App Component - Accessibility', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('has proper ARIA labels on buttons', () => {
    render(<App />)
    
    const helloButton = screen.getByRole('button', { name: /fetch message from backend api/i })
    expect(helloButton).toHaveAttribute('aria-label')
    
    const greetButton = screen.getByRole('button', { name: /get personalized greeting/i })
    expect(greetButton).toHaveAttribute('aria-label')
  })

  it('has proper ARIA label on input field', () => {
    render(<App />)
    
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    expect(input).toHaveAttribute('aria-label')
  })

  it('marks input as invalid when validation error exists', async () => {
    const user = userEvent.setup()
    
    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    // Trigger validation error
    await user.click(greetButton)
    
    // Input should be marked as invalid
    expect(input).toHaveAttribute('aria-invalid', 'true')
    expect(input).toHaveAttribute('aria-describedby', 'validation-error')
  })

  it('uses live regions for dynamic content', () => {
    render(<App />)
    
    // Check for live regions (they exist but may not have content initially)
    const liveRegions = screen.queryAllByRole('status')
    expect(liveRegions.length).toBeGreaterThan(0)
  })
})

describe('App Component - State Management', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('clears previous greeting when submitting new name', async () => {
    const user = userEvent.setup()
    
    // Mock two successful responses
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, First! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T14:30:00Z'
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Second! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T14:31:00Z'
        })
      })

    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    // First greeting
    await user.type(input, 'First')
    await user.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText(/hello, first/i)).toBeInTheDocument()
    })
    
    // Second greeting
    await user.type(input, 'Second')
    await user.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText(/hello, second/i)).toBeInTheDocument()
    })
    
    // First greeting should be replaced
    expect(screen.queryByText(/hello, first/i)).not.toBeInTheDocument()
  })

  it('clears previous error when submitting new greeting', async () => {
    const user = userEvent.setup()
    
    // Mock error then success
    fetch
      .mockRejectedValueOnce(new Error('Network error'))
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Retry! Welcome to our purple-themed app!',
          timestamp: '2024-01-15T14:30:00Z'
        })
      })

    render(<App />)
    const input = screen.getByLabelText(/enter your name for personalized greeting/i)
    const greetButton = screen.getByRole('button', { name: /greet me/i })
    
    // First attempt with error
    await user.type(input, 'Test')
    await user.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText(/failed to fetch greeting/i)).toBeInTheDocument()
    })
    
    // Retry with success
    await user.clear(input)
    await user.type(input, 'Retry')
    await user.click(greetButton)
    
    await waitFor(() => {
      expect(screen.getByText(/hello, retry/i)).toBeInTheDocument()
    })
    
    // Error should be cleared
    expect(screen.queryByText(/failed to fetch greeting/i)).not.toBeInTheDocument()
  })
})
