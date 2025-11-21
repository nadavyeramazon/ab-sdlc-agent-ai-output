/**
 * Main App component for Yellow Theme Hello World application.
 * 
 * Features:
 * - Displays static "Hello World" heading
 * - Button to fetch dynamic message from backend API
 * - Loading state indicator during API requests
 * - Error handling for failed API calls
 * - Yellow-themed responsive design
 */

import { useState } from 'react'

function App() {
  // State management using React hooks
  const [backendMessage, setBackendMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API.
   * Handles loading states, success, and error scenarios.
   */
  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    
    try {
      // Call backend API endpoint
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Update state with backend response
      setBackendMessage(data.message)
      setTimestamp(data.timestamp)
    } catch (err) {
      // Handle network errors or backend unavailability
      setError(`Failed to fetch from backend: ${err.message}`)
      setBackendMessage('')
      setTimestamp('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Static Hello World heading */}
        <h1 className="title">Hello World</h1>
        
        {/* Button to trigger backend API call */}
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Display backend response */}
        {backendMessage && (
          <div className="backend-response">
            <p className="message">{backendMessage}</p>
            <p className="timestamp">Timestamp: {timestamp}</p>
          </div>
        )}
        
        {/* Display error message if API call fails */}
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
