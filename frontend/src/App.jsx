/**
 * Green Theme Hello World Frontend Application
 * 
 * Main application component featuring:
 * - Static "Hello World" heading with green theme
 * - Button to fetch data from backend API
 * - Loading state management
 * - Error handling
 * - Responsive design (320px - 1920px)
 */

import { useState } from 'react'

function App() {
  // State management using React hooks
  const [backendMessage, setBackendMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API
   * Handles loading state, success, and error cases
   */
  const fetchMessage = async () => {
    // Reset states
    setLoading(true)
    setError('')
    setBackendMessage('')
    setTimestamp('')

    try {
      // Fetch data from backend with timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout

      const response = await fetch('http://localhost:8000/api/hello', {
        signal: controller.signal
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Update state with backend response
      setBackendMessage(data.message)
      
      // Format timestamp to human-readable format
      const date = new Date(data.timestamp)
      setTimestamp(date.toLocaleString())
      
    } catch (err) {
      // Handle different error types
      if (err.name === 'AbortError') {
        setError('Request timed out. Please check if the backend is running.')
      } else if (err.message.includes('Failed to fetch')) {
        setError('Unable to connect to backend. Please ensure the backend service is running on port 8000.')
      } else {
        setError(`An error occurred: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="content-wrapper">
        {/* Main heading - US-1 AC1 */}
        <h1 className="main-heading">Hello World</h1>
        
        {/* Button to fetch backend data - US-3 AC1, AC2 */}
        <button 
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Display backend message - US-3 AC5 */}
        {backendMessage && (
          <div className="message-container">
            <p className="backend-message">{backendMessage}</p>
            {/* Display timestamp - US-3 AC6 */}
            <p className="timestamp">Received at: {timestamp}</p>
          </div>
        )}

        {/* Error display - US-3 AC7 */}
        {error && (
          <div className="error-container">
            <p className="error-message">{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
