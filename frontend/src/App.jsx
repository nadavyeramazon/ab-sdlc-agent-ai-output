/**
 * Main App component for Green Theme Hello World application.
 * 
 * Features:
 * - Displays a static "Hello World" heading with green theme
 * - Provides a button to fetch dynamic data from backend API
 * - Handles loading states and error scenarios
 * - Uses React hooks for state management
 */

import { useState } from 'react'
import './App.css'

function App() {
  // State management using React hooks
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API.
   * Handles loading state and error scenarios.
   */
  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setMessage('')

    try {
      // Make GET request to backend /api/hello endpoint
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setMessage(data.message)
    } catch (err) {
      // Handle network errors or API failures
      setError('Failed to fetch message from backend. Please ensure the backend is running.')
      console.error('Error fetching message:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Main heading with green theme */}
        <h1 className="heading">Hello World</h1>
        
        {/* Button to trigger API call */}
        <button 
          className="button" 
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Display loading state */}
        {loading && (
          <div className="loading" role="status">
            Loading...
          </div>
        )}

        {/* Display backend message on success */}
        {message && !loading && (
          <div className="message" role="alert">
            {message}
          </div>
        )}

        {/* Display error message on failure */}
        {error && !loading && (
          <div className="error" role="alert">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default App