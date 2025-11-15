/**
 * Main App component for Purple Theme Hello World application.
 * 
 * Features:
 * - Displays a static "Hello World" heading with purple theme
 * - Provides a button to fetch dynamic data from backend API
 * - Provides personalized greeting feature with name input
 * - Handles loading states and error scenarios
 * - Uses React hooks for state management
 */

import { useState } from 'react'
import './App.css'

// Get API base URL from environment variable with fallback for local development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  // State management for existing "Get Message from Backend" feature
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // State management for new personalized greeting feature
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState('')
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState('')
  const [validationError, setValidationError] = useState('')

  /**
   * Fetch message from backend API.
   * Handles loading state and error scenarios.
   * This is the existing feature - unchanged functionality.
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

  /**
   * Handle name input change.
   * Clears validation error when user starts typing.
   */
  const handleNameChange = (e) => {
    setName(e.target.value)
    // Clear validation error when user starts typing
    if (validationError) {
      setValidationError('')
    }
  }

  /**
   * Fetch personalized greeting from backend API.
   * Validates input and handles loading state and error scenarios.
   */
  const fetchGreeting = async () => {
    // Client-side validation: check if name is empty or whitespace-only
    const trimmedName = name.trim()
    if (!trimmedName) {
      setValidationError('Please enter your name')
      return
    }

    setGreetLoading(true)
    setGreetError('')
    setGreeting('')
    setValidationError('')

    try {
      // Make POST request to backend /api/greet endpoint
      const response = await fetch(`${API_BASE_URL}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: trimmedName }),
      })
      
      if (!response.ok) {
        // Handle validation errors from backend
        if (response.status === 400) {
          const errorData = await response.json()
          setValidationError(errorData.detail || 'Invalid input')
        } else {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        return
      }
      
      const data = await response.json()
      setGreeting(data.greeting)
    } catch (err) {
      // Handle network errors or API failures
      setGreetError('Unable to connect. Please try again.')
      console.error('Error fetching greeting:', err)
    } finally {
      setGreetLoading(false)
    }
  }

  /**
   * Handle Enter key press in input field.
   * Triggers greeting fetch when Enter is pressed.
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      fetchGreeting()
    }
  }

  return (
    <div className="app">
      <div className="container">
        {/* Main heading with purple theme */}
        <h1 className="heading">Hello World</h1>
        
        {/* Existing feature: Button to trigger API call - shows loading state */}
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

        {/* New feature: Personalized greeting section */}
        <div className="greeting-section">
          {/* Input field for user name with accessible label */}
          <label htmlFor="name-input" className="sr-only">Enter your name</label>
          <input
            id="name-input"
            type="text"
            className="input-field"
            placeholder="Enter your name"
            value={name}
            onChange={handleNameChange}
            onKeyPress={handleKeyPress}
            disabled={greetLoading}
            aria-label="Enter your name"
            aria-invalid={!!validationError}
            aria-describedby={validationError ? 'validation-error' : undefined}
          />

          {/* Display validation error */}
          {validationError && (
            <div id="validation-error" className="validation-error" role="alert">
              {validationError}
            </div>
          )}

          {/* Button to trigger greeting - shows loading state */}
          <button 
            className="button" 
            onClick={fetchGreeting}
            disabled={greetLoading}
            role={greetLoading ? 'status' : undefined}
          >
            {greetLoading ? 'Loading...' : 'Greet Me'}
          </button>

          {/* Display personalized greeting on success */}
          {greeting && !greetLoading && (
            <div className="greeting" role="alert">
              {greeting}
            </div>
          )}

          {/* Display error message on failure */}
          {greetError && !greetLoading && (
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
