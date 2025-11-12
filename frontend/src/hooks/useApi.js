import { useState, useCallback } from 'react'

// Ensure exact API endpoint matches specification
const API_BASE_URL = 'http://localhost:8000'

/**
 * Custom hook for making API calls with loading and error states
 * @returns {Object} { loading, error, fetchData, clearError }
 */
export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchData = useCallback(async (endpoint, options = {}) => {
    setLoading(true)
    setError(null)

    try {
      const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`
      
      const defaultOptions = {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      }

      const response = await fetch(url, defaultOptions)
      
      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`
        
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorData.message || errorMessage
        } catch {
          // If we can't parse error JSON, use the default message
        }
        
        throw new Error(errorMessage)
      }

      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        return await response.json()
      } else {
        return await response.text()
      }
    } catch (err) {
      let errorMessage = err.message
      
      // Enhanced error handling for better user experience
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        errorMessage = 'Unable to connect to the backend server at http://localhost:8000. Please ensure the backend is running and accessible.'
      } else if (err.message.includes('NetworkError') || err.message.includes('Failed to fetch')) {
        errorMessage = 'Network connection failed. Please check your internet connection and try again.'
      }
      
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return {
    loading,
    error,
    fetchData,
    clearError
  }
}