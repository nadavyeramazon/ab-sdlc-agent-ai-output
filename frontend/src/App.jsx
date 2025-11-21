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
      setMessage(`${data.message} (${data.timestamp})`)
    } catch (err) {
      setError(`Failed to fetch message: ${err.message}`)
    } finally {
      setLoading(false)
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
    </div>
  )
}

export default App
