/**
 * Main Application Component
 * 
 * Displays a green-themed Hello World page with backend integration.
 * Implements comprehensive state management for loading, error handling,
 * and dynamic content display with accessibility support.
 * 
 * Features:
 * - Responsive green-themed UI
 * - Asynchronous API calls with loading states
 * - Comprehensive error handling (network, HTTP, timeout)
 * - Accessibility compliance (ARIA labels, live regions)
 * - Request timeout (5 seconds)
 * - User-friendly error messages
 * - Environment-aware API URL configuration
 */

import { useState } from 'react'
import './App.css'

// Get API URL from environment variable with fallback to localhost
// When running in Docker Compose, VITE_API_URL will be http://backend:8000
// When running locally, it defaults to http://localhost:8000
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  // State management for backend response, loading status, and errors
  const [backendMessage, setBackendMessage] = useState(null)
  const [timestamp, setTimestamp] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Fetch message from backend API
   * 
   * Makes an HTTP GET request to the backend /api/hello endpoint
   * with timeout and error handling. Updates component state based
   * on the response.
   * 
   * Handles three types of errors:
   * 1. AbortError - Request timeout (5 seconds)
   * 2. Network errors - Unable to connect to backend
   * 3. HTTP errors - Non-200 status codes
   */
  const fetchMessage = async () => {
    // Reset all states before making new request
    setLoading(true)
    setError(null)
    setBackendMessage(null)
    setTimestamp(null)

    try {
      // Create AbortController for timeout functionality
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000)

      // Make API call with abort signal using environment-aware API URL
      const response = await fetch(`${API_URL}/api/hello`, {
        signal: controller.signal,
      })

      // Clear timeout if request completes before timeout
      clearTimeout(timeoutId)

      // Check if response is successful (status 200-299)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Parse JSON response
      const data = await response.json()
      
      // Update state with response data
      setBackendMessage(data.message)
      
      // Format timestamp for human-readable display
      if (data.timestamp) {
        const date = new Date(data.timestamp)
        setTimestamp(date.toLocaleString())
      }
    } catch (err) {
      // Handle different error types with specific messages
      if (err.name === 'AbortError') {
        setError('Request timed out. Please try again.')
      } else if (err.message.includes('Failed to fetch')) {
        setError('Unable to connect to backend. Please ensure the backend service is running.')
      } else {
        setError(`Error: ${err.message}`)
      }
      console.error('Fetch error:', err)
    } finally {
      // Always set loading to false, whether success or error
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Main heading */}
        <h1 className="heading">Hello World</h1>
        
        {/* Subtitle */}
        <p className="subtitle">Green Theme Fullstack Application</p>

        {/* Fetch button - disabled during loading to prevent duplicate requests */}
        <button
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get Message from Backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Loading indicator with spinner and text */}
        {loading && (
          <div className="loading" role="status" aria-live="polite">
            <div className="spinner" aria-hidden="true"></div>
            <p>Fetching data from backend...</p>
          </div>
        )}

        {/* Error message display - only shown when error exists */}
        {error && (
          <div className="error" role="alert">
            <p>{error}</p>
          </div>
        )}

        {/* Success message display - only shown when data is available */}
        {backendMessage && !loading && !error && (
          <div className="success" role="status" aria-live="polite">
            <h2>Response from Backend:</h2>
            <p className="message">{backendMessage}</p>
            {timestamp && (
              <p className="timestamp">
                <strong>Timestamp:</strong> {timestamp}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
