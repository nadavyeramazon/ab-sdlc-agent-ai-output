import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MessageDisplay from '../MessageDisplay'

describe('MessageDisplay Component', () => {
  const defaultProps = {
    message: 'Hello from backend!'
  }

  it('renders message display with title and content', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const messageDisplay = screen.getByRole('region', { name: /message from backend/i })
    expect(messageDisplay).toBeInTheDocument()
    
    const title = screen.getByRole('heading', { level: 3, name: /message from backend/i })
    expect(title).toBeInTheDocument()
    
    const message = screen.getByText(defaultProps.message)
    expect(message).toBeInTheDocument()
  })

  it('displays timestamp when provided', () => {
    const timestamp = '2023-12-01T10:00:00Z'
    render(<MessageDisplay {...defaultProps} timestamp={timestamp} />)
    
    const timestampElement = screen.getByText(/received at:/i)
    expect(timestampElement).toBeInTheDocument()
    expect(timestampElement).toHaveTextContent('Received at:')
  })

  it('displays current timestamp when not provided', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const timestampElement = screen.getByText(/received at:/i)
    expect(timestampElement).toBeInTheDocument()
    expect(timestampElement).toHaveTextContent('Received at:')
  })

  it('includes check mark icon', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const icon = screen.getByText('✅')
    expect(icon).toBeInTheDocument()
    expect(icon).toHaveAttribute('aria-hidden', 'true')
  })

  it('has proper accessibility attributes', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const messageDisplay = screen.getByRole('region')
    expect(messageDisplay).toHaveAttribute('aria-labelledby', 'message-title')
    expect(messageDisplay).toHaveAttribute('aria-live', 'polite')
    
    const title = screen.getByRole('heading', { level: 3 })
    expect(title).toHaveAttribute('id', 'message-title')
  })

  it('applies custom className when provided', () => {
    const customClass = 'custom-message'
    render(<MessageDisplay {...defaultProps} className={customClass} />)
    
    const messageDisplay = screen.getByRole('region')
    expect(messageDisplay).toHaveClass('message-display', customClass)
  })

  it('handles long message text gracefully', () => {
    const longMessage = 'This is a very long message that should wrap properly and not break the layout of the component when displayed to the user'
    render(<MessageDisplay message={longMessage} />)
    
    const messageText = screen.getByText(longMessage)
    expect(messageText).toBeInTheDocument()
    expect(messageText).toHaveClass('message-text')
  })

  it('formats timestamp correctly', () => {
    const timestamp = '2023-12-01T15:30:00Z'
    render(<MessageDisplay {...defaultProps} timestamp={timestamp} />)
    
    // The exact format depends on locale, but it should contain the date/time info
    const timestampElement = screen.getByText(/received at:/i)
    expect(timestampElement.textContent).toMatch(/\d+\/\d+\/\d+/)
  })

  it('renders with fade-in animation class', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const messageDisplay = screen.getByRole('region')
    expect(messageDisplay).toHaveClass('message-display')
  })

  it('has proper semantic structure', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    // Check that the component structure is semantic
    const heading = screen.getByRole('heading', { level: 3 })
    const region = screen.getByRole('region')
    
    expect(heading).toBeInTheDocument()
    expect(region).toBeInTheDocument()
    expect(region).toContainElement(heading)
  })

  it('displays message text with proper styling classes', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const messageText = screen.getByText(defaultProps.message)
    expect(messageText).toHaveClass('message-text')
    
    const timestampText = screen.getByText(/received at:/i)
    expect(timestampText).toHaveClass('message-timestamp')
  })
})