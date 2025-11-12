// Test setup for Vitest and React Testing Library
import '@testing-library/jest-dom'

// Mock environment variables for tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock fetch for API tests
global.fetch = vi.fn()

// Setup test environment variables
process.env.VITE_API_URL = 'http://localhost:8000'

// Clean up after each test
afterEach(() => {
  vi.clearAllMocks()
})