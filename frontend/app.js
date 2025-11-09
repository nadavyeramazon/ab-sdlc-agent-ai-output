/**
 * Green Greeting Application - Frontend JavaScript
 * 
 * This application provides a user interface for interacting with the
 * Green Greeting API backend service.
 */

// Configuration
const CONFIG = {
    // Determine API URL based on environment
    // In Docker, backend service is named 'backend'
    // For local development, use localhost:8000
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : 'http://backend:8000',
    
    // Fallback to environment variable if available
    get apiUrl() {
        // Try to get from window object (can be set by Docker environment)
        if (window.API_URL) {
            return window.API_URL;
        }
        return this.API_BASE_URL;
    }
};

// DOM Elements
const elements = {
    healthStatus: document.getElementById('health-status'),
    refreshHealthBtn: document.getElementById('refresh-health'),
    nameInput: document.getElementById('name-input'),
    greetBtn: document.getElementById('greet-btn'),
    greetingResult: document.getElementById('greeting-result'),
    greetingMessage: document.querySelector('.greeting-message'),
    errorMessage: document.getElementById('error-message'),
    errorText: document.querySelector('.error-text'),
    apiEndpoint: document.getElementById('api-endpoint'),
    docsLink: document.getElementById('docs-link')
};

/**
 * Initialize the application
 */
function init() {
    // Set up API endpoint display
    elements.apiEndpoint.textContent = CONFIG.apiUrl;
    elements.docsLink.href = `${CONFIG.apiUrl}/docs`;
    
    // Set up event listeners
    setupEventListeners();
    
    // Initial health check
    checkHealth();
    
    console.log('Green Greeting App initialized');
}

/**
 * Set up event listeners for interactive elements
 */
function setupEventListeners() {
    // Health check refresh button
    elements.refreshHealthBtn.addEventListener('click', () => {
        checkHealth();
    });
    
    // Greet button
    elements.greetBtn.addEventListener('click', () => {
        handleGreeting();
    });
    
    // Enter key on name input
    elements.nameInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            handleGreeting();
        }
    });
    
    // Clear error when user starts typing
    elements.nameInput.addEventListener('input', () => {
        hideError();
    });
}

/**
 * Check the health status of the backend service
 */
async function checkHealth() {
    elements.healthStatus.innerHTML = '<div class="loading">Checking service health</div>';
    
    try {
        const response = await fetch(`${CONFIG.apiUrl}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayHealthStatus(data);
        
    } catch (error) {
        console.error('Health check failed:', error);
        displayHealthError(error);
    }
}

/**
 * Display health status information
 * @param {Object} data - Health status data from API
 */
function displayHealthStatus(data) {
    const statusClass = data.status === 'healthy' ? 'status-healthy' : 'status-unhealthy';
    
    elements.healthStatus.innerHTML = `
        <div class="health-status">
            <span class="status-indicator ${statusClass}"></span>
            <strong>Status:</strong> ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}
        </div>
        <div class="status-info">
            <p><strong>Service:</strong> ${data.service}</p>
            <p><strong>Version:</strong> ${data.version}</p>
            <p><strong>Last checked:</strong> ${new Date().toLocaleTimeString()}</p>
        </div>
    `;
}

/**
 * Display health check error
 * @param {Error} error - Error object
 */
function displayHealthError(error) {
    elements.healthStatus.innerHTML = `
        <div class="health-status">
            <span class="status-indicator status-unhealthy"></span>
            <strong>Status:</strong> Unavailable
        </div>
        <div class="status-info">
            <p style="color: #d32f2f;"><strong>Error:</strong> ${error.message}</p>
            <p><strong>Note:</strong> Backend service may be starting up or unavailable.</p>
        </div>
    `;
}

/**
 * Handle the greeting request
 */
async function handleGreeting() {
    const name = elements.nameInput.value.trim();
    
    // Validate input
    if (!name) {
        showError('Please enter your name');
        return;
    }
    
    if (name.length > 100) {
        showError('Name is too long (maximum 100 characters)');
        return;
    }
    
    // Disable button and show loading state
    elements.greetBtn.disabled = true;
    elements.greetBtn.textContent = 'Loading...';
    hideError();
    hideResult();
    
    try {
        const response = await fetch(`${CONFIG.apiUrl}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayGreeting(data);
        
    } catch (error) {
        console.error('Greeting request failed:', error);
        showError(error.message || 'Failed to get greeting. Please try again.');
    } finally {
        // Re-enable button
        elements.greetBtn.disabled = false;
        elements.greetBtn.textContent = 'Get Greeting';
    }
}

/**
 * Display the greeting message
 * @param {Object} data - Greeting data from API
 */
function displayGreeting(data) {
    elements.greetingMessage.textContent = data.message;
    elements.greetingResult.classList.remove('hidden');
    
    // Add a subtle animation
    elements.greetingResult.style.animation = 'none';
    setTimeout(() => {
        elements.greetingResult.style.animation = '';
    }, 10);
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    elements.errorText.textContent = message;
    elements.errorMessage.classList.remove('hidden');
    hideResult();
    
    // Add shake animation
    elements.errorMessage.style.animation = 'none';
    setTimeout(() => {
        elements.errorMessage.style.animation = '';
    }, 10);
}

/**
 * Hide error message
 */
function hideError() {
    elements.errorMessage.classList.add('hidden');
}

/**
 * Hide result message
 */
function hideResult() {
    elements.greetingResult.classList.add('hidden');
}

/**
 * Handle API connection errors gracefully
 */
window.addEventListener('error', (event) => {
    console.error('Application error:', event.error);
});

// Initialize the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        checkHealth,
        handleGreeting,
        displayGreeting,
        showError,
        hideError
    };
}
