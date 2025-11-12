import { useState } from 'react'
import './App.css'
import HelloButton from './components/HelloButton'
import GreetingForm from './components/GreetingForm'
import { useApi } from './hooks/useApi'

function App() {
  const [backendMessage, setBackendMessage] = useState(null)
  const [timestamp, setTimestamp] = useState(null)
  const { loading, error, fetchData } = useApi()

  const handleGetMessage = async () => {
    const data = await fetchData('/api/hello')
    if (data) {
      setBackendMessage(data.message)
      setTimestamp(new Date(data.timestamp).toLocaleString())
    }
  }

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1 className="title">Hello World</h1>
          <p className="subtitle">Purple Theme Fullstack Application</p>
        </header>

        <main className="main-content">
          <HelloButton onClick={handleGetMessage} loading={loading} />

          {error && (
            <div className="error-message" role="alert">
              <strong>Error:</strong> {error}
            </div>
          )}

          {backendMessage && !error && (
            <div className="response-container" role="status">
              <div className="response-message">
                <strong>Backend Response:</strong>
                <p>{backendMessage}</p>
              </div>
              {timestamp && (
                <div className="response-timestamp">
                  <small>Received at: {timestamp}</small>
                </div>
              )}
            </div>
          )}

          {/* New Greeting Form Component */}
          <GreetingForm />
        </main>

        <footer className="footer">
          <p>Built with React & FastAPI</p>
        </footer>
      </div>
    </div>
  )
}

export default App
