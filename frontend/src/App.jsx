import { useState } from 'react'
import './App.css'

/**
 * Main App component for Green Theme Hello World application.
 * 
 * Features:
 * - Displays "Hello World" heading
 * - Button to fetch data from backend API
 * - Loading state during API calls
 * - Error handling for network failures
 * - Green-themed responsive UI
 */
function App() {
  // State management for API interaction
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch data from backend /api/hello endpoint.
   * Handles loading states and error scenarios.
   */
  const fetchMessage = async () => {
    // Reset previous error and message
    setError('')
    setMessage('')
    setLoading(true)

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Display message and timestamp from backend
      setMessage(`${data.message} (Received at: ${new Date(data.timestamp).toLocaleString()})`)
    } catch (err) {
      // Handle network errors or backend unavailability
      setError('Failed to fetch data from backend. Please ensure the backend service is running.')
      console.error('Fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="content">
        {/* Main heading */}
        <h1 className="heading">Hello World</h1>
        
        {/* Button to fetch backend data */}
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Loading indicator */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Fetching data from backend...</p>
          </div>
        )}
        
        {/* Success message display */}
        {message && !loading && (
          <div className="message-display success">
            <p>{message}</p>
          </div>
        )}
        
        {/* Error message display */}
        {error && !loading && (
          <div className="message-display error">
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
