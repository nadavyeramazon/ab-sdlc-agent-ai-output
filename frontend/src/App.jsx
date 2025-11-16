import { useState } from 'react'
import './App.css'

function App() {
  // State for existing "Get Message from Backend" feature
  const [message, setMessage] = useState('')
  const [messageLoading, setMessageLoading] = useState(false)
  const [messageError, setMessageError] = useState('')

  // State for new "Greet Me" feature
  const [name, setName] = useState('')
  const [greetingMessage, setGreetingMessage] = useState('')
  const [greetingLoading, setGreetingLoading] = useState(false)
  const [greetingError, setGreetingError] = useState('')

  /**
   * Handle fetching message from backend
   * This is the EXISTING functionality that must remain unchanged
   */
  const handleGetMessage = async () => {
    setMessageLoading(true)
    setMessageError('')
    setMessage('')

    try {
      const response = await fetch('http://localhost:8000/api/hello')
      if (!response.ok) {
        throw new Error('Failed to fetch message')
      }
      const data = await response.json()
      setMessage(data.message)
    } catch (error) {
      setMessageError('Error: Could not connect to backend. Please make sure the server is running.')
      console.error('Error fetching message:', error)
    } finally {
      setMessageLoading(false)
    }
  }

  /**
   * Handle personalized greeting
   * This is the NEW functionality added per specification
   */
  const handleGreet = async () => {
    // Client-side validation
    if (!name || !name.trim()) {
      setGreetingError('Please enter your name')
      return
    }

    setGreetingLoading(true)
    setGreetingError('')
    setGreetingMessage('')

    try {
      const response = await fetch('http://localhost:8000/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to get greeting')
      }

      const data = await response.json()
      setGreetingMessage(data.greeting)
      // Keep the name in the input field for better UX
    } catch (error) {
      setGreetingError(
        error.message.includes('Failed to fetch')
          ? 'Error: Could not connect to backend. Please make sure the server is running.'
          : `Error: ${error.message}`
      )
      console.error('Error getting greeting:', error)
    } finally {
      setGreetingLoading(false)
    }
  }

  /**
   * Handle Enter key press in name input
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleGreet()
    }
  }

  return (
    <div className="App">
      <div className="container">
        {/* Header */}
        <header className="header">
          <h1>Hello World</h1>
          <p className="subtitle">Purple Theme Fullstack Application</p>
        </header>

        <div className="main-content">
          {/* Existing Feature: Get Message from Backend */}
          <div className="card">
            <h2>Backend Message</h2>
            <p className="description">
              Click the button below to fetch a message from the FastAPI backend.
            </p>
            
            <button
              className="button"
              onClick={handleGetMessage}
              disabled={messageLoading}
              aria-label="Get message from backend"
            >
              {messageLoading ? 'Loading...' : 'Get Message from Backend'}
            </button>

            {messageLoading && (
              <div className="loading" role="status" aria-live="polite">
                <div className="spinner"></div>
                <p>Loading...</p>
              </div>
            )}

            {message && !messageLoading && (
              <div className="result success" role="alert" aria-live="polite">
                <p className="result-message">{message}</p>
              </div>
            )}

            {messageError && !messageLoading && (
              <div className="result error" role="alert" aria-live="assertive">
                <p className="error-message">{messageError}</p>
              </div>
            )}
          </div>

          {/* New Feature: Personalized Greeting */}
          <div className="card">
            <h2>Personalized Greeting</h2>
            <p className="description">
              Enter your name to receive a personalized welcome message.
            </p>

            <div className="form-group">
              <label htmlFor="name-input" className="visually-hidden">
                Your name
              </label>
              <input
                id="name-input"
                type="text"
                className="input"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={greetingLoading}
                aria-label="Enter your name for greeting"
              />
            </div>

            <button
              className="button"
              onClick={handleGreet}
              disabled={greetingLoading}
              aria-label="Get personalized greeting"
            >
              {greetingLoading ? 'Loading...' : 'Greet Me'}
            </button>

            {greetingLoading && (
              <div className="loading" role="status" aria-live="polite">
                <div className="spinner"></div>
                <p>Loading...</p>
              </div>
            )}

            {greetingMessage && !greetingLoading && (
              <div className="result success" role="alert" aria-live="polite">
                <p className="result-message">{greetingMessage}</p>
              </div>
            )}

            {greetingError && !greetingLoading && (
              <div className="result error" role="alert" aria-live="assertive">
                <p className="error-message">{greetingError}</p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="footer">
          <p>
            Built with React + Vite and FastAPI
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App
