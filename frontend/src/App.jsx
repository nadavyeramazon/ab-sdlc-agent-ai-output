import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [timestamp, setTimestamp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

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
      </div>
    </div>
  )
}

export default App
