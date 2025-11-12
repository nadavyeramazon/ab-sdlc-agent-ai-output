/**
 * Main App component for Purple Theme Hello World application
 * 
 * Features:
 * - Purple-themed UI
 * - Static "Hello World" display
 * - Button to fetch data from backend
 * - User greet form with personalized greeting
 * - Loading states
 * - Error handling
 */
import { useState } from 'react'
import './App.css'

// API URL configuration with fallback to localhost for local development
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  // State management for backend message feature
  const [backendMessage, setBackendMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // State management for user greet feature
  const [userName, setUserName] = useState('')
  const [greetMessage, setGreetMessage] = useState('')
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState('')

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

  /**
   * Fetch personalized greeting from backend
   */
  const fetchGreeting = async (e) => {
    e.preventDefault()
    
    // Client-side validation
    if (!userName.trim()) {
      setGreetError('Please enter your name')
      return
    }

    setGreetLoading(true)
    setGreetError('')
    setGreetMessage('')

    try {
      const response = await fetch(`${API_URL}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: userName.trim() }),
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setGreetMessage(data.greeting)
      // Clear input after successful greeting
      setUserName('')
    } catch (err) {
      setGreetError(`Failed to get greeting: ${err.message}`)
      console.error('Error fetching greeting:', err)
    } finally {
      setGreetLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Static Hello World heading */}
        <h1 className="title">Hello World</h1>
        
        {/* Subtitle */}
        <p className="subtitle">Purple Theme React Application</p>
        
        {/* Section 1: Original backend message feature */}
        <div className="section">
          <h2 className="section-title">Backend Message</h2>
          
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

        {/* Section 2: New user greet feature */}
        <div className="section">
          <h2 className="section-title">Personalized Greeting</h2>
          
          <form className="greet-form" onSubmit={fetchGreeting}>
            <input
              type="text"
              className="name-input"
              placeholder="Enter your name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              disabled={greetLoading}
              aria-label="Your name"
            />
            
            <button 
              type="submit"
              className="fetch-button"
              disabled={greetLoading || !userName.trim()}
              aria-label="Get personalized greeting"
            >
              {greetLoading ? 'Loading...' : 'Greet Me'}
            </button>
          </form>
          
          {/* Display personalized greeting */}
          {greetMessage && (
            <div className="message success" role="status">
              <p>{greetMessage}</p>
            </div>
          )}
          
          {/* Display greet error if any */}
          {greetError && (
            <div className="message error" role="alert">
              <p>{greetError}</p>
            </div>
          )}
          
          {/* Loading indicator for greet */}
          {greetLoading && (
            <div className="spinner" aria-label="Loading greeting"></div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
