import { useState } from 'react'

function App() {
  // Existing Hello World feature state
  const [backendMessage, setBackendMessage] = useState('')
  const [messageLoading, setMessageLoading] = useState(false)
  const [messageError, setMessageError] = useState(null)

  // New greeting feature state
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  // Existing feature: Get message from backend
  const fetchBackendMessage = async () => {
    setMessageLoading(true)
    setMessageError(null)
    setBackendMessage('')

    try {
      const response = await fetch('http://localhost:8000/api/hello')
      const data = await response.json()
      
      if (response.ok) {
        setBackendMessage(data.message)
      } else {
        setMessageError('Failed to fetch message')
      }
    } catch (err) {
      setMessageError('Unable to connect to server')
    } finally {
      setMessageLoading(false)
    }
  }

  // New feature: Get personalized greeting
  const handleGreet = async () => {
    setError(null)
    setGreeting(null)
    
    if (name.trim().length === 0) {
      setError('Please enter your name')
      return
    }
    
    setIsLoading(true)
    
    try {
      const response = await fetch('http://localhost:8000/api/greet', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: name.trim() }),
      })
      
      const data = await response.json()
      
      if (response.ok) {
        setGreeting(data.greeting)
      } else {
        setError(data.detail || 'An error occurred')
      }
    } catch (err) {
      setError('Unable to connect to server')
    } finally {
      setIsLoading(false)
    }
  }

  // Handle Enter key press in name input
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      handleGreet()
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hello World</h1>
        <p className="subtitle">Purple-Themed React Application</p>
      </header>

      <main className="App-main">
        {/* Existing Feature: Get Message from Backend */}
        <section className="feature-section">
          <h2>Backend Integration</h2>
          <button 
            onClick={fetchBackendMessage} 
            disabled={messageLoading}
            className="btn btn-primary"
          >
            {messageLoading ? 'Loading...' : 'Get Message from Backend'}
          </button>
          
          {backendMessage && (
            <div className="message-display">
              <p>{backendMessage}</p>
            </div>
          )}
          
          {messageError && (
            <div className="error-display">
              <p>{messageError}</p>
            </div>
          )}
        </section>

        {/* New Feature: Personalized Greeting */}
        <section className="feature-section greeting-section">
          <h2>Personalized Greeting</h2>
          
          <div className="form-group">
            <label htmlFor="name-input">Name</label>
            <input
              id="name-input"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter your name"
              disabled={isLoading}
              className="input-field"
            />
          </div>
          
          <button 
            onClick={handleGreet} 
            disabled={isLoading || name.trim().length === 0}
            className="btn btn-primary"
          >
            {isLoading ? 'Loading...' : 'Greet Me'}
          </button>
          
          {greeting && (
            <div className="greeting-display">
              <p>{greeting}</p>
            </div>
          )}
          
          {error && (
            <div className="error-display">
              <p>{error}</p>
            </div>
          )}
        </section>
      </main>

      <footer className="App-footer">
        <p>© 2024 Purple Greeting App | React + FastAPI</p>
      </footer>
    </div>
  )
}

export default App