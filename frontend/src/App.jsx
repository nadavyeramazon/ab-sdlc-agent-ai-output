import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [greeting, setGreeting] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchGreeting()
  }, [])

  const fetchGreeting = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${apiUrl}/api/greeting`)
      if (!response.ok) {
        throw new Error('Failed to fetch greeting')
      }
      const data = await response.json()
      setGreeting(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Yellow Theme Hello World 🌟</h1>
        
        <div className="card">
          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Loading...</p>
            </div>
          )}
          
          {error && (
            <div className="error">
              <p>⚠️ Error: {error}</p>
              <button onClick={fetchGreeting} className="retry-button">
                Retry
              </button>
            </div>
          )}
          
          {greeting && !loading && (
            <div className="greeting">
              <h2>{greeting.message}</h2>
              <div className="info">
                <p><strong>Theme:</strong> {greeting.theme}</p>
                <p><strong>Timestamp:</strong> {new Date(greeting.timestamp).toLocaleString()}</p>
              </div>
              <button onClick={fetchGreeting} className="refresh-button">
                Refresh Greeting
              </button>
            </div>
          )}
        </div>

        <footer className="footer">
          <p>Powered by React + Vite + FastAPI</p>
        </footer>
      </div>
    </div>
  )
}

export default App
