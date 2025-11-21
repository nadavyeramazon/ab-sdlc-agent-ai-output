import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [timestamp, setTimestamp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const fetchMessage = async () => {
    try {
      setLoading(true);
      setError('');
      setMessage('');
      setTimestamp('');
      
      const response = await fetch(`${apiUrl}/api/hello`);
      
      if (!response.ok) {
        throw new Error('Failed to load message');
      }
      
      const data = await response.json();
      setMessage(data.message);
      setTimestamp(data.timestamp);
    } catch (err) {
      setError('Failed to load message');
      console.error('Error fetching message:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Hello World</h1>
        
        <button onClick={fetchMessage} disabled={loading}>
          Get Message from Backend
        </button>

        {loading && <p className="loading">Loading...</p>}
        
        {error && <p className="error">{error}</p>}
        
        {message && !loading && (
          <div className="message">
            <p className="message-text">{message}</p>
            <p className="timestamp">Timestamp: {new Date(timestamp).toLocaleString()}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
