/**
 * Purple Theme Hello World Application with Personalized Greeting
 * 
 * Main React component that displays a purple-themed interface with:
 * - Static "Hello World" heading
 * - Button to fetch data from backend API
 * - Personalized greeting feature with name input
 * - Display of responses with loading and error states
 */

import { useState } from 'react'
import './App.css'

// Security: Max name length to prevent DoS attacks
const MAX_NAME_LENGTH = 100

function App() {
  // State for "Get Message from Backend" functionality
  const [backendMessage, setBackendMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // State for "Greet Me" functionality
  const [name, setName] = useState('')
  const [greetingMessage, setGreetingMessage] = useState('')
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState('')

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

  /**
   * Send greeting request to backend
   * Validates input and handles responses
   */
  const handleGreet = async () => {
    // Client-side validation
    if (!name || !name.trim()) {
      setGreetError('Please enter your name')
      return
    }

    setGreetLoading(true)
    setGreetError('')
    setGreetingMessage('')
    
    try {
      const baseUrl = window.location.hostname === 'localhost'
        ? 'http://localhost:8000'
        : 'http://backend:8000'
      
      const response = await fetch(`${baseUrl}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setGreetingMessage(`${data.greeting} (at ${new Date(data.timestamp).toLocaleTimeString()})`)
      setName('') // Clear input after successful greeting
    } catch (err) {
      setGreetError(`Failed to get greeting: ${err.message}`)
      console.error('Error fetching greeting:', err)
    } finally {
      setGreetLoading(false)
    }
  }

  /**
   * Handle Enter key press in name input
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !greetLoading) {
      handleGreet()
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        <p className="subtitle">Purple Theme React Application</p>
        
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

        {/* Greeting Section */}
        <div className="greeting-section">
          <h2>Get Personalized Greeting</h2>
          
          <input
            type="text"
            className="name-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your name"
            maxLength={MAX_NAME_LENGTH}
            disabled={greetLoading}
            aria-label="Your name"
          />
          
          <button
            className="greet-button"
            onClick={handleGreet}
            disabled={greetLoading || !name.trim()}
            aria-label="Greet Me"
          >
            {greetLoading ? 'Loading...' : 'Greet Me'}
          </button>
          
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
      </div>
    </div>
  )
}

export default App
