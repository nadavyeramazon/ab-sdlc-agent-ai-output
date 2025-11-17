/**
 * Main App Component - Green Theme Hello World Application
 * 
 * Features:
 * - Displays "Hello World" heading with green theme
 * - Fetches dynamic message from backend API
 * - Shows loading state during API calls
 * - Handles errors gracefully
 * - Responsive layout with centered content
 */

import { useState } from 'react'
import './App.css'

function App() {
  const [backendMessage, setBackendMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetches message from backend API
   * Handles loading state and error cases
   */
  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')
    setTimestamp('')

    try {
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBackendMessage(data.message)
      setTimestamp(data.timestamp)
    } catch (err) {
      setError('Failed to fetch message from backend. Please ensure the backend service is running.')
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
          aria-label={loading ? 'Loading' : 'Get Message from Backend'}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {backendMessage && (
          <div className="backend-response">
            <p className="message">{backendMessage}</p>
            <p className="timestamp">Received at: {new Date(timestamp).toLocaleString()}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
