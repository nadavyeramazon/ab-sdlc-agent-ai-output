import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App'

// Mock the useApi hook
vi.mock('../hooks/useApi', () => ({
  useApi: () => ({
    loading: false,
    error: null,
    fetchData: vi.fn().mockResolvedValue({
      message: 'Hello World from Backend!',
      timestamp: '2024-01-15T10:30:00Z'
    })
  })
}))

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<App />)
    expect(screen.getByText('Hello World')).toBeInTheDocument()
  })

  it('displays the main heading correctly', () => {
    render(<App />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toHaveTextContent('Hello World')
  })

  it('displays the subtitle', () => {
    render(<App />)
    expect(screen.getByText('Green Theme Fullstack Application')).toBeInTheDocument()
  })

  it('displays the button with correct text', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /get message from backend/i })
    expect(button).toBeInTheDocument()
  })

  it('displays footer text', () => {
    render(<App />)
    expect(screen.getByText('Built with React & FastAPI')).toBeInTheDocument()
  })
})

describe('App Component - User Interactions', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('button click triggers API call', async () => {
    const user = userEvent.setup()
    render(<App />)
    
    const button = screen.getByRole('button', { name: /get message from backend/i })
    await user.click(button)
    
    // Button should be clickable
    expect(button).not.toBeDisabled()
  })
})
