/**
 * Green Hello World API Frontend Application
 * Vanilla JavaScript implementation for interacting with FastAPI backend
 */

// API base URL - uses environment-aware configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'http://backend:8000';

/**
 * Make API request with error handling
 * @param {string} endpoint - API endpoint path
 * @returns {Promise<Object>} Response data
 */
async function makeRequest(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        console.error('API request failed:', error);
        return { 
            success: false, 
            error: error.message || 'Failed to connect to API' 
        };
    }
}

/**
 * Display response in a formatted way
 * @param {string} elementId - Target element ID
 * @param {Object} result - Result object from makeRequest
 */
function displayResponse(elementId, result) {
    const element = document.getElementById(elementId);
    
    if (!element) {
        console.error(`Element with id '${elementId}' not found`);
        return;
    }
    
    if (result.success) {
        element.textContent = JSON.stringify(result.data, null, 2);
        element.className = 'response-box success';
    } else {
        element.textContent = `Error: ${result.error}`;
        element.className = 'response-box error';
    }
}

/**
 * Update status indicator
 * @param {boolean} isHealthy - Health status
 * @param {string} message - Status message
 */
function updateStatus(isHealthy, message) {
    const indicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    if (indicator && statusText) {
        statusText.textContent = message;
        indicator.className = `status-indicator ${isHealthy ? 'healthy' : 'error'}`;
    }
}

/**
 * Check API health status
 */
async function checkHealth() {
    updateStatus(false, 'Checking...');
    const result = await makeRequest('/health');
    
    if (result.success) {
        updateStatus(true, `Healthy - ${result.data.service} v${result.data.version}`);
    } else {
        updateStatus(false, 'Unhealthy - Cannot connect to API');
    }
}

/**
 * Get welcome message from root endpoint
 */
async function getWelcome() {
    const result = await makeRequest('/');
    displayResponse('welcome-response', result);
}

/**
 * Get hello world message
 */
async function getHello() {
    const result = await makeRequest('/hello');
    displayResponse('hello-response', result);
}

/**
 * Get personalized greeting
 */
async function getPersonalizedGreeting() {
    const nameInput = document.getElementById('name-input');
    const name = nameInput.value.trim();
    
    if (!name) {
        displayResponse('personalized-response', {
            success: false,
            error: 'Please enter a name'
        });
        return;
    }
    
    const result = await makeRequest(`/hello/${encodeURIComponent(name)}`);
    displayResponse('personalized-response', result);
}

/**
 * Handle Enter key press in name input
 * @param {KeyboardEvent} event - Keyboard event
 */
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        getPersonalizedGreeting();
    }
}

/**
 * Initialize the application
 */
function init() {
    console.log('Green Hello World API Frontend initialized');
    console.log(`API Base URL: ${API_BASE_URL}`);
    
    // Check health on page load
    checkHealth();
    
    // Set up periodic health checks (every 30 seconds)
    setInterval(checkHealth, 30000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}