/**
 * Main App component for Hello World fullstack application.
 * 
 * Features:
 * - Green-themed UI with centered content
 * - Static "Hello World" heading
 * - Button to fetch message from backend API
 * - Loading states and error handling
 * - Displays backend response with timestamp
 */

import { useState } from 'react'

function App() {
  // State management
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API.
   * Handles loading states, errors, and success responses.
   */
  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setMessage('')
    setTimestamp('')

    try {
      // Create abort controller for timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000)

      const response = await fetch('http://localhost:8000/api/hello', {
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setMessage(data.message)
      setTimestamp(data.timestamp)
    } catch (err) {
      if (err.name === 'AbortError') {
        setError('Request timed out. Please try again.')
      } else if (err.message.includes('Failed to fetch')) {
        setError('Unable to connect to backend. Please ensure the backend service is running.')
      } else {
        setError(`Error: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="content">
        <h1 className="heading">Hello World</h1>
        
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {loading && (
          <div className="loading" role="status">
            <div className="spinner"></div>
            <p>Fetching message from backend...</p>
          </div>
        )}

        {error && (
          <div className="error" role="alert">
            <p>{error}</p>
          </div>
        )}

        {message && !error && (
          <div className="success">
            <h2>{message}</h2>
            {timestamp && (
              <p className="timestamp">
                Timestamp: {new Date(timestamp).toLocaleString()}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
