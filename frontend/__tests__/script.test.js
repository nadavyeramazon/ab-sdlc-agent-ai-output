// Import the functions we want to test
// Since script.js doesn't export functions, we'll test the DOM interactions

describe('Green Greeter Frontend', () => {
  let container;

  beforeEach(() => {
    // Set up our document body
    document.body.innerHTML = `
      <div class="container">
        <div class="header">
          <h1>🌿 Green Greeter 🌱</h1>
          <p>Enter your name to receive a warm, eco-friendly greeting!</p>
        </div>
        
        <div class="input-section">
          <input type="text" id="nameInput" placeholder="Enter your name..." maxlength="100">
          <button id="greetButton">Get Green Greeting 🍃</button>
        </div>
        
        <div id="result" class="result hidden">
          <div class="greeting-card">
            <div id="greetingMessage" class="greeting-message"></div>
            <div id="timestamp" class="timestamp"></div>
          </div>
        </div>
        
        <div id="loading" class="loading hidden">
          <div class="spinner"></div>
          <p>Generating your green greeting...</p>
        </div>
        
        <div id="error" class="error hidden">
          <p>🌿 Oops! Something went wrong. Please try again.</p>
        </div>
      </div>
    `;

    // Mock the API configuration
    window.API_BASE_URL = 'http://localhost:8000';
    
    // Load our script by executing its content
    const scriptContent = `
      // Utility function to get API base URL
      function getApiBaseUrl() {
        // Check if we're running in a Docker environment
        if (window.location.hostname === 'localhost' && window.location.port === '8080') {
          // Running in Docker, use backend service name
          return 'http://backend:8000';
        }
        // Development or other environments
        return window.API_BASE_URL || 'http://localhost:8000';
      }

      // DOM elements
      const nameInput = document.getElementById('nameInput');
      const greetButton = document.getElementById('greetButton');
      const resultDiv = document.getElementById('result');
      const loadingDiv = document.getElementById('loading');
      const errorDiv = document.getElementById('error');
      const greetingMessage = document.getElementById('greetingMessage');
      const timestamp = document.getElementById('timestamp');

      // Show/hide functions
      function showElement(element) {
        element.classList.remove('hidden');
      }

      function hideElement(element) {
        element.classList.add('hidden');
      }

      // API call function
      async function greetUser(name) {
        const apiUrl = getApiBaseUrl();
        const response = await fetch(apiUrl + '/greet', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name: name })
        });
        
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        return await response.json();
      }

      // Main greeting function
      async function handleGreeting() {
        const name = nameInput.value.trim();
        
        // Hide previous results
        hideElement(resultDiv);
        hideElement(errorDiv);
        showElement(loadingDiv);
        
        try {
          const data = await greetUser(name);
          
          // Display results
          greetingMessage.textContent = data.greeting;
          timestamp.textContent = 'Generated at: ' + new Date(data.timestamp).toLocaleString();
          
          hideElement(loadingDiv);
          showElement(resultDiv);
          
          // Add animation class
          resultDiv.classList.add('animate');
          setTimeout(() => {
            resultDiv.classList.remove('animate');
          }, 500);
          
        } catch (error) {
          console.error('Error:', error);
          hideElement(loadingDiv);
          showElement(errorDiv);
        }
      }

      // Event listeners
      if (greetButton) {
        greetButton.addEventListener('click', handleGreeting);
      }
      
      if (nameInput) {
        nameInput.addEventListener('keypress', function(e) {
          if (e.key === 'Enter') {
            handleGreeting();
          }
        });
      }

      // Make functions available for testing
      window.testHelpers = {
        getApiBaseUrl,
        greetUser,
        handleGreeting,
        showElement,
        hideElement
      };
    `;
    
    eval(scriptContent);
  });

  afterEach(() => {
    document.body.innerHTML = '';
    jest.clearAllMocks();
  });

  test('should have all required DOM elements', () => {
    expect(document.getElementById('nameInput')).toBeTruthy();
    expect(document.getElementById('greetButton')).toBeTruthy();
    expect(document.getElementById('result')).toBeTruthy();
    expect(document.getElementById('loading')).toBeTruthy();
    expect(document.getElementById('error')).toBeTruthy();
  });

  test('should return correct API URL for different environments', () => {
    // Test localhost development
    window.location.hostname = 'localhost';
    window.location.port = '3000';
    expect(window.testHelpers.getApiBaseUrl()).toBe('http://localhost:8000');

    // Test Docker environment
    window.location.hostname = 'localhost';
    window.location.port = '8080';
    expect(window.testHelpers.getApiBaseUrl()).toBe('http://backend:8000');
  });

  test('should show and hide elements correctly', () => {
    const testElement = document.getElementById('result');
    
    // Initially hidden
    expect(testElement.classList.contains('hidden')).toBe(true);
    
    // Show element
    window.testHelpers.showElement(testElement);
    expect(testElement.classList.contains('hidden')).toBe(false);
    
    // Hide element
    window.testHelpers.hideElement(testElement);
    expect(testElement.classList.contains('hidden')).toBe(true);
  });

  test('should handle successful API response', async () => {
    const mockResponse = {
      greeting: 'Hello, Test User!',
      timestamp: '2023-12-01T10:00:00Z'
    };
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    const result = await window.testHelpers.greetUser('Test User');
    
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/greet',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: 'Test User' })
      }
    );
    
    expect(result).toEqual(mockResponse);
  });

  test('should handle API error response', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    });

    await expect(window.testHelpers.greetUser('Test User'))
      .rejects.toThrow('Network response was not ok');
  });

  test('should handle button click event', () => {
    const nameInput = document.getElementById('nameInput');
    const greetButton = document.getElementById('greetButton');
    
    nameInput.value = 'Test User';
    
    // Mock the API call
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        greeting: 'Hello, Test User!',
        timestamp: '2023-12-01T10:00:00Z'
      })
    });

    // Simulate button click
    greetButton.click();
    
    // Check that loading is shown
    const loadingDiv = document.getElementById('loading');
    expect(loadingDiv.classList.contains('hidden')).toBe(false);
  });

  test('should handle Enter key press in input field', () => {
    const nameInput = document.getElementById('nameInput');
    nameInput.value = 'Test User';
    
    // Mock the API call
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        greeting: 'Hello, Test User!',
        timestamp: '2023-12-01T10:00:00Z'
      })
    });

    // Simulate Enter key press
    const enterEvent = new KeyboardEvent('keypress', { key: 'Enter' });
    nameInput.dispatchEvent(enterEvent);
    
    // Check that loading is shown
    const loadingDiv = document.getElementById('loading');
    expect(loadingDiv.classList.contains('hidden')).toBe(false);
  });

  test('should trim whitespace from input', () => {
    const nameInput = document.getElementById('nameInput');
    nameInput.value = '  Test User  ';
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        greeting: 'Hello, Test User!',
        timestamp: '2023-12-01T10:00:00Z'
      })
    });

    const greetButton = document.getElementById('greetButton');
    greetButton.click();
    
    expect(fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        body: JSON.stringify({ name: 'Test User' })
      })
    );
  });
});
