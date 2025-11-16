import { useState } from 'react'
import './App.css'

/**
 * Main App component for Purple Theme Hello World application.
 * 
 * Features:
 * - Displays "Hello World" heading
 * - Button to fetch data from backend API (existing feature)
 * - Personalized greeting form (new feature)
 * - Loading states during API calls
 * - Error handling for network failures
 * - Client-side validation with user-friendly messages
 * - Purple-themed responsive UI
 * - WCAG AA compliant accessibility
 */
function App() {
  // State management for existing "Get Message from Backend" feature
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // State management for new greeting feature
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState('')
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState('')
  const [validationError, setValidationError] = useState('')

  /**
   * Fetch data from backend /api/hello endpoint.
   * Handles loading states and error scenarios.
   * This is the EXISTING feature - preserved unchanged.
   */
  const fetchMessage = async () => {
    // Reset previous error and message
    setError('')
    setMessage('')
    setLoading(true)

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Display message and timestamp from backend
      setMessage(`${data.message} (Received at: ${new Date(data.timestamp).toLocaleString()})`)
    } catch (err) {
      // Handle network errors or backend unavailability
      setError('Failed to fetch data from backend. Please ensure the backend service is running.')
      console.error('Fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  /**
   * Handle input change for name field.
   * Clears validation error when user types.
   * Implements real-time feedback for better UX.
   */
  const handleNameChange = (e) => {
    const value = e.target.value
    setName(value)
    
    // Clear validation and error messages when user starts typing
    if (validationError) {
      setValidationError('')
    }
    if (greetError) {
      setGreetError('')
    }
  }

  /**
   * Validate name input on the client side.
   * Prevents unnecessary API calls for invalid input.
   * 
   * @returns {boolean} True if validation passes, false otherwise
   */
  const validateName = () => {
    const trimmedName = name.trim()
    
    if (!trimmedName) {
      setValidationError('Please enter your name')
      return false
    }
    
    if (trimmedName.length > 100) {
      setValidationError('Name is too long (maximum 100 characters)')
      return false
    }
    
    return true
  }

  /**
   * Fetch personalized greeting from backend /api/greet endpoint.
   * NEW FEATURE - implements personalized user greeting.
   * Includes comprehensive error handling and user feedback.
   */
  const fetchGreeting = async () => {
    // Client-side validation before API call
    if (!validateName()) {
      return
    }

    const trimmedName = name.trim()

    // Reset previous states
    setGreetError('')
    setGreeting('')
    setValidationError('')
    setGreetLoading(true)

    try {
      // Call backend API with POST request
      const response = await fetch('http://localhost:8000/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: trimmedName }),
      })

      if (!response.ok) {
        // Handle backend validation errors (400) or other errors
        if (response.status === 400) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Invalid input')
        } else if (response.status === 422) {
          throw new Error('Invalid request format. Please check your input.')
        } else if (response.status >= 500) {
          throw new Error('Server error. Please try again later.')
        }
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Display greeting from backend
      setGreeting(data.greeting)
      
      // Optional: Clear input after successful greeting for better UX
      setName('')
    } catch (err) {
      // Handle different types of errors with appropriate messages
      if (err.message.includes('Name cannot be empty')) {
        setGreetError('Please enter a valid name')
      } else if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
        setGreetError('Failed to fetch greeting. Please check your connection and try again.')
      } else {
        setGreetError(err.message || 'Failed to fetch greeting. Please try again.')
      }
      console.error('Greet error:', err)
    } finally {
      setGreetLoading(false)
    }
  }

  /**
   * Handle Enter key press in input field.
   * Provides keyboard accessibility for form submission.
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !greetLoading) {
      fetchGreeting()
    }
  }

  return (
    <div className="app-container">
      <div className="content">
        {/* Main heading */}
        <h1 className="heading">Hello World</h1>
        
        {/* EXISTING FEATURE: Button to fetch backend data */}
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
          aria-label="Fetch message from backend API"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {/* Loading indicator for existing feature */}
        {loading && (
          <div className="loading" role="status" aria-live="polite">
            <div className="spinner" aria-hidden="true"></div>
            <p>Fetching data from backend...</p>
          </div>
        )}
        
        {/* Success message display for existing feature */}
        {message && !loading && (
          <div className="message-display success" role="status" aria-live="polite">
            <p>{message}</p>
          </div>
        )}
        
        {/* Error message display for existing feature */}
        {error && !loading && (
          <div className="message-display error" role="alert" aria-live="assertive">
            <p>{error}</p>
          </div>
        )}

        {/* NEW FEATURE: Greeting section - visually separated */}
        <div className="greeting-section">
          <h2>Get a Personalized Greeting</h2>
          
          {/* Input field for name with accessibility attributes */}
          <input
            type="text"
            className="greeting-input"
            placeholder="Enter your name"
            value={name}
            onChange={handleNameChange}
            onKeyPress={handleKeyPress}
            disabled={greetLoading}
            aria-label="Enter your name for personalized greeting"
            aria-describedby={validationError ? "validation-error" : undefined}
            aria-invalid={!!validationError}
            maxLength={100}
          />
          
          {/* Validation error message */}
          {validationError && (
            <div 
              id="validation-error" 
              className="validation-message" 
              role="alert"
              aria-live="polite"
            >
              {validationError}
            </div>
          )}
          
          {/* Greet Me button */}
          <button
            className="greet-button"
            onClick={fetchGreeting}
            disabled={greetLoading}
            aria-label="Get personalized greeting"
          >
            {greetLoading ? 'Loading...' : 'Greet Me'}
          </button>
          
          {/* Loading indicator for greeting feature */}
          {greetLoading && (
            <div className="loading" role="status" aria-live="polite">
              <div className="spinner" aria-hidden="true"></div>
              <p>Fetching your greeting...</p>
            </div>
          )}
          
          {/* Greeting display */}
          {greeting && !greetLoading && (
            <div className="greeting-display" role="status" aria-live="polite">
              <p>{greeting}</p>
            </div>
          )}
          
          {/* Error message display for greeting feature */}
          {greetError && !greetLoading && (
            <div className="message-display error" role="alert" aria-live="assertive">
              <p>{greetError}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
