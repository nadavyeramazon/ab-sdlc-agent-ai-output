/**
 * Purple Theme Hello World Application
 * 
 * Main React component that displays a purple-themed interface with:
 * - Static "Hello World" heading
 * - User greet input with personalized greeting from backend
 * - Button to fetch data from backend API (existing functionality)
 * - Display of responses with loading and error states
 */

import { useState } from 'react'
import './App.css'

function App() {
  // Existing state for "Get Message from Backend" functionality
  const [backendMessage, setBackendMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // New state for user greet functionality
  const [userName, setUserName] = useState('')
  const [greetingMessage, setGreetingMessage] = useState('')
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState('')

  /**
   * Fetch message from backend API (existing functionality)
   * Handles loading state and error cases
   */
  const fetchBackendMessage = async () => {
    setLoading(true)
    setError('')
    
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

  /**
   * Fetch personalized greeting from backend (new functionality)
   * Validates input and handles loading state and error cases
   */
  const fetchGreeting = async () => {
    // Client-side validation
    if (!userName.trim()) {
      setGreetError('Please enter your name')
      return
    }

    setGreetLoading(true)
    setGreetError('')
    setGreetingMessage('')
    
    try {
      // Use backend service name when running in Docker, localhost otherwise
      const baseUrl = window.location.hostname === 'localhost' 
        ? 'http://localhost:8000'
        : 'http://backend:8000'
      
      const response = await fetch(`${baseUrl}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: userName.trim() })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setGreetingMessage(`${data.greeting} (at ${new Date(data.timestamp).toLocaleTimeString()})`)
      setUserName('') // Clear input after successful greeting
    } catch (err) {
      setGreetError(`Failed to get greeting: ${err.message}`)
      console.error('Error fetching greeting:', err)
    } finally {
      setGreetLoading(false)
    }
  }

  /**
   * Handle Enter key press in name input
   * Uses onKeyDown (React 18 recommended) instead of deprecated onKeyPress
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      fetchGreeting()
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        <p className="subtitle">Purple Theme React Application</p>
        
        {/* New User Greet Section */}
        <div className="greet-section">
          <label htmlFor="name-input" className="input-label">
            Enter your name:
          </label>
          <div className="input-group">
            <input
              id="name-input"
              type="text"
              className="name-input"
              placeholder="Your name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={greetLoading}
              maxLength={100}
              aria-label="Enter your name"
            />
            <button 
              className="greet-button"
              onClick={fetchGreeting}
              disabled={greetLoading}
              aria-label="Greet Me"
            >
              {greetLoading ? 'Loading...' : 'Greet Me'}
            </button>
          </div>
          
          {greetingMessage && (
            <div className="message success" role="status">
              {greetingMessage}
            </div>
          )}
          
          {greetError && (
            <div className="message error" role="alert">
              {greetError}
            </div>
          )}
        </div>

        {/* Divider */}
        <div className="divider"></div>
        
        {/* Existing Backend Message Section */}
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
