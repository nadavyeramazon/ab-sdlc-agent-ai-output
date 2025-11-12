import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App'

// Integration test to verify the complete application flow
describe('App Integration Tests', () => {
  let mockFetch

  beforeEach(() => {
    mockFetch = vi.fn()
    global.fetch = mockFetch
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('should render Hello World app with all required elements', () => {
    render(<App />)
    
    // Verify "Hello World" h1 heading exists
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
    expect(heading).toHaveTextContent('Hello World')
    
    // Verify button labeled "Get Message from Backend"
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toBeInTheDocument()
    expect(button).not.toBeDisabled()
    
    // Verify green color scheme is applied (checking CSS custom properties)
    const computedStyle = getComputedStyle(document.documentElement)
    expect(computedStyle.getPropertyValue('--color-primary').trim()).toBe('#2ecc71')
    expect(computedStyle.getPropertyValue('--color-secondary').trim()).toBe('#27ae60')
  })

  it('should make API call to http://localhost:8000/api/hello and display response', async () => {
    const user = userEvent.setup()
    const mockResponse = {
      message: 'Hello from the backend!',
      timestamp: '2023-12-01T10:00:00Z'
    }

    mockFetch.mockResolvedValueOnce({
      ok: true,
      headers: new Map([['content-type', 'application/json']]),
      json: async () => mockResponse
    })

    render(<App />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    // Verify API call to correct endpoint
    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/hello',
      expect.objectContaining({
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      })
    )
    
    // Verify response is displayed
    await waitFor(() => {
      const messageDisplay = screen.getByRole('region', { name: /message from backend/i })
      expect(messageDisplay).toBeInTheDocument()
      expect(messageDisplay).toHaveTextContent('Hello from the backend!')
    })
  })

  it('should show loading spinner during API call', async () => {
    const user = userEvent.setup()
    
    // Mock a delayed response
    mockFetch.mockImplementation(() => 
      new Promise(resolve => 
        setTimeout(() => resolve({
          ok: true,
          headers: new Map([['content-type', 'application/json']]),
          json: async () => ({ message: 'Hello!' })
        }), 100)
      )
    )

    render(<App />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    // Verify loading spinner appears
    const spinner = screen.getByRole('status', { name: /loading/i })
    expect(spinner).toBeInTheDocument()
    
    // Verify button shows loading state
    expect(button).toHaveTextContent('Getting Message...')
    expect(button).toBeDisabled()
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByRole('status', { name: /loading/i })).not.toBeInTheDocument()
    }, { timeout: 200 })
  })

  it('should show error handling when API call fails', async () => {
    const user = userEvent.setup()
    
    mockFetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    // Verify error message appears
    await waitFor(() => {
      const errorMessage = screen.getByRole('alert')
      expect(errorMessage).toBeInTheDocument()
      expect(errorMessage).toHaveTextContent(/unable to connect to the backend server/i)
    })
  })

  it('should be responsive and accessible', () => {
    render(<App />)
    
    // Verify main landmark
    const main = screen.getByRole('main')
    expect(main).toBeInTheDocument()
    
    // Verify button accessibility
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toHaveAttribute('type', 'button')
    expect(button).toHaveAttribute('aria-label')
    
    // Verify heading structure
    const h1 = screen.getByRole('heading', { level: 1 })
    expect(h1).toBeInTheDocument()
    
    // Verify emoji accessibility
    const emoji = screen.getByRole('img', { name: /waving hand/i })
    expect(emoji).toBeInTheDocument()
  })

  it('should handle HTTP error responses correctly', async () => {
    const user = userEvent.setup()
    
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: async () => ({ detail: 'Server is temporarily unavailable' })
    })

    render(<App />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    await waitFor(() => {
      const errorMessage = screen.getByRole('alert')
      expect(errorMessage).toBeInTheDocument()
      expect(errorMessage).toHaveTextContent('Server is temporarily unavailable')
    })
  })

  it('should retry API call when retry button is clicked', async () => {
    const user = userEvent.setup()
    
    // First call fails
    mockFetch.mockRejectedValueOnce(new Error('Network error'))
    
    render(<App />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument()
    })
    
    // Mock successful retry
    mockFetch.mockResolvedValueOnce({
      ok: true,
      headers: new Map([['content-type', 'application/json']]),
      json: async () => ({ message: 'Success on retry!' })
    })
    
    // Click retry button
    const retryButton = screen.getByRole('button', { name: /try again/i })
    await user.click(retryButton)
    
    // Verify success message appears
    await waitFor(() => {
      const messageDisplay = screen.getByRole('region', { name: /message from backend/i })
      expect(messageDisplay).toHaveTextContent('Success on retry!')
    })
  })
})