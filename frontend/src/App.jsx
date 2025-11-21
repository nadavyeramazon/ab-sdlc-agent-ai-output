import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // NEW state for greeting feature
  const [userName, setUserName] = useState('');
  const [greetingResponse, setGreetingResponse] = useState('');
  const [greetingLoading, setGreetingLoading] = useState(false);
  const [greetingError, setGreetingError] = useState('');

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

  const handleGreeting = async () => {
    // Clear previous messages
    setGreetingResponse('');
    setGreetingError('');
    
    // Client-side validation
    if (!userName.trim()) {
      setGreetingError('Please enter your name');
      return;
    }
    
    setGreetingLoading(true);
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: userName.trim() }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get greeting');
      }
      
      const data = await response.json();
      setGreetingResponse(data.greeting);
    } catch (error) {
      setGreetingError(error.message || 'Network error. Please try again.');
    } finally {
      setGreetingLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Hello World</h1>
      <button onClick={handleGetMessage}>Get Message from Backend</button>
      
      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">{error}</div>}
      {message && <div className="message">{message}</div>}

      {/* NEW Greeting UI Section */}
      <div className="greeting-section" style={{ marginTop: '2rem' }}>
        <h2>Personalized Greeting</h2>
        
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
          <input
            type="text"
            placeholder="Enter your name"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            disabled={greetingLoading}
            style={{
              padding: '0.75rem',
              fontSize: '1rem',
              borderRadius: '4px',
              border: '2px solid #9b59b6',
              minWidth: '200px',
            }}
            aria-label="Your name"
          />
          
          <button 
            onClick={handleGreeting} 
            disabled={greetingLoading}
            style={{
              padding: '0.75rem 1.5rem',
              fontSize: '1rem',
              cursor: greetingLoading ? 'not-allowed' : 'pointer',
              opacity: greetingLoading ? 0.6 : 1,
            }}
          >
            {greetingLoading ? 'Loading...' : 'Greet Me'}
          </button>
        </div>
        
        {greetingResponse && (
          <p className="message" style={{ color: '#ffffff', fontWeight: 'bold' }}>
            {greetingResponse}
          </p>
        )}
        
        {greetingError && (
          <p style={{ color: '#ff6b6b', fontWeight: 'bold', marginTop: '1rem' }}>
            {greetingError}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
