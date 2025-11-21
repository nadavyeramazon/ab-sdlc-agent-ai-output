import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchMessage = async () => {
    // Clear previous state
    setLoading(true);
    setError('');
    setMessage('');

    try {
      // Fetch from backend API
      const response = await fetch('http://localhost:8000/api/hello');
      
      if (!response.ok) {
        throw new Error('Failed to fetch from backend');
      }

      const data = await response.json();
      
      // Display message and timestamp from backend
      setMessage(`${data.message} (Received at: ${data.timestamp})`);
    } catch (err) {
      // Handle connection errors
      setError('Failed to connect to backend. Make sure the backend server is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Hello World</h1>
        <p className="subtitle">Fullstack Demo Application</p>
        
        <button 
          className="button" 
          onClick={fetchMessage}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {/* Display loading state */}
        {loading && (
          <div className="loading">
            Connecting to backend...
          </div>
        )}

        {/* Display error message */}
        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {/* Display success message */}
        {message && (
          <div className="message-box">
            <h3>Response from Backend:</h3>
            <p>{message}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
