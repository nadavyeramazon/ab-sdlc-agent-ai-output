import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import GreetingForm from '../components/GreetingForm'

// Mock fetch globally
global.fetch = vi.fn()

describe('GreetingForm Component - New Feature Tests', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
    fetch.mockClear()
  })

  it('renders greeting form with input and button', () => {
    render(<GreetingForm />)
    
    expect(screen.getByLabelText(/enter your name/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/e.g., John Doe/i)).toBeInTheDocument()
    expect(screen.getByText('Greet Me')).toBeInTheDocument()
  })

  it('updates input value when user types', () => {
    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    fireEvent.change(input, { target: { value: 'John Doe' } })
    
    expect(input.value).toBe('John Doe')
  })

  it('shows validation error when submitting empty name', async () => {
    render(<GreetingForm />)
    
    const button = screen.getByText('Greet Me')
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
    })
    
    // Ensure no API call was made
    expect(fetch).not.toHaveBeenCalled()
  })

  it('shows validation error when submitting whitespace-only name', async () => {
    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    fireEvent.change(input, { target: { value: '   ' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
    })
    
    expect(fetch).not.toHaveBeenCalled()
  })

  it('displays loading state during API call', async () => {
    // Mock a delayed response
    fetch.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({
          greeting: 'Hello, Test! Welcome to our purple-themed app!',
          timestamp: new Date().toISOString()
        })
      }), 100))
    )

    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    fireEvent.change(input, { target: { value: 'Test User' } })
    fireEvent.click(button)
    
    // Check loading state appears
    await waitFor(() => {
      expect(screen.getByText(/loading/i)).toBeInTheDocument()
    })
  })

  it('displays greeting message on successful submission', async () => {
    const mockResponse = {
      greeting: 'Hello, John Doe! Welcome to our purple-themed app!',
      timestamp: '2024-01-15T10:30:00.000Z'
    }

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })

    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    fireEvent.change(input, { target: { value: 'John Doe' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText(/Hello, John Doe! Welcome to our purple-themed app!/i)).toBeInTheDocument()
    })
    
    // Verify API was called correctly
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/greet',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'John Doe' })
      })
    )
  })

  it('displays error message when API returns error', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({ detail: 'Name cannot be empty' })
    })

    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    fireEvent.change(input, { target: { value: 'Test' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText(/name cannot be empty/i)).toBeInTheDocument()
    })
  })

  it('displays error message when network fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'))

    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    fireEvent.change(input, { target: { value: 'Test' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText(/network error/i)).toBeInTheDocument()
    })
  })

  it('clears input field after successful submission', async () => {
    const mockResponse = {
      greeting: 'Hello, Test! Welcome to our purple-themed app!',
      timestamp: '2024-01-15T10:30:00.000Z'
    }

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })

    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    fireEvent.change(input, { target: { value: 'Test User' } })
    expect(input.value).toBe('Test User')
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(input.value).toBe('')
    })
  })

  it('clears error when user starts typing', () => {
    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    // Trigger validation error
    fireEvent.click(button)
    expect(screen.getByText(/please enter your name/i)).toBeInTheDocument()
    
    // Start typing
    fireEvent.change(input, { target: { value: 'J' } })
    
    // Error should be cleared
    expect(screen.queryByText(/please enter your name/i)).not.toBeInTheDocument()
  })
})

describe('GreetingForm - Accessibility Tests', () => {
  it('has proper ARIA labels and attributes', () => {
    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByRole('button', { name: /submit greeting request/i })
    
    expect(input).toHaveAttribute('aria-label', 'Name input')
    expect(button).toHaveAttribute('aria-label', 'Submit greeting request')
  })

  it('sets aria-invalid when there is an error', async () => {
    render(<GreetingForm />)
    
    const input = screen.getByLabelText(/enter your name/i)
    const button = screen.getByText('Greet Me')
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(input).toHaveAttribute('aria-invalid', 'true')
    })
  })
})
