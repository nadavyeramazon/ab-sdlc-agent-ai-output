/**
 * Main App component for Yellow Theme Hello World application
 * 
 * Features:
 * - Displays "Hello World" heading
 * - Button to fetch data from backend API
 * - Loading state during API calls
 * - Error handling with user-friendly messages
 * - Yellow-themed responsive design
 */

import { useState } from 'react'
import './App.css'

function App() {
  // State management
  const [backendMessage, setBackendMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetches data from backend /api/hello endpoint
   * Handles loading states and errors gracefully
   */
  const fetchBackendData = async () => {
    // Reset previous states
    setLoading(true)
    setError('')
    setBackendMessage('')
    setTimestamp('')

    try {
      // Get backend URL from environment or use default
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      
      const response = await fetch(`${apiUrl}/api/hello`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Update state with backend response
      setBackendMessage(data.message)
      setTimestamp(data.timestamp)
      
    } catch (err) {
      // Handle errors with user-friendly message
      console.error('Error fetching backend data:', err)
      setError('Failed to fetch data from backend. Please ensure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Main heading */}
        <h1 className="main-heading">Hello World</h1>
        
        {/* Subtitle */}
        <p className="subtitle">Yellow Theme Fullstack Application</p>
        
        {/* Fetch button */}
        <button 
          className="fetch-button" 
          onClick={fetchBackendData}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Loading indicator */}
        {loading && (
          <div className="loading" role="status" aria-live="polite">
            <div className="spinner"></div>
            <p>Fetching data from backend...</p>
          </div>
        )}
        
        {/* Error message */}
        {error && (
          <div className="error" role="alert">
            <p>❌ {error}</p>
          </div>
        )}
        
        {/* Backend response */}
        {backendMessage && !loading && (
          <div className="backend-response">
            <h2>Backend Response:</h2>
            <p className="message">{backendMessage}</p>
            <p className="timestamp">Timestamp: {new Date(timestamp).toLocaleString()}</p>
          </div>
        )}
        
        {/* Info footer */}
        <div className="info">
          <p>Frontend: React + Vite</p>
          <p>Backend: FastAPI</p>
          <p>Theme: Yellow (#FFEB3B)</p>
        </div>
      </div>
    </div>
  )
}

export default App
