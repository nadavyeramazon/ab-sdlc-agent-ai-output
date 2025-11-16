import { useState } from 'react'
import './App.css'

function App() {
  // Existing feature state
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Greeting feature state
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState(null)
  const [isLoadingGreet, setIsLoadingGreet] = useState(false)
  const [greetError, setGreetError] = useState(null)

  const fetchMessageFromBackend = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error('Failed to fetch data from backend')
      }
      
      const data = await response.json()
      setMessage(data.message)
      setTimestamp(data.timestamp)
    } catch (err) {
      console.error('Error fetching from backend:', err)
      setError('Cannot connect to backend. Please ensure the backend service is running.')
      setMessage('')
      setTimestamp('')
    } finally {
      setLoading(false)
    }
  }

  // Handle greeting submission
  const handleGreet = async () => {
    // Clear previous states
    setGreetError(null)
    setGreeting(null)
    
    // Client-side validation
    if (name.trim().length === 0) {
      setGreetError('Please enter your name')
      return
    }
    
    setIsLoadingGreet(true)
    
    try {
      const response = await fetch('http://localhost:8000/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() }),
      })
      
      const data = await response.json()
      
      if (response.ok) {
        setGreeting(data.greeting)
      } else {
        // Handle validation error from server
        setGreetError(data.detail || 'An error occurred')
      }
    } catch (err) {
      // Handle network error
      console.error('Error greeting user:', err)
      setGreetError('Unable to connect to server')
    } finally {
      setIsLoadingGreet(false)
    }
  }

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleGreet()
    }
  }

  return (
    <div className="App">
      <div className="container">
        <h1 className="heading">Hello World</h1>
        
        <button 
          className="fetch-button" 
          onClick={fetchMessageFromBackend}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        {message && !error && (
          <div className="response-container">
            <p className="message"><strong>Message:</strong> {message}</p>
            <p className="timestamp"><strong>Timestamp:</strong> {timestamp}</p>
          </div>
        )}

        {/* New Greeting Feature */}
        <div className="greeting-section">
          <div className="greeting-form">
            <div className="input-group">
              <label htmlFor="name-input" className="input-label">Name</label>
              <input
                id="name-input"
                type="text"
                className="name-input"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter your name"
                disabled={isLoadingGreet}
                aria-describedby={greetError ? "greet-error" : undefined}
              />
            </div>
            <button 
              className="greet-button"
              onClick={handleGreet} 
              disabled={isLoadingGreet}
            >
              {isLoadingGreet ? 'Loading...' : 'Greet Me'}
            </button>
          </div>
          
          {/* Display greeting response */}
          {greeting && (
            <div className="greeting-message">
              {greeting}
            </div>
          )}
          
          {/* Display error message */}
          {greetError && (
            <div id="greet-error" className="greeting-error" role="alert">
              {greetError}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
