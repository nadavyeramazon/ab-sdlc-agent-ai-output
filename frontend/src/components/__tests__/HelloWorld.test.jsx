import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import HelloWorld from '../HelloWorld'
import * as useApiModule from '../../hooks/useApi'

// Mock the useApi hook
vi.mock('../../hooks/useApi')

describe('HelloWorld Component', () => {
  const mockFetchData = vi.fn()
  const mockClearError = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
    useApiModule.useApi.mockReturnValue({
      loading: false,
      error: null,
      fetchData: mockFetchData,
      clearError: mockClearError
    })
  })

  it('renders main heading with correct text and emoji', () => {
    render(<HelloWorld />)
    
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
    expect(heading).toHaveTextContent('Hello World')
    
    const emoji = screen.getByRole('img', { name: /waving hand/i })
    expect(emoji).toBeInTheDocument()
  })

  it('renders subtitle with welcome message', () => {
    render(<HelloWorld />)
    
    const subtitle = screen.getByText(/welcome to our green-themed fullstack application/i)
    expect(subtitle).toBeInTheDocument()
  })

  it('renders get message button', () => {
    render(<HelloWorld />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toBeInTheDocument()
    expect(button).not.toBeDisabled()
  })

  it('calls fetchData when button is clicked', async () => {
    const user = userEvent.setup()
    mockFetchData.mockResolvedValueOnce({ message: 'Hello from backend!' })
    
    render(<HelloWorld />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    expect(mockFetchData).toHaveBeenCalledTimes(1)
    expect(mockFetchData).toHaveBeenCalledWith('/api/hello')
  })

  it('displays loading state when fetching data', () => {
    useApiModule.useApi.mockReturnValue({
      loading: true,
      error: null,
      fetchData: mockFetchData,
      clearError: mockClearError
    })
    
    render(<HelloWorld />)
    
    const button = screen.getByRole('button')
    expect(button).toHaveTextContent('Getting Message...')
    expect(button).toBeDisabled()
    
    const spinner = screen.getByRole('status', { name: /loading/i })
    expect(spinner).toBeInTheDocument()
  })

  it('displays error message when API call fails', () => {
    const errorMessage = 'Failed to fetch data'
    useApiModule.useApi.mockReturnValue({
      loading: false,
      error: errorMessage,
      fetchData: mockFetchData,
      clearError: mockClearError
    })
    
    render(<HelloWorld />)
    
    const errorElement = screen.getByRole('alert')
    expect(errorElement).toBeInTheDocument()
    expect(errorElement).toHaveTextContent(errorMessage)
  })

  it('displays message when API call succeeds', async () => {
    const user = userEvent.setup()
    const mockMessage = 'Hello from the backend!'
    mockFetchData.mockResolvedValueOnce({ message: mockMessage })
    
    render(<HelloWorld />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    await waitFor(() => {
      const messageDisplay = screen.getByRole('region', { name: /message from backend/i })
      expect(messageDisplay).toBeInTheDocument()
      expect(messageDisplay).toHaveTextContent(mockMessage)
    })
  })

  it('handles API response without message property', async () => {
    const user = userEvent.setup()
    mockFetchData.mockResolvedValueOnce({ data: 'some other data' })
    
    render(<HelloWorld />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    await waitFor(() => {
      const messageDisplay = screen.getByRole('region', { name: /message from backend/i })
      expect(messageDisplay).toBeInTheDocument()
      expect(messageDisplay).toHaveTextContent('Hello from backend!')
    })
  })

  it('renders tech stack information', () => {
    render(<HelloWorld />)
    
    expect(screen.getByText(/built with/i)).toBeInTheDocument()
    expect(screen.getByText('React 18')).toBeInTheDocument()
    expect(screen.getByText('Vite')).toBeInTheDocument()
    expect(screen.getByText('FastAPI')).toBeInTheDocument()
  })

  it('has proper accessibility attributes', () => {
    render(<HelloWorld />)
    
    const main = screen.getByRole('main')
    expect(main).toBeInTheDocument()
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toHaveAttribute('type', 'button')
  })

  it('handles fetch error correctly', async () => {
    const user = userEvent.setup()
    const fetchError = new Error('Network error')
    mockFetchData.mockRejectedValueOnce(fetchError)
    
    // Mock console.error to avoid test output noise
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    
    render(<HelloWorld />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    expect(consoleSpy).toHaveBeenCalledWith('Failed to fetch message:', fetchError)
    
    consoleSpy.mockRestore()
  })
})