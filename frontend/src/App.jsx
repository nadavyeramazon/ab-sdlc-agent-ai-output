import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

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
      </div>
    </div>
  )
}

export default App
