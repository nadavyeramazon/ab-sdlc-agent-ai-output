import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGetMessage = async () => {
    setLoading(true);
    setError(null);
    setMessage('');

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/hello`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch message from backend');
      }

      const data = await response.json();
      setMessage(`${data.message} (${data.timestamp})`);
    } catch (err) {
      setError('Failed to connect to backend. Please make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Hello World</h1>
      <button onClick={handleGetMessage}>Get Message from Backend</button>
      
      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">{error}</div>}
      {message && <div className="message">{message}</div>}
    </div>
  );
}

export default App;
