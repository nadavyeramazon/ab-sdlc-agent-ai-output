import { render } from '@testing-library/react'

/**
 * Custom render function that wraps components with common providers
 * Can be extended to include context providers, routers, etc.
 */
export function renderWithProviders(ui, options = {}) {
  return render(ui, { ...options })
}

/**
 * Mock fetch response helper
 */
export function createMockResponse(data, options = {}) {
  return {
    ok: options.ok !== undefined ? options.ok : true,
    status: options.status || 200,
    json: async () => data,
    ...options
  }
}

/**
 * Setup global fetch mock
 */
export function setupFetchMock() {
  global.fetch = vi.fn()
  return global.fetch
}

/**
 * Reset fetch mock
 */
export function resetFetchMock() {
  if (global.fetch && global.fetch.mockReset) {
    global.fetch.mockReset()
  }
}
