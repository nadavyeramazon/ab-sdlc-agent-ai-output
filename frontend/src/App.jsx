import { useState } from 'react';
import './App.css';

function App() {
  const [backendMessage, setBackendMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchMessage = async () => {
    setLoading(true);
    setError('');
    setBackendMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/hello');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setBackendMessage(data.message || JSON.stringify(data));
    } catch (err) {
      setError(`Failed to fetch: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1>Hello World</h1>
        
        <button 
          onClick={fetchMessage} 
          disabled={loading}
          className="fetch-button"
        >
          Get Message from Backend
        </button>

        <div className="message-display">
          {loading && <p className="loading">Loading...</p>}
          {error && <p className="error">{error}</p>}
          {backendMessage && !loading && !error && (
            <p className="message">{backendMessage}</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
