import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import LoadingSpinner from '../LoadingSpinner'

describe('LoadingSpinner Component', () => {
  it('renders with default props', () => {
    render(<LoadingSpinner />)
    
    const spinner = screen.getByRole('status', { name: /loading/i })
    expect(spinner).toBeInTheDocument()
    expect(spinner).toHaveClass('loading-spinner--md')
    expect(spinner).toHaveClass('loading-spinner--primary')
  })

  it('renders with custom size', () => {
    render(<LoadingSpinner size="lg" />)
    
    const spinner = screen.getByRole('status')
    expect(spinner).toHaveClass('loading-spinner--lg')
  })

  it('renders with custom color', () => {
    render(<LoadingSpinner color="secondary" />)
    
    const spinner = screen.getByRole('status')
    expect(spinner).toHaveClass('loading-spinner--secondary')
  })

  it('applies custom className', () => {
    render(<LoadingSpinner className="custom-class" />)
    
    const spinner = screen.getByRole('status')
    expect(spinner).toHaveClass('custom-class')
  })

  it('has proper accessibility attributes', () => {
    render(<LoadingSpinner />)
    
    const spinner = screen.getByRole('status')
    expect(spinner).toHaveAttribute('aria-label', 'Loading')
    
    const srText = screen.getByText('Loading...')
    expect(srText).toHaveClass('sr-only')
  })

  it('renders all size variants correctly', () => {
    const sizes = ['xs', 'sm', 'md', 'lg', 'xl']
    
    sizes.forEach(size => {
      const { unmount } = render(<LoadingSpinner size={size} />)
      const spinner = screen.getByRole('status')
      expect(spinner).toHaveClass(`loading-spinner--${size}`)
      unmount()
    })
  })

  it('renders all color variants correctly', () => {
    const colors = ['primary', 'secondary', 'white']
    
    colors.forEach(color => {
      const { unmount } = render(<LoadingSpinner color={color} />)
      const spinner = screen.getByRole('status')
      expect(spinner).toHaveClass(`loading-spinner--${color}`)
      unmount()
    })
  })

  it('contains spinner ring with correct structure', () => {
    render(<LoadingSpinner />)
    
    const spinner = screen.getByRole('status')
    const ring = spinner.querySelector('.spinner-ring')
    expect(ring).toBeInTheDocument()
    
    const dots = ring.querySelectorAll('div')
    expect(dots).toHaveLength(4)
  })
})