import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Frontend runs in browser, browser connects to localhost ports exposed by Docker
  // NEVER use Docker service names (like 'backend') - browser cannot resolve them
  const API_URL = 'http://localhost:8000';

  const fetchMessageFromBackend = async () => {
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await fetch(`${API_URL}/api/hello`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMessage(data.message || 'No message received');
    } catch (err) {
      setError(
        err.message || 'Failed to fetch message from backend. Please ensure the backend server is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="content-wrapper">
        <header className="app-header">
          <h1 className="main-title">Hello World</h1>
          <p className="subtitle">Green Theme Fullstack Application</p>
        </header>

        <main className="app-main">
          <div className="card">
            <button
              className="fetch-button"
              onClick={fetchMessageFromBackend}
              disabled={loading}
              aria-label="Get message from backend"
            >
              {loading ? (
                <span className="button-content">
                  <span className="spinner" aria-hidden="true"></span>
                  Loading...
                </span>
              ) : (
                'Get Message from Backend'
              )}
            </button>

            {message && (
              <div className="message-box success" role="status" aria-live="polite">
                <svg
                  className="icon"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z"
                    clipRule="evenodd"
                  />
                </svg>
                <p>{message}</p>
              </div>
            )}

            {error && (
              <div className="message-box error" role="alert" aria-live="assertive">
                <svg
                  className="icon"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-1.72 6.97a.75.75 0 10-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 101.06 1.06L12 13.06l1.72 1.72a.75.75 0 101.06-1.06L13.06 12l1.72-1.72a.75.75 0 10-1.06-1.06L12 10.94l-1.72-1.72z"
                    clipRule="evenodd"
                  />
                </svg>
                <p>{error}</p>
              </div>
            )}
          </div>

          <div className="info-section">
            <h2>Features</h2>
            <ul>
              <li>✓ Green-themed responsive design</li>
              <li>✓ Backend API integration</li>
              <li>✓ Loading states & error handling</li>
              <li>✓ Accessibility-compliant</li>
              <li>✓ Built with React 18 & Vite</li>
            </ul>
          </div>
        </main>

        <footer className="app-footer">
          <p>Powered by React + Vite | Green Theme v1.0.0</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
