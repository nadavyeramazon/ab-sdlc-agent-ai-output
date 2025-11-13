import { useState } from 'react'
import './App.css'

function App() {
  // State management using React hooks
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Fetch message from backend API
   * Handles loading state, success, and error cases
   */
  const fetchMessage = async () => {
    // Reset previous error and set loading state
    setError(null)
    setLoading(true)

    try {
      // Call backend API endpoint
      const response = await fetch('http://localhost:8000/api/hello')
      
      // Check if response is successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      // Parse JSON response
      const data = await response.json()
      
      // Update message state with backend response
      setMessage(data.message)
    } catch (err) {
      // Handle network errors and API failures
      console.error('Error fetching message:', err)
      setError('Failed to fetch message. Please try again.')
      setMessage('') // Clear any previous message
    } finally {
      // Always reset loading state
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Display backend message */}
        {message && (
          <div className="message" role="status">
            {message}
          </div>
        )}
        
        {/* Display error message */}
        {error && (
          <div className="error" role="alert">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
