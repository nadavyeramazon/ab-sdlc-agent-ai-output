import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MessageDisplay from '../MessageDisplay'

describe('MessageDisplay Component', () => {
  const defaultProps = {
    message: 'Hello from the backend!'
  }

  it('renders message with correct content', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const region = screen.getByRole('region', { name: /message from backend/i })
    expect(region).toBeInTheDocument()
    
    expect(screen.getByText('Hello from the backend!')).toBeInTheDocument()
  })

  it('displays success icon', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const icon = screen.getByText('✅')
    expect(icon).toBeInTheDocument()
    expect(icon).toHaveAttribute('aria-hidden', 'true')
  })

  it('renders title correctly', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const title = screen.getByRole('heading', { level: 3 })
    expect(title).toBeInTheDocument()
    expect(title).toHaveTextContent('Message from Backend')
    expect(title).toHaveAttribute('id', 'message-title')
  })

  it('applies custom className when provided', () => {
    render(<MessageDisplay {...defaultProps} className="custom-message-class" />)
    
    const region = screen.getByRole('region')
    expect(region).toHaveClass('custom-message-class')
  })

  it('has proper accessibility attributes', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    const region = screen.getByRole('region')
    expect(region).toHaveAttribute('aria-labelledby', 'message-title')
    expect(region).toHaveAttribute('aria-live', 'polite')
  })

  it('renders long messages correctly', () => {
    const longMessage = 'This is a very long message from the backend that should be displayed properly and wrap to multiple lines if necessary without breaking the layout. It contains multiple sentences and should maintain good readability.'
    
    render(<MessageDisplay message={longMessage} />)
    
    expect(screen.getByText(longMessage)).toBeInTheDocument()
  })

  it('handles messages with special characters', () => {
    const specialMessage = 'Hello! 👋 Welcome to our API. Status: ✓ Success (HTTP 200)'
    
    render(<MessageDisplay message={specialMessage} />)
    
    expect(screen.getByText(specialMessage)).toBeInTheDocument()
  })

  it('handles empty message gracefully', () => {
    render(<MessageDisplay message="" />)
    
    const region = screen.getByRole('region')
    expect(region).toBeInTheDocument()
    
    const messageText = screen.getByText('')
    expect(messageText).toBeInTheDocument()
  })

  it('maintains proper structure with all elements', () => {
    render(<MessageDisplay {...defaultProps} />)
    
    // Check that all main elements are present
    const region = screen.getByRole('region')
    const icon = region.querySelector('.message-icon')
    const content = region.querySelector('.message-content')
    const title = region.querySelector('.message-title')
    const text = region.querySelector('.message-text')
    
    expect(icon).toBeInTheDocument()
    expect(content).toBeInTheDocument()
    expect(title).toBeInTheDocument()
    expect(text).toBeInTheDocument()
  })
})