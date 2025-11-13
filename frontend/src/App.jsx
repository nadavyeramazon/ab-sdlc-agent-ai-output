import { useState } from 'react'
import './App.css'

// Get API URL from environment variable or use relative path for Nginx proxy
const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  // State management for existing "Get Message from Backend" feature
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // State management for new greeting feature
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState('')
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState('')

  /**
   * Fetch message from backend API (existing feature)
   * Handles loading state, success, and error cases
   */
  const fetchMessage = async () => {
    // Reset previous error and set loading state
    setError(null)
    setLoading(true)

    try {
      // Call backend API endpoint using environment-configured URL
      const response = await fetch(`${API_URL}/hello`)
      
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

  /**
   * Handle greeting request (new feature)
   * Validates input, calls greet API, and handles response
   */
  const handleGreet = async () => {
    // Client-side validation: check if name is empty or whitespace-only
    if (!name.trim()) {
      setGreetError('Please enter your name')
      setGreeting('')
      return
    }

    // Reset previous error and greeting
    setGreetError('')
    setGreeting('')
    setGreetLoading(true)

    try {
      // Call backend greet API endpoint
      const response = await fetch(`${API_URL}/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() }),
      })

      // Check if response is successful
      if (!response.ok) {
        // Handle validation errors from backend
        if (response.status === 400) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Invalid name provided')
        }
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Parse JSON response
      const data = await response.json()
      
      // Update greeting state with backend response
      setGreeting(data.greeting)
    } catch (err) {
      // Handle network errors and API failures
      console.error('Error fetching greeting:', err)
      setGreetError('Unable to fetch greeting. Please try again.')
    } finally {
      // Always reset loading state
      setGreetLoading(false)
    }
  }

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        {/* Existing "Get Message from Backend" feature */}
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

        {/* New greeting feature - separate section */}
        <div className="greeting-section">
          <input
            type="text"
            className="greeting-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            aria-label="Enter your name for personalized greeting"
          />
          
          <button
            className="greet-button"
            onClick={handleGreet}
            disabled={greetLoading}
            aria-label="Get personalized greeting"
          >
            {greetLoading ? 'Loading...' : 'Greet Me'}
          </button>

          {/* Display personalized greeting */}
          {greeting && (
            <div className="greeting-message" role="status">
              {greeting}
            </div>
          )}

          {/* Display greeting error message */}
          {greetError && (
            <div className="error" role="alert">
              {greetError}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
