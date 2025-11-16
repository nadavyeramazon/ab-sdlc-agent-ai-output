import { useState } from 'react'
import './App.css'

// Get API URL from environment variable with fallback to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  // State for existing "Get Message from Backend" feature
  const [message, setMessage] = useState('')
  const [messageLoading, setMessageLoading] = useState(false)
  const [messageError, setMessageError] = useState('')

  // State for new greeting feature
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState('')
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState('')

  // Handler for existing "Get Message from Backend" feature
  const handleGetMessage = async () => {
    setMessageLoading(true)
    setMessageError('')
    
    try {
      const response = await fetch(`${API_URL}/api/hello`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch message')
      }
      
      const data = await response.json()
      setMessage(data.message)
    } catch (error) {
      setMessageError('Unable to connect to server')
      console.error('Error fetching message:', error)
    } finally {
      setMessageLoading(false)
    }
  }

  // Handler for new greeting feature
  const handleGreetMe = async () => {
    // Client-side validation for empty name
    const trimmedName = name.trim()
    if (!trimmedName) {
      setGreetError('Please enter your name')
      return
    }

    setGreetLoading(true)
    setGreetError('')
    setGreeting('')
    
    try {
      const response = await fetch(`${API_URL}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: trimmedName }),
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to get greeting')
      }
      
      const data = await response.json()
      setGreeting(data.greeting)
      // Optional: Clear input after successful submission
      setName('')
    } catch (error) {
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        setGreetError('Unable to connect to server')
      } else {
        setGreetError(error.message)
      }
      console.error('Error getting greeting:', error)
    } finally {
      setGreetLoading(false)
    }
  }

  // Handle Enter key press in name input
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleGreetMe()
    }
  }

  return (
    <div className="App">
      <h1>Hello World</h1>
      
      {/* Existing "Get Message from Backend" feature */}
      <div className="card">
        <button 
          onClick={handleGetMessage} 
          disabled={messageLoading}
          aria-label="Get message from backend"
        >
          {messageLoading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {message && (
          <p className="message" role="status" aria-live="polite">
            {message}
          </p>
        )}
        
        {messageError && (
          <p className="error" role="alert" aria-live="assertive">
            {messageError}
          </p>
        )}
      </div>

      {/* New greeting feature */}
      <div className="card greeting-section">
        <div className="input-group">
          <label htmlFor="name-input">Name</label>
          <input
            id="name-input"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your name"
            disabled={greetLoading}
            aria-label="Name input"
            aria-describedby={greetError ? 'greet-error' : undefined}
          />
        </div>
        
        <button 
          onClick={handleGreetMe} 
          disabled={greetLoading}
          aria-label="Greet me"
        >
          {greetLoading ? 'Loading...' : 'Greet Me'}
        </button>
        
        {greeting && (
          <p className="greeting" role="status" aria-live="polite">
            {greeting}
          </p>
        )}
        
        {greetError && (
          <p id="greet-error" className="error" role="alert" aria-live="assertive">
            {greetError}
          </p>
        )}
      </div>
    </div>
  )
}

export default App