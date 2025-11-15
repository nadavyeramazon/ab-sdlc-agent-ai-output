import { useState } from 'react'
import './App.css'

function App() {
  // State management using React hooks
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Fetches message from backend API.
   * Handles loading state, success, and error cases.
   */
  const fetchMessage = async () => {
    // Reset previous state
    setLoading(true)
    setError(null)
    setMessage('')
    setTimestamp('')

    try {
      // Use environment variable for API URL, fallback to localhost
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      
      // Fetch with 5-second timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000)

      const response = await fetch(`${apiUrl}/api/hello`, {
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
      // Handle different error types with user-friendly messages
      if (err.name === 'AbortError') {
        setError('Request timed out. Please check if the backend is running.')
      } else if (err.message.includes('Failed to fetch')) {
        setError('Cannot connect to backend. Please ensure the server is running on port 8000.')
      } else {
        setError(`Error: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  /**
   * Formats ISO 8601 timestamp to human-readable format.
   * @param {string} isoString - ISO 8601 formatted timestamp
   * @returns {string} - Formatted date string
   */
  const formatTimestamp = (isoString) => {
    if (!isoString) return ''
    try {
      const date = new Date(isoString)
      return date.toLocaleString('en-US', {
        dateStyle: 'medium',
        timeStyle: 'medium',
      })
    } catch {
      return isoString
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
          aria-live="polite"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Display backend message if available */}
        {message && (
          <div className="message-container" role="region" aria-label="Backend response">
            <p className="message">{message}</p>
            <p className="timestamp">
              Received at: {formatTimestamp(timestamp)}
            </p>
          </div>
        )}

        {/* Display error message if request failed */}
        {error && (
          <div className="error-container" role="alert">
            <p className="error-message">{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
