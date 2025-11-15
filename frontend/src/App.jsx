import { useState } from 'react'
import './App.css'

/**
 * Main App component for Hello World application.
 * Features:
 * - Green themed UI
 * - Displays static Hello World heading
 * - Button to fetch message from backend API
 * - Loading state during API calls
 * - Error handling for failed requests
 */
function App() {
  // State management using React hooks
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Fetch message from backend API.
   * Handles loading state, success, and error scenarios.
   */
  const fetchMessage = async () => {
    // Reset states
    setLoading(true)
    setError(null)
    setMessage('')

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/api/hello')
      
      // Check if response is ok
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      // Parse JSON response
      const data = await response.json()
      
      // Update message state with backend response
      setMessage(data.message)
    } catch (err) {
      // Handle errors (network issues, backend down, etc.)
      console.error('Error fetching message:', err)
      setError('Failed to fetch message from backend. Please ensure the backend is running.')
    } finally {
      // Always reset loading state
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Main heading */}
        <h1 className="heading">Hello World</h1>
        
        {/* Button to trigger API call */}
        <button
          className="button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Loading indicator */}
        {loading && (
          <div className="loading" role="status" aria-live="polite">
            <div className="spinner"></div>
            <p>Fetching message...</p>
          </div>
        )}

        {/* Success message display */}
        {message && !loading && (
          <div className="message success" role="alert" aria-live="polite">
            <p>{message}</p>
          </div>
        )}

        {/* Error message display */}
        {error && !loading && (
          <div className="message error" role="alert" aria-live="assertive">
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
