/**
 * Main App component for Hello World application.
 * Displays green-themed UI with backend integration.
 */

import { useState } from 'react'
import './App.css'

function App() {
  // State management for backend message, loading, and errors
  const [backendMessage, setBackendMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Get API URL from environment variable or fallback to localhost for local development
  // In Docker: VITE_API_URL=http://backend:8000 (uses Docker service name)
  // In local dev: Falls back to http://localhost:8000
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  /**
   * Fetch message from backend API.
   * Handles loading states, errors, and displays response.
   */
  const fetchBackendMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')
    setTimestamp('')

    try {
      const response = await fetch(`${API_URL}/api/hello`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBackendMessage(data.message)
      
      // Format timestamp to be more readable
      if (data.timestamp) {
        const date = new Date(data.timestamp)
        setTimestamp(date.toLocaleString())
      }
    } catch (err) {
      setError('Failed to fetch data from backend. Make sure the backend server is running.')
      console.error('Error fetching backend message:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">Hello World</h1>
          <p className="subtitle">Green Theme Fullstack Application</p>
        </header>

        <main className="main-content">
          <button 
            className="fetch-button"
            onClick={fetchBackendMessage}
            disabled={loading}
            aria-label="Get message from backend"
          >
            {loading ? 'Loading...' : 'Get Message from Backend'}
          </button>

          {loading && (
            <div className="loading" role="status" aria-label="Loading" aria-live="polite">
              <div className="spinner"></div>
              <p>Loading...</p>
            </div>
          )}

          {error && (
            <div className="error" role="alert" aria-live="assertive">
              <p>{error}</p>
            </div>
          )}

          {backendMessage && !loading && (
            <div className="response" role="status" aria-live="polite">
              <h2>Response from Backend:</h2>
              <p className="message">{backendMessage}</p>
              {timestamp && (
                <p className="timestamp">Timestamp: {timestamp}</p>
              )}
            </div>
          )}
        </main>

        <footer className="footer">
          <p>Powered by React + FastAPI</p>
        </footer>
      </div>
    </div>
  )
}

export default App
