import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useApi } from '../hooks/useApi'

// Mock fetch
global.fetch = vi.fn()

describe('useApi Hook', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('initializes with correct default values', () => {
    const { result } = renderHook(() => useApi())
    
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
    expect(typeof result.current.fetchData).toBe('function')
  })

  it('handles successful API call', async () => {
    const mockData = {
      message: 'Hello World from Backend!',
      timestamp: '2024-01-15T10:30:00Z'
    }

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    })

    const { result } = renderHook(() => useApi())
    
    const data = await result.current.fetchData('/api/hello')
    
    expect(data).toEqual(mockData)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
  })

  it('handles API error', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    })

    const { result } = renderHook(() => useApi())
    
    const data = await result.current.fetchData('/api/hello')
    
    expect(data).toBe(null)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBeTruthy()
  })

  it('handles network error', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'))

    const { result } = renderHook(() => useApi())
    
    const data = await result.current.fetchData('/api/hello')
    
    expect(data).toBe(null)
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe('Network error')
  })
})
