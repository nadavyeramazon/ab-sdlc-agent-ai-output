/**
 * Main Application Component
 * 
 * Green-themed Hello World application with backend integration.
 * Features:
 * - Static "Hello World" heading
 * - Button to fetch message from backend API
 * - Loading state indicator during API call
 * - Error handling for network failures
 * - Timestamp display from backend response
 */

import { useState } from 'react'

function App() {
  // State management using React hooks
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API
   * Handles loading state, success, and error scenarios
   */
  const fetchMessage = async () => {
    // Reset previous state
    setLoading(true)
    setError('')
    setMessage('')
    setTimestamp('')

    try {
      // Make API call to backend with 5 second timeout
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
      
      // Update state with backend data
      setMessage(data.message)
      
      // Format timestamp to human-readable format
      const date = new Date(data.timestamp)
      const formattedTimestamp = date.toLocaleString('en-US', {
        dateStyle: 'medium',
        timeStyle: 'medium',
      })
      setTimestamp(formattedTimestamp)

    } catch (err) {
      // Handle different error scenarios
      if (err.name === 'AbortError') {
        setError('Request timeout. Please try again.')
      } else if (err.message.includes('fetch')) {
        setError('Failed to connect to backend. Please ensure the backend is running.')
      } else {
        setError(`Error: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <main className="content-wrapper">
        {/* Static Hello World heading */}
        <h1 className="main-heading">Hello World</h1>
        
        <p className="subtitle">Green Theme Fullstack Application</p>

        {/* Button to trigger backend API call */}
        <button 
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Loading indicator */}
        {loading && (
          <div className="loading-container" role="status" aria-live="polite">
            <div className="spinner"></div>
            <p className="loading-text">Fetching data from backend...</p>
          </div>
        )}

        {/* Error message display */}
        {error && (
          <div className="error-container" role="alert" aria-live="assertive">
            <p className="error-text">⚠️ {error}</p>
          </div>
        )}

        {/* Backend response display */}
        {message && !loading && !error && (
          <div className="message-container">
            <h2 className="message-heading">Response from Backend:</h2>
            <p className="message-text">{message}</p>
            {timestamp && (
              <p className="timestamp-text">
                <strong>Timestamp:</strong> {timestamp}
              </p>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
