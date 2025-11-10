/**
 * Main Application Component
 * 
 * Purple-themed Hello World application with backend integration.
 * Features:
 * - Static "Hello World" heading
 * - Button to fetch message from backend API (/api/hello)
 * - User greeting form with name input
 * - Button to fetch personalized greeting from backend API (/api/greet)
 * - Loading state indicators during API calls
 * - Error handling for network failures
 * - Client-side validation for user input
 * - Timestamp display from backend responses
 */

import { useState } from 'react'

function App() {
  // State management for existing hello endpoint
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // State management for new greeting feature
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState('')
  const [greetingLoading, setGreetingLoading] = useState(false)
  const [greetingError, setGreetingError] = useState('')
  const [validationError, setValidationError] = useState('')

  /**
   * Fetch message from backend API (/api/hello)
   * Handles loading state, success, and error scenarios
   */
  const fetchMessage = async () => {
    // Reset previous state
    setLoading(true)
    setError('')
    setMessage('')
    setTimestamp('')

    try {
      // Make API call to backend with 5 second timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000)

      const response = await fetch('http://localhost:8000/api/hello', {
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      // Check if response is successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Parse JSON response
      const data = await response.json()
      
      // Update state with backend data
      setMessage(data.message)
      
      // Format timestamp to human-readable format
      const date = new Date(data.timestamp)
      const formattedTimestamp = date.toLocaleString('en-US', {
        dateStyle: 'medium',
        timeStyle: 'medium',
      })
      setTimestamp(formattedTimestamp)

    } catch (err) {
      // Handle different error scenarios
      if (err.name === 'AbortError') {
        setError('Request timeout. Please try again.')
      } else if (err.message.includes('fetch')) {
        setError('Failed to connect to backend. Please ensure the backend is running.')
      } else {
        setError(`Error: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  /**
   * Handle name input change
   * Clears validation error when user starts typing
   */
  const handleNameChange = (e) => {
    setName(e.target.value)
    // Clear validation error when user types
    if (validationError) {
      setValidationError('')
    }
  }

  /**
   * Validate name input
   * Returns true if valid, false if invalid
   */
  const validateName = () => {
    const trimmedName = name.trim()
    if (!trimmedName) {
      setValidationError('Please enter your name')
      return false
    }
    return true
  }

  /**
   * Fetch personalized greeting from backend API (/api/greet)
   * Validates input before making API call
   * Handles loading state, success, and error scenarios
   */
  const fetchGreeting = async () => {
    // Clear previous state
    setValidationError('')
    setGreetingError('')
    setGreeting('')

    // Client-side validation
    if (!validateName()) {
      return
    }

    // Set loading state
    setGreetingLoading(true)

    try {
      // Make POST API call to backend with 5 second timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000)

      const response = await fetch('http://localhost:8000/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() }),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      // Check if response is successful
      if (!response.ok) {
        // Handle 400 Bad Request (validation error from backend)
        if (response.status === 400) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Validation error')
        }
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Parse JSON response
      const data = await response.json()
      
      // Update state with greeting from backend
      setGreeting(data.greeting)

    } catch (err) {
      // Handle different error scenarios
      if (err.name === 'AbortError') {
        setGreetingError('Request timeout. Please try again.')
      } else if (err.message.includes('fetch') || err.message.includes('Failed to fetch')) {
        setGreetingError('Unable to connect to server. Please try again.')
      } else {
        setGreetingError(`Error: ${err.message}`)
      }
    } finally {
      setGreetingLoading(false)
    }
  }

  /**
   * Handle form submission (Enter key press)
   */
  const handleSubmit = (e) => {
    e.preventDefault()
    fetchGreeting()
  }

  return (
    <div className="app-container">
      <main className="content-wrapper">
        {/* Static Hello World heading */}
        <h1 className="main-heading">Hello World</h1>
        
        <p className="subtitle">Purple Theme Fullstack Application</p>

        {/* Button to trigger backend API call for existing hello endpoint */}
        <button 
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Get message from backend"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Loading indicator for hello endpoint */}
        {loading && (
          <div className="loading-container" role="status" aria-live="polite">
            <div className="spinner"></div>
            <p className="loading-text">Fetching data from backend...</p>
          </div>
        )}

        {/* Error message display for hello endpoint */}
        {error && (
          <div className="error-container" role="alert" aria-live="assertive">
            <p className="error-text">⚠️ {error}</p>
          </div>
        )}

        {/* Backend response display for hello endpoint */}
        {message && !loading && !error && (
          <div className="message-container">
            <h2 className="message-heading">Response from Backend:</h2>
            <p className="message-text">{message}</p>
            {timestamp && (
              <p className="timestamp-text">
                <strong>Timestamp:</strong> {timestamp}
              </p>
            )}
          </div>
        )}

        {/* User greeting section */}
        <section className="greeting-section">
          <h3>Get Your Personalized Greeting</h3>
          
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="name-input" className="input-label">
                Your Name
              </label>
              <input
                id="name-input"
                type="text"
                className="name-input"
                placeholder="Enter your name"
                value={name}
                onChange={handleNameChange}
                disabled={greetingLoading}
                aria-label="Your Name"
                aria-describedby={validationError ? 'validation-error' : undefined}
              />
              {validationError && (
                <p id="validation-error" className="validation-error" role="alert">
                  {validationError}
                </p>
              )}
            </div>

            <button
              type="button"
              className="greet-button"
              onClick={fetchGreeting}
              disabled={greetingLoading}
              aria-label="Greet Me"
            >
              {greetingLoading ? 'Loading...' : 'Greet Me'}
            </button>
          </form>

          {/* Loading indicator for greeting */}
          {greetingLoading && (
            <div className="loading-container" role="status" aria-live="polite">
              <div className="spinner"></div>
              <p className="loading-text">Getting your personalized greeting...</p>
            </div>
          )}

          {/* Error message for greeting */}
          {greetingError && (
            <div className="error-container" role="alert" aria-live="assertive">
              <p className="error-text">⚠️ {greetingError}</p>
            </div>
          )}

          {/* Greeting display */}
          {greeting && !greetingLoading && !greetingError && (
            <div className="greeting-container">
              <h4 className="greeting-heading">Your Personalized Greeting:</h4>
              <p className="greeting-text">{greeting}</p>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
