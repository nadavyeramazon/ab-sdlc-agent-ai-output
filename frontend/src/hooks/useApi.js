import { useState } from 'react'

/**
 * Custom hook for making API calls to the backend
 * @returns {Object} { loading, error, fetchData }
 */
export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const fetchData = async (endpoint) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setLoading(false)
      return data
    } catch (err) {
      const errorMessage = err.message || 'Failed to fetch data from backend'
      setError(errorMessage)
      setLoading(false)
      console.error('API Error:', err)
      return null
    }
  }

  return { loading, error, fetchData }
}
