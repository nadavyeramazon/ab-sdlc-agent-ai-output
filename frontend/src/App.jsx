import { useState } from 'react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  // Existing state for "Get Message from Backend" feature
  const [backendMessage, setBackendMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // State for personalized greeting feature
  const [name, setName] = useState('');
  const [greeting, setGreeting] = useState('');
  const [greetLoading, setGreetLoading] = useState(false);
  const [greetError, setGreetError] = useState('');

  // Existing handler for fetching hello message
  const fetchMessage = async () => {
    setLoading(true);
    setError('');
    setBackendMessage('');

    try {
      const response = await fetch(`${API_URL}/api/hello`);
      
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

  // New handler for personalized greeting
  const handleGreet = async () => {
    // Clear previous states
    setGreetError('');
    setGreeting('');
    
    // Validate name is not empty
    if (!name.trim()) {
      setGreetError('Please enter your name');
      return;
    }
    
    setGreetLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/api/greet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name.trim() }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get greeting');
      }
      
      const data = await response.json();
      setGreeting(data.greeting);
    } catch (error) {
      setGreetError(error.message || 'Failed to connect to backend');
    } finally {
      setGreetLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1>Hello World</h1>
        
        {/* Existing "Get Message from Backend" feature */}
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

        {/* New Greeting Section */}
        <div className="greeting-section">
          <h2>Get Personalized Greeting</h2>
          
          <div className="input-group">
            <label htmlFor="name-input">Enter Your Name:</label>
            <input
              id="name-input"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
              disabled={greetLoading}
              style={{
                padding: '0.5rem',
                fontSize: '1rem',
                borderRadius: '4px',
                border: '2px solid #9b59b6',
                width: '100%',
                maxWidth: '300px',
                marginTop: '0.5rem'
              }}
            />
          </div>
          
          <button
            onClick={handleGreet}
            disabled={greetLoading}
            style={{
              marginTop: '1rem',
              padding: '0.75rem 1.5rem',
              fontSize: '1rem',
              backgroundColor: '#9b59b6',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: greetLoading ? 'not-allowed' : 'pointer',
              opacity: greetLoading ? 0.6 : 1,
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              if (!greetLoading) {
                e.target.style.backgroundColor = '#8e44ad';
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 5px 15px rgba(155, 89, 182, 0.3)';
              }
            }}
            onMouseLeave={(e) => {
              if (!greetLoading) {
                e.target.style.backgroundColor = '#9b59b6';
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = 'none';
              }
            }}
          >
            {greetLoading ? 'Loading...' : 'Greet Me'}
          </button>
          
          {greeting && (
            <div className="greeting-message">
              {greeting}
            </div>
          )}
          
          {greetError && (
            <div className="error-message">
              Error: {greetError}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
