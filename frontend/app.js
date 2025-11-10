/**
 * Green Theme Hello World - Frontend JavaScript
 * 
 * Handles interaction with backend API and UI updates
 */

// Configuration
const CONFIG = {
    BACKEND_URL: 'http://localhost:8000',
    API_HELLO_ENDPOINT: '/api/hello'
};

// DOM Elements
const elements = {
    fetchButton: document.getElementById('fetchButton'),
    loading: document.getElementById('loading'),
    response: document.getElementById('response'),
    error: document.getElementById('error'),
    messageContent: document.getElementById('messageContent'),
    timestampContent: document.getElementById('timestampContent'),
    errorMessage: document.getElementById('errorMessage')
};

/**
 * Hide all status displays (loading, response, error)
 */
function hideAllDisplays() {
    elements.loading.classList.add('hidden');
    elements.response.classList.add('hidden');
    elements.error.classList.add('hidden');
}

/**
 * Show loading indicator
 */
function showLoading() {
    hideAllDisplays();
    elements.loading.classList.remove('hidden');
    elements.fetchButton.disabled = true;
}

/**
 * Show response from backend
 * @param {Object} data - Response data from API
 */
function showResponse(data) {
    hideAllDisplays();
    elements.messageContent.textContent = data.message;
    elements.timestampContent.textContent = `Timestamp: ${formatTimestamp(data.timestamp)}`;
    elements.response.classList.remove('hidden');
    elements.fetchButton.disabled = false;
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    hideAllDisplays();
    elements.errorMessage.textContent = message;
    elements.error.classList.remove('hidden');
    elements.fetchButton.disabled = false;
}

/**
 * Format ISO timestamp to readable format
 * @param {string} isoString - ISO format timestamp
 * @returns {string} Formatted timestamp
 */
function formatTimestamp(isoString) {
    try {
        const date = new Date(isoString);
        return date.toLocaleString();
    } catch (error) {
        return isoString;
    }
}

/**
 * Fetch data from backend API
 */
async function fetchFromBackend() {
    showLoading();
    
    try {
        const response = await fetch(`${CONFIG.BACKEND_URL}${CONFIG.API_HELLO_ENDPOINT}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showResponse(data);
        
    } catch (error) {
        console.error('Error fetching from backend:', error);
        showError(`Failed to fetch data from backend: ${error.message}`);
    }
}

/**
 * Initialize application
 */
function init() {
    // Add event listener to fetch button
    elements.fetchButton.addEventListener('click', fetchFromBackend);
    
    console.log('Green Theme Hello World App initialized');
}

// Initialize when DOM is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
