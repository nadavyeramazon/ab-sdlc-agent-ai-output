import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock environment variables
global.import = {
  meta: {
    env: {
      VITE_API_URL: 'http://localhost:8000'
    }
  }
}
