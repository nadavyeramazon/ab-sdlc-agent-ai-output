import { useState } from 'react'
import './App.css'

function App() {
  // State management for API response, loading, and error states
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetches greeting message from backend API
   * Implements timeout and error handling
   */
  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setMessage('')
    setTimestamp('')

    try {
      // Create AbortController for request timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout

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
      } else {
        setError('Failed to fetch data. Please try again.')
      }
      console.error('Error fetching message:', err)
    } finally {
      setLoading(false)
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
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Display backend response */}
        {message && (
          <div className="response" role="status" aria-live="polite">
            <p className="message">{message}</p>
            <p className="timestamp">Timestamp: {timestamp}</p>
          </div>
        )}

        {/* Display error message */}
        {error && (
          <div className="error" role="alert" aria-live="assertive">
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
