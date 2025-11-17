/**
 * Main App component with yellow theme and backend integration.
 * 
 * Features:
 * - Static "Hello World" heading
 * - Button to fetch data from backend API
 * - Loading state indicator
 * - Error handling with user-friendly messages
 * - Responsive centered layout
 */
import { useState } from 'react'

function App() {
  // State management using React hooks
  const [backendMessage, setBackendMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Get backend URL from environment variable or use default
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

  /**
   * Fetch message from backend API.
   * Handles loading states and errors.
   */
  const fetchBackendMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')

    try {
      const response = await fetch(`${BACKEND_URL}/api/hello`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBackendMessage(`${data.message} (${data.timestamp})`)
    } catch (err) {
      setError(`Failed to fetch from backend: ${err.message}`)
      console.error('Error fetching backend message:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="content-card">
        {/* Static Hello World heading */}
        <h1 className="main-heading">Hello World</h1>
        
        <p className="subtitle">
          Welcome to the Yellow Theme Fullstack Application
        </p>

        {/* Button to fetch backend data */}
        <button 
          className="fetch-button"
          onClick={fetchBackendMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Loading indicator */}
        {loading && (
          <div className="loading-spinner" data-testid="loading-indicator">
            <div className="spinner"></div>
          </div>
        )}

        {/* Backend response display */}
        {backendMessage && (
          <div className="backend-message" data-testid="backend-message">
            <strong>Backend Response:</strong>
            <p>{backendMessage}</p>
          </div>
        )}

        {/* Error message display */}
        {error && (
          <div className="error-message" data-testid="error-message">
            <strong>Error:</strong>
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
