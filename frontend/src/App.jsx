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
      setError(`Failed to fetch message: ${err.message}`);
      console.error('Error fetching from backend:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Hello World</h1>
        
        <button 
          onClick={fetchMessage} 
          disabled={loading}
          className="fetch-button"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {loading && (
          <div className="status-message loading">
            <span className="spinner"></span>
            Loading...
          </div>
        )}

        {error && (
          <div className="status-message error">
            ❌ {error}
          </div>
        )}

        {backendMessage && !loading && !error && (
          <div className="status-message success">
            ✅ {backendMessage}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
