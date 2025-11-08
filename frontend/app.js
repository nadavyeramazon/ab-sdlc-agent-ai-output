/**
 * Green Themed API Interface - Vanilla JavaScript
 * 
 * This script handles all interactions with the FastAPI backend.
 * No frameworks used - pure JavaScript for simplicity and performance.
 * 
 * Features:
 * - Automatic backend URL detection (Docker/localhost)
 * - Retry logic for failed requests
 * - Enhanced error handling and user feedback
 * - Connection status monitoring
 */

// Configuration
const API_CONFIGS = {
    // Try backend service name in Docker network first, fallback to localhost
    urls: [
        'http://backend:8000',      // Docker Compose internal network
        'http://localhost:8000',    // Local development
    ],
    retryAttempts: 2,
    retryDelay: 1000,  // milliseconds
    timeout: 10000,    // 10 seconds
};

let API_BASE_URL = API_CONFIGS.urls[1]; // Start with localhost for browser compatibility
let isBackendReachable = false;

// Utility Functions

/**
 * Display result in a result box with enhanced formatting
 * @param {string} elementId - The ID of the result box element
 * @param {string} message - The message to display
 * @param {string} type - The type of message ('success', 'error', 'loading')
 */
function displayResult(elementId, message, type = 'success') {
    const resultBox = document.getElementById(elementId);
    if (!resultBox) return;
    
    resultBox.className = `result-box show ${type}`;
    resultBox.textContent = message;
    
    // Auto-scroll to result if it's below the viewport
    if (type !== 'loading') {
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * Make an API request with retry logic
 * @param {string} endpoint - The API endpoint to call
 * @param {number} attempt - Current retry attempt number
 * @returns {Promise<Object>} The JSON response
 */
async function makeApiRequest(endpoint, attempt = 1) {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIGS.timeout);
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            signal: controller.signal,
            headers: {
                'Accept': 'application/json',
            }
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Mark backend as reachable on first success
        if (!isBackendReachable) {
            isBackendReachable = true;
            updateConnectionStatus(true);
        }
        
        return { success: true, data };
    } catch (error) {
        // Retry logic
        if (attempt < API_CONFIGS.retryAttempts) {
            console.log(`Attempt ${attempt} failed, retrying in ${API_CONFIGS.retryDelay}ms...`);
            await new Promise(resolve => setTimeout(resolve, API_CONFIGS.retryDelay));
            return makeApiRequest(endpoint, attempt + 1);
        }
        
        // All retries exhausted
        isBackendReachable = false;
        updateConnectionStatus(false);
        
        return { 
            success: false, 
            error: error.name === 'AbortError' 
                ? 'Request timeout - backend not responding' 
                : error.message 
        };
    }
}

/**
 * Update connection status indicator
 * @param {boolean} isConnected - Whether backend is reachable
 */
function updateConnectionStatus(isConnected) {
    const statusElement = document.getElementById('connectionStatus');
    if (!statusElement) return;
    
    if (isConnected) {
        statusElement.innerHTML = '🟢 Connected';
        statusElement.className = 'connection-status connected';
    } else {
        statusElement.innerHTML = '🔴 Disconnected';
        statusElement.className = 'connection-status disconnected';
    }
}

/**
 * Format JSON for display with syntax highlighting
 * @param {Object} data - The data to format
 * @returns {string} Formatted JSON string
 */
function formatJSON(data) {
    return JSON.stringify(data, null, 2);
}

/**
 * Show loading state on button
 * @param {HTMLElement} button - The button element
 * @param {boolean} isLoading - Whether to show loading state
 */
function setButtonLoading(button, isLoading) {
    if (!button) return;
    
    button.disabled = isLoading;
    if (isLoading) {
        button.dataset.originalText = button.textContent;
        button.classList.add('loading');
    } else {
        button.classList.remove('loading');
        if (button.dataset.originalText) {
            button.textContent = button.dataset.originalText;
        }
    }
}

// Event Handlers

/**
 * Handle health check button click
 */
async function handleHealthCheck() {
    const resultId = 'healthResult';
    const button = document.getElementById('healthCheckBtn');
    
    // Show loading state
    setButtonLoading(button, true);
    displayResult(resultId, '🔍 Checking health status...', 'loading');
    
    // Make API request
    const result = await makeApiRequest('/health');
    
    // Display result
    if (result.success) {
        const statusEmoji = result.data.status === 'healthy' ? '✅' : '⚠️';
        const message = [
            `${statusEmoji} Status: ${result.data.status.toUpperCase()}`,
            '',
            'Backend API is operational!',
            '',
            'Full Response:',
            formatJSON(result.data)
        ].join('\n');
        
        displayResult(resultId, message, 'success');
    } else {
        const message = [
            '❌ Health Check Failed',
            '',
            `Error: ${result.error}`,
            '',
            'Troubleshooting:',
            '• Ensure Docker Compose is running: docker compose up',
            '• Check backend logs: docker compose logs backend',
            `• Verify backend URL: ${API_BASE_URL}`,
            '• Check if port 8000 is accessible'
        ].join('\n');
        
        displayResult(resultId, message, 'error');
    }
    
    setButtonLoading(button, false);
}

