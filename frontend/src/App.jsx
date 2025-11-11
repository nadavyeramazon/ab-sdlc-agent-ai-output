/**
 * Main Application Component
 * 
 * Displays a green-themed Hello World page with backend integration.
 * Includes state management for loading, error handling, and dynamic content display.
 */

import { useState } from 'react'

function App() {
  // State management for backend response, loading status, and errors
  const [backendMessage, setBackendMessage] = useState(null)
  const [timestamp, setTimestamp] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Fetch message from backend API
   * Handles loading states, success responses, and error scenarios
   */
  const fetchMessage = async () => {
    // Reset states
    setLoading(true)
    setError(null)
    setBackendMessage(null)
    setTimestamp(null)

    try {
      // Make API call with timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000)

      const response = await fetch('http://localhost:8000/api/hello', {
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      // Check if response is successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Parse JSON response
      const data = await response.json()
      
      // Update state with response data
      setBackendMessage(data.message)
      
      // Format timestamp for display
      if (data.timestamp) {
        const date = new Date(data.timestamp)
        setTimestamp(date.toLocaleString())
      }
    } catch (err) {
      // Handle different error types
      if (err.name === 'AbortError') {
        setError('Request timed out. Please try again.')
      } else if (err.message.includes('Failed to fetch')) {
        setError('Unable to connect to backend. Please ensure the backend service is running.')
      } else {
        setError(`Error: ${err.message}`)
      }
      console.error('Fetch error:', err)
    } finally {
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

        {/* Fetch button */}
        <button
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get Message from Backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Loading indicator */}
        {loading && (
          <div className="loading" role="status" aria-live="polite">
            <div className="spinner"></div>
            <p>Fetching data from backend...</p>
          </div>
        )}

        {/* Error message display */}
        {error && (
          <div className="error" role="alert">
            <p>{error}</p>
          </div>
        )}

        {/* Success message display */}
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
