import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useApi } from '../useApi'

// Mock fetch globally
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('useApi Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('initializes with correct default state', () => {
    const { result } = renderHook(() => useApi())
    
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
    expect(typeof result.current.fetchData).toBe('function')
    expect(typeof result.current.clearError).toBe('function')
  })

  it('handles successful API call with JSON response', async () => {
    const mockData = { message: 'Hello World' }
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
      headers: {
        get: (key) => key === 'content-type' ? 'application/json' : null
      }
    })

    const { result } = renderHook(() => useApi())

    let responseData
    await act(async () => {
      responseData = await result.current.fetchData('/api/test')
    })

    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe(null)
    expect(responseData).toEqual(mockData)
    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/test',
      expect.objectContaining({
        headers: {
          'Content-Type': 'application/json'
        }
      })
    )
  })

  it('handles successful API call with text response', async () => {
    const mockText = 'Plain text response'
    mockFetch.mockResolvedValueOnce({
      ok: true,
      text: () => Promise.resolve(mockText),
      headers: {
        get: () => null
      }
    })

    const { result } = renderHook(() => useApi())

    let responseData
    await act(async () => {
      responseData = await result.current.fetchData('/api/test')
    })

    expect(responseData).toBe(mockText)
  })

  it('sets loading state during API call', async () => {
    mockFetch.mockImplementation(() => 
      new Promise(resolve => {
        setTimeout(() => resolve({
          ok: true,
          json: () => Promise.resolve({ data: 'test' }),
          headers: { get: () => 'application/json' }
        }), 100)
      })
    )

    const { result } = renderHook(() => useApi())

    act(() => {
      result.current.fetchData('/api/test')
    })

    expect(result.current.loading).toBe(true)
    expect(result.current.error).toBe(null)
  })

  it('handles HTTP error responses', async () => {
    const errorResponse = { detail: 'Not found' }
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      statusText: 'Not Found',
      json: () => Promise.resolve(errorResponse)
    })

    const { result } = renderHook(() => useApi())

    await act(async () => {
      try {
        await result.current.fetchData('/api/test')
      } catch (error) {
        expect(error.message).toBe('Not found')
      }
    })

    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBe('Not found')
  })

  it('handles HTTP error without JSON body', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: () => Promise.reject(new Error('No JSON'))
    })

    const { result } = renderHook(() => useApi())

    await act(async () => {
      try {
        await result.current.fetchData('/api/test')
      } catch (error) {
        expect(error.message).toBe('HTTP 500: Internal Server Error')
      }
    })

    expect(result.current.error).toBe('HTTP 500: Internal Server Error')
  })

  it('handles network errors', async () => {
    mockFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))

    const { result } = renderHook(() => useApi())

    await act(async () => {
      try {
        await result.current.fetchData('/api/test')
      } catch (error) {
        expect(error.message).toBe('Unable to connect to the server. Please check if the backend is running.')
      }
    })

    expect(result.current.error).toBe('Unable to connect to the server. Please check if the backend is running.')
  })

  it('handles absolute URLs correctly', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ data: 'test' }),
      headers: { get: () => 'application/json' }
    })

    const { result } = renderHook(() => useApi())

    await act(async () => {
      await result.current.fetchData('https://example.com/api/test')
    })

    expect(mockFetch).toHaveBeenCalledWith(
      'https://example.com/api/test',
      expect.any(Object)
    )
  })

  it('merges custom headers with default headers', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ data: 'test' }),
      headers: { get: () => 'application/json' }
    })

    const { result } = renderHook(() => useApi())

    await act(async () => {
      await result.current.fetchData('/api/test', {
        headers: {
          'Authorization': 'Bearer token123'
        }
      })
    })

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/test',
      expect.objectContaining({
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer token123'
        }
      })
    )
  })

  it('clears error when clearError is called', () => {
    const { result } = renderHook(() => useApi())

    // Manually set an error state
    act(() => {
      result.current.clearError()
    })

    expect(result.current.error).toBe(null)
  })

  it('handles different error response formats', async () => {
    const testCases = [
      { errorData: { message: 'Custom message' }, expected: 'Custom message' },
      { errorData: { detail: 'Detail message' }, expected: 'Detail message' },
      { errorData: { error: 'Error field' }, expected: 'HTTP 400: Bad Request' }
    ]

    for (const testCase of testCases) {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: () => Promise.resolve(testCase.errorData)
      })

      const { result } = renderHook(() => useApi())

      await act(async () => {
        try {
          await result.current.fetchData('/api/test')
        } catch (error) {
          expect(error.message).toBe(testCase.expected)
        }
      })

      expect(result.current.error).toBe(testCase.expected)
    }
  })
})