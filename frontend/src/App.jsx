import { useState } from 'react'
import './App.css'

/**
 * Main application component for Green Theme Hello World
 * 
 * Features:
 * - Static "Hello World" display with green theme
 * - Interactive button to fetch data from backend API
 * - Loading state management during API calls
 * - Error handling for failed requests
 * - Responsive design for mobile and desktop
 */
function App() {
  // State management using React hooks
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API
   * Handles loading states, success, and error scenarios
   */
  const fetchMessage = async () => {
    // Clear previous state
    setMessage('')
    setTimestamp('')
    setError('')
    setLoading(true)

    try {
      // Determine API URL based on environment
      // In Docker, use service name; in local dev, use localhost
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      
      const response = await fetch(`${apiUrl}/api/hello`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Update state with response data
      setMessage(data.message)
      setTimestamp(data.timestamp)
    } catch (err) {
      // Handle errors with user-friendly message
      console.error('Error fetching message:', err)
      setError('Failed to connect to backend. Please ensure the backend service is running.')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Format timestamp for display
   * Converts ISO 8601 timestamp to readable format
   */
  const formatTimestamp = (isoString) => {
    if (!isoString) return ''
    try {
      const date = new Date(isoString)
      return date.toLocaleString()
    } catch {
      return isoString
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Main heading - Story 1: Static Frontend Display */}
        <h1 className="title">Hello World</h1>
        
        {/* Interactive button - Story 3: Frontend-Backend Integration */}
        <button 
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Display area for API response */}
        <div className="response-area">
          {/* Loading indicator */}
          {loading && (
            <div className="loading" role="status" aria-live="polite">
              <div className="spinner"></div>
              <p>Fetching message...</p>
            </div>
          )}

          {/* Error message display */}
          {error && (
            <div className="error" role="alert">
              <p>{error}</p>
            </div>
          )}

          {/* Success message display */}
          {message && !loading && !error && (
            <div className="success">
              <p className="message">{message}</p>
              <p className="timestamp">
                Received at: {formatTimestamp(timestamp)}
              </p>
            </div>
          )}
        </div>

        {/* Footer with API information */}
        <div className="footer">
          <p>Frontend: React 18 + Vite</p>
          <p>Backend: Python FastAPI</p>
        </div>
      </div>
    </div>
  )
}

export default App
