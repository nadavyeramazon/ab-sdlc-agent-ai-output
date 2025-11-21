import { useState } from 'react'

function App() {
  const [message, setMessage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

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
    </div>
  )
}

export default App
