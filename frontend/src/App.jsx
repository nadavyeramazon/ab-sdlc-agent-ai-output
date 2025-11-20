import { useState } from 'react'

function App() {
  const [loading, setLoading] = useState(false)
  const [backendMessage, setBackendMessage] = useState('')
  const [error, setError] = useState('')

  const fetchMessage = async () => {
    setLoading(true)
    setError('')
    setBackendMessage('')

    try {
      const response = await fetch('http://localhost:8000/api/hello')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBackendMessage(data.message || 'No message received')
    } catch (err) {
      setError(
        err.message === 'Failed to fetch'
          ? 'Unable to connect to backend. Please ensure the backend server is running on port 8000.'
          : `Error: ${err.message}`
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="heading">Hello World</h1>
        
        <button
          className="fetch-button"
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {backendMessage && !error && (
          <div className="backend-message">
            <p><strong>Backend Response:</strong></p>
            <p className="message-content">{backendMessage}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
