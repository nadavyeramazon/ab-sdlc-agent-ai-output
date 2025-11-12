import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

// Mock the HelloWorld component to avoid testing its internals
vi.mock('../components/HelloWorld', () => ({
  default: () => <div data-testid="hello-world-component">HelloWorld Component</div>
}))

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<App />)
    
    const app = document.querySelector('.App')
    expect(app).toBeInTheDocument()
  })

  it('renders HelloWorld component', () => {
    render(<App />)
    
    const helloWorldComponent = screen.getByTestId('hello-world-component')
    expect(helloWorldComponent).toBeInTheDocument()
  })

  it('has correct structure', () => {
    render(<App />)
    
    const app = document.querySelector('.App')
    expect(app).toBeInTheDocument()
    
    const helloWorldComponent = screen.getByTestId('hello-world-component')
    expect(app).toContainElement(helloWorldComponent)
  })
})