/**
 * Handle hello world button click
 */
async function handleHelloWorld() {
    const resultId = 'helloWorldResult';
    const button = document.getElementById('helloWorldBtn');
    
    // Show loading state
    setButtonLoading(button, true);
    displayResult(resultId, '📡 Fetching message from backend...', 'loading');
    
    // Make API request
    const result = await makeApiRequest('/');
    
    // Display result
    if (result.success) {
        const message = [
            `🎉 ${result.data.message}`,
            '',
            'Successfully retrieved message from the backend!',
            '',
            'Full Response:',
            formatJSON(result.data)
        ].join('\n');
        
        displayResult(resultId, message, 'success');
    } else {
        const message = [
            '❌ Failed to Fetch Message',
            '',
            `Error: ${result.error}`,
            '',
            'Please ensure:',
            '• Backend service is running',
            '• Network connectivity is available',
            `• API endpoint is accessible: ${API_BASE_URL}/`
        ].join('\n');
        
        displayResult(resultId, message, 'error');
    }
    
    setButtonLoading(button, false);
}

/**
 * Handle personalized greeting
 */
async function handleGreeting() {
    const resultId = 'greetResult';
    const button = document.getElementById('greetBtn');
    const nameInput = document.getElementById('nameInput');
    const name = nameInput.value.trim();
    
    // Validate input
    if (!name) {
        displayResult(resultId, '⚠️ Please enter a name first!', 'error');
        nameInput.focus();
        return;
    }
    
    // Validate name length
    if (name.length > 50) {
        displayResult(resultId, '⚠️ Name is too long (maximum 50 characters)', 'error');
        return;
    }
    
    // Show loading state
    setButtonLoading(button, true);
    displayResult(resultId, `💬 Generating personalized greeting for ${name}...`, 'loading');
    
    // Make API request
    const result = await makeApiRequest(`/hello/${encodeURIComponent(name)}`);
    
    // Display result
    if (result.success) {
        const message = [
            `👋 ${result.data.message}`,
            '',
            `Personalized greeting generated successfully!`,
            '',
            'Full Response:',
            formatJSON(result.data)
        ].join('\n');
        
        displayResult(resultId, message, 'success');
        
        // Clear input on success
        // nameInput.value = '';
    } else {
        const message = [
            '❌ Failed to Generate Greeting',
            '',
            `Error: ${result.error}`,
            '',
            'Troubleshooting:',
            '• Check if the name contains valid characters',
            '• Ensure backend service is running',
            `• Verify endpoint: ${API_BASE_URL}/hello/{name}`
        ].join('\n');
        
        displayResult(resultId, message, 'error');
    }
    
    setButtonLoading(button, false);
}

/**
 * Check backend connectivity on page load
 */
async function checkInitialConnection() {
    console.log('🌿 Checking backend connectivity...');
    const result = await makeApiRequest('/health');
    
    if (result.success) {
        console.log('✅ Backend is reachable');
        updateConnectionStatus(true);
    } else {
        console.warn('⚠️ Backend is not reachable:', result.error);
        updateConnectionStatus(false);
    }
}

// Initialize Event Listeners

/**
 * Set up all event listeners when DOM is loaded
 */
function initializeEventListeners() {
    // Health Check button
    const healthCheckBtn = document.getElementById('healthCheckBtn');
    if (healthCheckBtn) {
        healthCheckBtn.addEventListener('click', handleHealthCheck);
    }
    
    // Hello World button
    const helloWorldBtn = document.getElementById('helloWorldBtn');
    if (helloWorldBtn) {
        helloWorldBtn.addEventListener('click', handleHelloWorld);
    }
    
    // Greet button
    const greetBtn = document.getElementById('greetBtn');
    if (greetBtn) {
        greetBtn.addEventListener('click', handleGreeting);
    }
    
    // Name input - allow Enter key to trigger greeting
    const nameInput = document.getElementById('nameInput');
    if (nameInput) {
        nameInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                handleGreeting();
            }
        });
        
        // Clear validation message on input
        nameInput.addEventListener('input', () => {
            const resultBox = document.getElementById('greetResult');
            if (resultBox && resultBox.classList.contains('error') && resultBox.textContent.includes('Please enter a name')) {
                resultBox.classList.remove('show');
            }
        });
    }
    
    // Check backend connection on load
    checkInitialConnection();
}

// Wait for DOM to be fully loaded before initializing
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeEventListeners);
} else {
    // DOM is already loaded
    initializeEventListeners();
}

// Log initialization
console.log('🌿 Green Themed API Interface initialized');
console.log(`📡 API Base URL: ${API_BASE_URL}`);
console.log(`🔄 Retry attempts: ${API_CONFIGS.retryAttempts}`);
console.log(`⏱️ Request timeout: ${API_CONFIGS.timeout}ms`);
