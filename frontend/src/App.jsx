/**
 * Main App Component - Purple Theme Hello World Application
 * 
 * Features:
 * - Displays "Hello World" heading with purple theme
 * - Fetches dynamic message from backend API
 * - Personalized user greeting with POST /api/greet endpoint
 * - Shows loading state during API calls
 * - Handles errors gracefully
 * - Responsive layout with centered content
 */

import { useState } from 'react'
import './App.css'

function App() {
  // Existing state for backend message feature
  const [backendMessage, setBackendMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // New state for greeting feature
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState('')
  const [greetingTimestamp, setGreetingTimestamp] = useState('')
  const [greetingLoading, setGreetingLoading] = useState(false)
  const [greetingError, setGreetingError] = useState('')

  /**
   * Fetches message from backend API (existing feature)
   * Handles loading state and error cases
   */
  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')
    setTimestamp('')

    try {
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBackendMessage(data.message)
      setTimestamp(data.timestamp)
    } catch (err) {
      setError('Failed to fetch message from backend. Please ensure the backend service is running.')
      console.error('Error fetching message:', err)
    } finally {
      setLoading(false)
    }
  }

  /**
   * Fetches personalized greeting from backend API (new feature)
   * Validates input and handles loading state and error cases
   */
  const fetchGreeting = async () => {
    // Client-side validation: trim whitespace and check non-empty
    const trimmedName = name.trim()
    
    if (!trimmedName) {
      setGreetingError('Please enter your name')
      return
    }

    setGreetingLoading(true)
    setGreetingError('')
    setGreeting('')
    setGreetingTimestamp('')

    try {
      const response = await fetch('http://localhost:8000/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: trimmedName }),
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setGreeting(data.greeting)
      setGreetingTimestamp(data.timestamp)
      setName('') // Clear input field after successful greeting
    } catch (err) {
      setGreetingError('Failed to fetch greeting. Please ensure the backend service is running.')
      console.error('Error fetching greeting:', err)
    } finally {
      setGreetingLoading(false)
    }
  }

  /**
   * Handle form submission for greeting
   */
  const handleGreetSubmit = (e) => {
    e.preventDefault()
    fetchGreeting()
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        {/* Existing "Get Message from Backend" feature */}
        <button 
          className="fetch-button" 
          onClick={fetchMessage}
          disabled={loading}
          aria-label={loading ? 'Loading' : 'Get Message from Backend'}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {backendMessage && (
          <div className="backend-response">
            <p className="message">{backendMessage}</p>
            <p className="timestamp">Received at: {new Date(timestamp).toLocaleString()}</p>
          </div>
        )}

        {/* New greeting feature */}
        <div className="greeting-section">
          <form className="greeting-form" onSubmit={handleGreetSubmit}>
            <input
              type="text"
              className="greeting-input"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={greetingLoading}
              aria-label="Enter your name"
            />
            <button 
              type="submit"
              className="greet-button"
              disabled={greetingLoading}
              aria-label={greetingLoading ? 'Loading' : 'Greet Me'}
            >
              {greetingLoading ? 'Loading...' : 'Greet Me'}
            </button>
          </form>

          {greetingError && (
            <div className="error-message" role="alert">
              {greetingError}
            </div>
          )}

          {greeting && (
            <div className="greeting-response">
              <p className="greeting-text">{greeting}</p>
              <p className="timestamp">Greeted at: {new Date(greetingTimestamp).toLocaleString()}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
