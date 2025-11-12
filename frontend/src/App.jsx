/**
 * Main App component for Green Theme Hello World application
 * 
 * Features:
 * - Green-themed UI
 * - Static "Hello World" display
 * - Button to fetch data from backend
 * - Loading states
 * - Error handling
 */
import { useState } from 'react'
import './App.css'

// API URL configuration with fallback to localhost for local development
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  // State management
  const [backendMessage, setBackendMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API
   */
  const fetchBackendMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')

    try {
      const response = await fetch(`${API_URL}/api/hello`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBackendMessage(`${data.message} (${new Date(data.timestamp).toLocaleTimeString()})`)
    } catch (err) {
      setError(`Failed to fetch from backend: ${err.message}`)
      console.error('Error fetching backend message:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Static Hello World heading */}
        <h1 className="title">Hello World</h1>
        
        {/* Subtitle */}
        <p className="subtitle">Green Theme React Application</p>
        
        {/* Button to fetch backend data */}
        <button 
          className="fetch-button"
          onClick={fetchBackendMessage}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Display backend response */}
        {backendMessage && (
          <div className="message success" role="status">
            <p>{backendMessage}</p>
          </div>
        )}
        
        {/* Display error if any */}
        {error && (
          <div className="message error" role="alert">
            <p>{error}</p>
          </div>
        )}
        
        {/* Loading indicator */}
        {loading && (
          <div className="spinner" aria-label="Loading"></div>
        )}
      </div>
    </div>
  )
}

export default App
