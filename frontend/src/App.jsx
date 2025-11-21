import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  // New state for greeting feature
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
      setMessage(`${data.message} (${data.timestamp})`)
    } catch (err) {
      setError(`Failed to fetch message: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleGreet = async () => {
    // Clear previous messages
    setGreetingError('')
    setGreeting('')
    
    // Validate name is not empty
    if (!name.trim()) {
      setGreetingError('Please enter your name')
      return
    }
    
    setGreetingLoading(true)
    
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
      setGreeting(data.greeting)
    } catch (err) {
      setGreetingError(err.message || 'Network error. Please try again.')
    } finally {
      setGreetingLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>Hello World</h1>
      
      <button onClick={fetchMessage} disabled={loading}>
        Get Message from Backend
      </button>
      
      {loading && <p className="loading">Loading...</p>}
      
      {message && <p className="message">{message}</p>}
      
      {error && <p className="error">{error}</p>}

      {/* New Greeting Feature */}
      <div className="greeting-section">
        <input
          type="text"
          className="name-input"
          placeholder="Enter your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={greetingLoading}
        />
        <button 
          className="greet-button"
          onClick={handleGreet}
          disabled={greetingLoading}
        >
          {greetingLoading ? 'Loading...' : 'Greet Me'}
        </button>
      </div>

      {greeting && (
        <div className="greeting-message">
          {greeting}
        </div>
      )}

      {greetingError && (
        <div className="error-message">
          {greetingError}
        </div>
      )}
    </div>
  )
}

export default App
