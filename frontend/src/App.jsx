import { useState } from 'react'
import './App.css'

// Backend API URL - configurable via environment variable
// Defaults to localhost:8000 for local development
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  // State management using React hooks
  const [backendMessage, setBackendMessage] = useState('') // Stores message from backend
  const [loading, setLoading] = useState(false) // Tracks loading state during API call
  const [error, setError] = useState('') // Stores error messages

  /**
   * Fetches message from backend /api/hello endpoint
   * Implements loading states and error handling
   */
  const fetchMessage = async () => {
    // Reset error state and set loading
    setError('')
    setLoading(true)
    
    try {
      // Make API call to backend
      const response = await fetch(`${API_URL}/api/hello`)
      
      // Check if response is successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      // Parse JSON response
      const data = await response.json()
      
      // Update state with backend message and timestamp
      setBackendMessage(`${data.message} (at ${new Date(data.timestamp).toLocaleString()})`)
    } catch (err) {
      // Handle errors gracefully
      console.error('Error fetching message:', err)
      setError(`Failed to fetch message from backend. Please ensure the backend is running at ${API_URL}`)
      setBackendMessage('') // Clear any previous message
    } finally {
      // Always reset loading state
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <div className="container">
        {/* Main heading - Story 1 requirement */}
        <h1 className="hello-heading">Hello World</h1>
        
        {/* Subtitle with green accent */}
        <p className="subtitle">A Green-Themed Fullstack Application</p>
        
        {/* Divider line */}
        <div className="divider"></div>
        
        {/* Button to trigger API call - Story 3 requirement */}
        <button 
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Fetch message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Display backend message if available */}
        {backendMessage && (
          <div className="message-box success" role="alert">
            <strong>Backend Response:</strong>
            <p>{backendMessage}</p>
          </div>
        )}
        
        {/* Display error message if API call fails - Story 3 requirement */}
        {error && (
          <div className="message-box error" role="alert">
            <strong>Error:</strong>
            <p>{error}</p>
          </div>
        )}
        
        {/* Footer with tech stack information */}
        <footer className="footer">
          <p>Built with React 18 + Vite + FastAPI</p>
          <p className="small">Frontend: localhost:3000 | Backend: localhost:8000</p>
        </footer>
      </div>
    </div>
  )
}

export default App
