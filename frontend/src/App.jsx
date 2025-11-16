import { useState } from 'react'
import './App.css'

// Backend API URL - configurable via environment variable
// Defaults to localhost:8000 for local development
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Maximum allowed name length to prevent DoS attacks
const MAX_NAME_LENGTH = 100

function App() {
  // State management for existing "Get Message from Backend" feature
  const [backendMessage, setBackendMessage] = useState('') // Stores message from backend
  const [loading, setLoading] = useState(false) // Tracks loading state during API call
  const [error, setError] = useState('') // Stores error messages

  // State management for new greeting feature
  const [name, setName] = useState('') // User's name input
  const [greeting, setGreeting] = useState(null) // Greeting response from API
  const [isLoading, setIsLoading] = useState(false) // Loading state for greeting request
  const [greetError, setGreetError] = useState(null) // Error state for greeting request

  /**
   * Fetches message from backend /api/hello endpoint
   * Implements loading states and error handling
   * EXISTING FUNCTIONALITY - PRESERVED
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

  /**
   * Handles greeting request to /api/greet endpoint
   * Implements client-side validation, loading states, and error handling
   * NEW FUNCTIONALITY - GREETING FEATURE
   */
  const handleGreet = async () => {
    // Clear previous state
    setGreetError(null)
    setGreeting(null)
    
    // Client-side validation - empty check
    if (name.trim().length === 0) {
      setGreetError('Please enter your name')
      return
    }
    
    // Client-side validation - max length check to prevent DoS
    if (name.trim().length > MAX_NAME_LENGTH) {
      setGreetError(`Name must be ${MAX_NAME_LENGTH} characters or less`)
      return
    }
    
    // Set loading state
    setIsLoading(true)
    
    try {
      // Make POST request to /api/greet
      const response = await fetch(`${API_URL}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() }),
      })
      
      // Parse JSON response
      const data = await response.json()
      
      // Check if response is successful
      if (response.ok) {
        setGreeting(data.greeting)
      } else {
        // Handle server-side validation errors (400 or 422)
        setGreetError(data.detail || 'An error occurred')
      }
    } catch (err) {
      // Handle network errors
      console.error('Error greeting user:', err)
      setGreetError('Unable to connect to server')
    } finally {
      // Always reset loading state
      setIsLoading(false)
    }
  }

  /**
   * Handles Enter key press in name input
   * Allows form submission via keyboard
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      handleGreet()
    }
  }

  return (
    <div className="App">
      <div className="container">
        {/* Main heading - Story 1 requirement */}
        <h1 className="hello-heading">Hello World</h1>
        
        {/* Subtitle with purple accent */}
        <p className="subtitle">A Purple-Themed Fullstack Application</p>
        
        {/* Divider line */}
        <div className="divider"></div>
        
        {/* EXISTING FEATURE: Get Message from Backend */}
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
        
        {/* NEW FEATURE: Personalized Greeting Section */}
        <div className="greeting-section">
          <h2>Get Personalized Greeting</h2>
          
          <div className="greeting-form">
            <div className="form-group">
              <label htmlFor="name-input">Name</label>
              <input
                id="name-input"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter your name"
                disabled={isLoading}
                maxLength={MAX_NAME_LENGTH}
                aria-label="Name input"
              />
              <small className="input-hint">
                {name.length}/{MAX_NAME_LENGTH} characters
              </small>
            </div>
            
            <button 
              className="greet-button"
              onClick={handleGreet}
              disabled={isLoading}
              aria-label="Get personalized greeting"
            >
              {isLoading ? 'Loading...' : 'Greet Me'}
            </button>
          </div>
          
          {/* Display greeting message */}
          {greeting && (
            <div className="greeting-message" role="alert">
              <p>{greeting}</p>
            </div>
          )}
          
          {/* Display error message for greeting */}
          {greetError && (
            <div className="message-box error" role="alert">
              <strong>Error:</strong>
              <p>{greetError}</p>
            </div>
          )}
        </div>
        
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
