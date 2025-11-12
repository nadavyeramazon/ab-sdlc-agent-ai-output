import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import HelloButton from '../components/HelloButton'

describe('HelloButton Component', () => {
  it('renders with correct text', () => {
    render(<HelloButton onClick={vi.fn()} loading={false} />)
    expect(screen.getByText('Get Message from Backend')).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()
    
    render(<HelloButton onClick={handleClick} loading={false} />)
    const button = screen.getByRole('button')
    
    await user.click(button)
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('displays loading state correctly', () => {
    render(<HelloButton onClick={vi.fn()} loading={true} />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('is disabled when loading', () => {
    render(<HelloButton onClick={vi.fn()} loading={true} />)
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
  })

  it('is not disabled when not loading', () => {
    render(<HelloButton onClick={vi.fn()} loading={false} />)
    const button = screen.getByRole('button')
    expect(button).not.toBeDisabled()
  })

  it('has correct aria-label', () => {
    render(<HelloButton onClick={vi.fn()} loading={false} />)
    const button = screen.getByRole('button')
    expect(button).toHaveAttribute('aria-label', 'Get message from backend')
  })

  it('has aria-busy attribute when loading', () => {
    render(<HelloButton onClick={vi.fn()} loading={true} />)
    const button = screen.getByRole('button')
    expect(button).toHaveAttribute('aria-busy', 'true')
  })
})
