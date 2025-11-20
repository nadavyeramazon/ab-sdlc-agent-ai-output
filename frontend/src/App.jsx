import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGetMessage = async () => {
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await fetch('/api/hello');
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      
      // Display message and timestamp from response
      if (data.message) {
        const timestamp = data.timestamp ? new Date(data.timestamp).toLocaleString() : new Date().toLocaleString();
        setMessage(`${data.message} (${timestamp})`);
      } else {
        setMessage('Response received from backend');
      }
    } catch (err) {
      console.error('Failed to fetch from backend:', err);
      setError('Failed to connect to backend. Please ensure the server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Hello World</h1>
        
        <button 
          onClick={handleGetMessage} 
          disabled={loading}
          className="btn-primary"
        >
          {loading ? 'Loading...' : 'Get Message from Backend'}
        </button>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Fetching message from backend...</p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>{error}</p>
          </div>
        )}

        {message && !loading && !error && (
          <div className="message">
            <h2>Backend Response:</h2>
            <p>{message}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
