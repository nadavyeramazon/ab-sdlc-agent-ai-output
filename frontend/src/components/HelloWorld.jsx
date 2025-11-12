import { useState } from 'react'
import { useApi } from '../hooks/useApi'
import LoadingSpinner from './LoadingSpinner'
import ErrorMessage from './ErrorMessage'
import MessageDisplay from './MessageDisplay'
import './HelloWorld.css'

const HelloWorld = () => {
  const [message, setMessage] = useState('')
  const { loading, error, fetchData } = useApi()

  const handleGetMessage = async () => {
    try {
      const response = await fetchData('/api/hello')
      setMessage(response.message || 'Hello from backend!')
    } catch (err) {
      console.error('Failed to fetch message:', err)
    }
  }

  return (
    <main className="hello-world" role="main">
      <div className="container">
        <header className="hero-section">
          <h1 className="main-heading">
            Hello World
            <span className="emoji" role="img" aria-label="waving hand">
              👋
            </span>
          </h1>
          <p className="subtitle">
            Welcome to our green-themed fullstack application!
          </p>
        </header>

        <section className="action-section" aria-labelledby="action-heading">
          <h2 id="action-heading" className="sr-only">
            Backend Integration
          </h2>
          
          <button
            className="get-message-btn"
            onClick={handleGetMessage}
            disabled={loading}
            type="button"
            aria-describedby={error ? 'error-message' : undefined}
          >
            {loading ? (
              <>
                <LoadingSpinner size="sm" />
                <span>Getting Message...</span>
              </>
            ) : (
              'Get Message from Backend'
            )}
          </button>

          {error && (
            <ErrorMessage 
              id="error-message"
              message={error} 
              onRetry={handleGetMessage}
            />
          )}

          {message && !loading && !error && (
            <MessageDisplay message={message} />
          )}
        </section>

        <footer className="app-info">
          <p className="tech-stack">
            Built with{' '}
            <span className="tech-item">React 18</span>
            {' + '}
            <span className="tech-item">Vite</span>
            {' + '}
            <span className="tech-item">FastAPI</span>
          </p>
        </footer>
      </div>
    </main>
  )
}

export default HelloWorld