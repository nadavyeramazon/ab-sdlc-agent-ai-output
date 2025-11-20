import { useState } from 'react';
import './App.css';

function App() {
  // State management for backend data, loading, and errors
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch message from backend API
  const fetchBackendMessage = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      const response = await fetch('http://localhost:8000/api/hello');
      
      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.status}`);
      }

      const data = await response.json();
      setMessage(data.message);
    } catch (err) {
      setError(err.message || 'Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="content">
        {/* Main heading */}
        <h1 className="heading">Hello World</h1>

        {/* Fetch button */}
        <button 
          className="fetch-button" 
          onClick={fetchBackendMessage}
          disabled={loading}
        >
          Get Message from Backend
        </button>

        {/* Loading indicator */}
        {loading && (
          <div className="loading">Loading...</div>
        )}

        {/* Backend message display */}
        {message && !loading && (
          <div className="message">
            <strong>Backend says:</strong> {message}
          </div>
        )}

        {/* Error message display */}
        {error && !loading && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
