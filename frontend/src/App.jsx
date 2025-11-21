import { useState } from 'react'

function App() {
  const [message, setMessage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // NEW state for greeting feature
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState(null)
  const [greetLoading, setGreetLoading] = useState(false)
  const [greetError, setGreetError] = useState(null)

  const handleGetMessage = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setMessage(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleGreet = async () => {
    // Client-side validation
    if (!name || !name.trim()) {
      setGreetError('Please enter your name')
      return
    }
    
    setGreetLoading(true)
    setGreetError(null)
    setGreeting(null)
    
    try {
      const response = await fetch('/api/greet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() })
      })
      
      if (!response.ok) {
        throw new Error('Unable to fetch greeting. Please try again.')
      }
      
      const data = await response.json()
      setGreeting(data)
      setName('') // Clear input after success
    } catch (err) {
      setGreetError(err.message)
    } finally {
      setGreetLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>Hello World</h1>
      
      <button onClick={handleGetMessage} disabled={loading}>
        Get Message from Backend
      </button>
      
      {loading && <p className="loading">Loading...</p>}
      
      {error && <p className="error">Error: {error}</p>}
      
      {message && (
        <div className="message">
          <p><strong>Message:</strong> {message.message}</p>
          <p><strong>Timestamp:</strong> {message.timestamp}</p>
        </div>
      )}

      {/* NEW: Personalized Greeting Section */}
      <div style={{ marginTop: '2rem', borderTop: '2px solid #8e44ad', paddingTop: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center', marginBottom: '1rem' }}>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            aria-label="Name input"
            style={{
              padding: '0.75rem',
              fontSize: '1rem',
              borderRadius: '5px',
              border: '2px solid #8e44ad',
              flex: '1',
              maxWidth: '250px'
            }}
            disabled={greetLoading}
          />
          <button onClick={handleGreet} disabled={greetLoading || !name.trim()}>
            Greet Me
          </button>
        </div>
        
        {greetLoading && <p className="loading">Loading...</p>}
        
        {greetError && <p className="error">{greetError}</p>}
        
        {greeting && (
          <div className="message">
            <p><strong>Greeting:</strong> {greeting.greeting}</p>
            <p><strong>Timestamp:</strong> {greeting.timestamp}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
