import { useState } from 'react'
import './GreetingForm.css'

function GreetingForm() {
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [timestamp, setTimestamp] = useState(null)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Client-side validation
    const trimmedName = name.trim()
    if (!trimmedName) {
      setError('Please enter your name')
      setGreeting(null)
      return
    }

    setLoading(true)
    setError(null)
    setGreeting(null)

    try {
      const response = await fetch(`${apiUrl}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: trimmedName }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`)
      }

      setGreeting(data.greeting)
      setTimestamp(new Date(data.timestamp).toLocaleString())
      setName('') // Clear input on success
    } catch (err) {
      const errorMessage = err.message || 'Failed to get greeting from backend'
      setError(errorMessage)
      console.error('Greet API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    setName(e.target.value)
    // Clear error when user starts typing
    if (error) {
      setError(null)
    }
  }

  return (
    <div className="greeting-form-section">
      <div className="greeting-divider">
        <span>Personalized Greeting</span>
      </div>

      <form className="greeting-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name-input" className="form-label">
            Enter Your Name
          </label>
          <input
            id="name-input"
            type="text"
            className="form-input"
            placeholder="e.g., John Doe"
            value={name}
            onChange={handleInputChange}
            disabled={loading}
            aria-label="Name input"
            aria-describedby={error ? 'error-message' : undefined}
            aria-invalid={error ? 'true' : 'false'}
          />
        </div>

        <button
          type="submit"
          className={`greet-button ${loading ? 'loading' : ''}`}
          disabled={loading}
          aria-label="Submit greeting request"
          aria-busy={loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              <span>Loading...</span>
            </>
          ) : (
            'Greet Me'
          )}
        </button>
      </form>

      {error && (
        <div 
          id="error-message"
          className="validation-error" 
          role="alert"
        >
          {error}
        </div>
      )}

      {greeting && !error && (
        <div className="greeting-response" role="status">
          <div className="greeting-message">
            <p>{greeting}</p>
          </div>
          {timestamp && (
            <div className="greeting-timestamp">
              <small>Received at: {timestamp}</small>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default GreetingForm
