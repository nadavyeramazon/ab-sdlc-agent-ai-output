/**
 * Main App component for Hello World application
 * 
 * Features:
 * - Displays green-themed Hello World greeting
 * - Button to fetch message from backend API
 * - Loading state during API calls
 * - Error handling for failed requests
 * - Responsive, centered layout
 */

import { useState } from 'react'
import './App.css'

function App() {
  // State management using React hooks
  const [backendMessage, setBackendMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API
   * Handles loading state, success response, and errors
   */
  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')
    setTimestamp('')

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Update state with response data
      setBackendMessage(data.message)
      setTimestamp(data.timestamp)
    } catch (err) {
      // Handle errors (network issues, backend down, etc.)
      setError(`Failed to fetch message: ${err.message}. Make sure the backend is running on port 8000.`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="content">
        {/* Main heading */}
        <h1 className="main-heading">Hello World</h1>
        
        {/* Subtitle */}
        <p className="subtitle">Green-themed React Frontend</p>
        
        {/* Button to fetch backend message */}
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Display loading state */}
        {loading && <p className="loading-text">Loading...</p>}
        
        {/* Display backend message */}
        {backendMessage && (
          <div className="message-container">
            <p className="backend-message">{backendMessage}</p>
            <p className="timestamp">Timestamp: {timestamp}</p>
          </div>
        )}
        
        {/* Display error message */}
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
