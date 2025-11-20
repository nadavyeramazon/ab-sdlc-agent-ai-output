import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState('')
  const [greetingLoading, setGreetingLoading] = useState(false)
  const [greetingError, setGreetingError] = useState('')

  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setMessage('')

    try {
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setMessage(data.message || JSON.stringify(data))
    } catch (err) {
      setError(`Failed to fetch: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleGreet = async () => {
    // Clear previous messages
    setGreetingError('')
    setGreeting('')
    
    // Validate name
    const trimmedName = name.trim()
    if (!trimmedName) {
      setGreetingError('Please enter your name')
      return
    }
    
    // Set loading state
    setGreetingLoading(true)
    
    try {
      // Call POST /api/greet endpoint
      const response = await fetch('http://localhost:8000/api/greet', {
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
      setName('') // Clear input after success
    } catch (err) {
      setGreetingError(err.message || 'Failed to connect to server')
    } finally {
      setGreetingLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Hello World</h1>
        
        <button 
          className="button" 
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {loading && <p className="loading">Loading...</p>}
        
        {error && <p className="error">{error}</p>}
        
        {message && (
          <div className="response">
            <h2>Backend Response:</h2>
            <p>{message}</p>
          </div>
        )}

        {/* New Greeting Feature Section */}
        <div className="card">
          <h2>Personalized Greeting</h2>
          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            maxLength="100"
            className="input-field"
            aria-label="Enter your name"
          />
          <button onClick={handleGreet} disabled={greetingLoading}>
            {greetingLoading ? 'Loading...' : 'Greet Me'}
          </button>
          
          {greetingError && <p className="error">{greetingError}</p>}
          {greeting && <p className="success">{greeting}</p>}
        </div>
      </div>
    </div>
  )
}

export default App
