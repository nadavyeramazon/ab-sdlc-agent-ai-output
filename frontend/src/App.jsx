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

// Get API base URL from environment variable with fallback for local development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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
      // Make GET request to backend /api/hello endpoint using env variable
      const response = await fetch(`${API_BASE_URL}/api/hello`)
      
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
        
        {/* Button to trigger API call - shows loading state */}
        <button 
          className="button" 
          onClick={fetchMessage}
          disabled={loading}
          role={loading ? 'status' : undefined}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

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
