/**
 * Green Theme Hello World Application
 * 
 * Main React component that displays a green-themed interface with:
 * - Static "Hello World" heading
 * - Button to fetch data from backend API
 * - Display of responses with loading and error states
 */

import { useState } from 'react'
import './App.css'

function App() {
  // State for "Get Message from Backend" functionality
  const [backendMessage, setBackendMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  /**
   * Fetch message from backend API
   * Handles loading state and error cases
   */
  const fetchBackendMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')
    
    try {
      // Use backend service name when running in Docker, localhost otherwise
      const baseUrl = window.location.hostname === 'localhost' 
        ? 'http://localhost:8000'
        : 'http://backend:8000'
      
      const response = await fetch(`${baseUrl}/api/hello`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBackendMessage(`${data.message} (at ${new Date(data.timestamp).toLocaleTimeString()})`)
    } catch (err) {
      setError(`Failed to fetch: ${err.message}`)
      console.error('Error fetching backend message:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        <p className="subtitle">Green Theme React Application</p>
        
        {/* Backend Message Section */}
        <button 
          className="fetch-button"
          onClick={fetchBackendMessage}
          disabled={loading}
          aria-label="Get Message from Backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {backendMessage && (
          <div className="message success" role="status">
            {backendMessage}
          </div>
        )}
        
        {error && (
          <div className="message error" role="alert">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
