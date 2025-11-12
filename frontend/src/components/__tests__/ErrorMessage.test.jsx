import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ErrorMessage from '../ErrorMessage'

describe('ErrorMessage Component', () => {
  const defaultProps = {
    message: 'Something went wrong'
  }

  it('renders error message with default content', () => {
    render(<ErrorMessage {...defaultProps} />)
    
    const alert = screen.getByRole('alert')
    expect(alert).toBeInTheDocument()
    
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
  })

  it('displays error icon', () => {
    render(<ErrorMessage {...defaultProps} />)
    
    const icon = screen.getByText('⚠️')
    expect(icon).toBeInTheDocument()
    expect(icon).toHaveAttribute('aria-hidden', 'true')
  })

  it('renders retry button when onRetry is provided', () => {
    const mockRetry = vi.fn()
    render(<ErrorMessage {...defaultProps} onRetry={mockRetry} />)
    
    const retryButton = screen.getByRole('button', { name: /retry the previous action/i })
    expect(retryButton).toBeInTheDocument()
    expect(retryButton).toHaveTextContent('Try Again')
  })

  it('does not render retry button when onRetry is not provided', () => {
    render(<ErrorMessage {...defaultProps} />)
    
    const retryButton = screen.queryByRole('button', { name: /retry/i })
    expect(retryButton).not.toBeInTheDocument()
  })

  it('calls onRetry when retry button is clicked', async () => {
    const user = userEvent.setup()
    const mockRetry = vi.fn()
    
    render(<ErrorMessage {...defaultProps} onRetry={mockRetry} />)
    
    const retryButton = screen.getByRole('button', { name: /retry the previous action/i })
    await user.click(retryButton)
    
    expect(mockRetry).toHaveBeenCalledTimes(1)
  })

  it('applies custom id when provided', () => {
    render(<ErrorMessage {...defaultProps} id="custom-error" />)
    
    const alert = screen.getByRole('alert')
    expect(alert).toHaveAttribute('id', 'custom-error')
  })

  it('applies custom className when provided', () => {
    render(<ErrorMessage {...defaultProps} className="custom-error-class" />)
    
    const alert = screen.getByRole('alert')
    expect(alert).toHaveClass('custom-error-class')
  })

  it('has proper accessibility attributes', () => {
    render(<ErrorMessage {...defaultProps} />)
    
    const alert = screen.getByRole('alert')
    expect(alert).toHaveAttribute('aria-live', 'polite')
  })

  it('renders long error messages correctly', () => {
    const longMessage = 'This is a very long error message that should be displayed properly and wrap to multiple lines if necessary without breaking the layout.'
    
    render(<ErrorMessage message={longMessage} />)
    
    expect(screen.getByText(longMessage)).toBeInTheDocument()
  })

  it('handles special characters in error message', () => {
    const specialMessage = 'Error: Failed to fetch data from API (HTTP 500) - Internal Server Error'
    
    render(<ErrorMessage message={specialMessage} />)
    
    expect(screen.getByText(specialMessage)).toBeInTheDocument()
  })
})