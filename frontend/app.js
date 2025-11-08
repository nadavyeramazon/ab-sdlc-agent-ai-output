/**
 * User Greeting Service - Frontend Application
 * 
 * This application provides a green-themed UI for interacting with the
 * FastAPI backend greeting service.
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000';
const API_GREET_ENDPOINT = `${API_BASE_URL}/api/greet`;
const API_HEALTH_ENDPOINT = `${API_BASE_URL}/health`;

// DOM Elements
let form, titleInput, nameInput, submitBtn, btnText, btnLoader;
let responseArea, responseCard, greetingMessage;
let errorArea, errorMessage;
let apiStatus;

/**
 * Initialize the application when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeDOMElements();
    setupEventListeners();
    checkAPIHealth();
});

/**
 * Initialize all DOM element references
 */
function initializeDOMElements() {
    form = document.getElementById('greetingForm');
    titleInput = document.getElementById('title');
    nameInput = document.getElementById('name');
    submitBtn = document.getElementById('submitBtn');
    btnText = submitBtn.querySelector('.btn-text');
    btnLoader = submitBtn.querySelector('.btn-loader');
    
    responseArea = document.getElementById('responseArea');
    responseCard = document.getElementById('responseCard');
    greetingMessage = document.getElementById('greetingMessage');
    
    errorArea = document.getElementById('errorArea');
    errorMessage = document.getElementById('errorMessage');
    
    apiStatus = document.getElementById('apiStatus');
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    form.addEventListener('submit', handleFormSubmit);
    
    // Add input validation
    nameInput.addEventListener('input', validateNameInput);
    titleInput.addEventListener('input', validateTitleInput);
}

/**
 * Validate name input in real-time
 */
function validateNameInput(e) {
    const value = e.target.value;
    // Only allow letters, spaces, hyphens, and apostrophes
    const validPattern = /^[a-zA-Z\s'-]*$/;
    
    if (!validPattern.test(value)) {
        e.target.value = value.slice(0, -1);
    }
}

/**
 * Validate title input in real-time
 */
function validateTitleInput(e) {
    const value = e.target.value;
    // Only allow letters and periods
    const validPattern = /^[a-zA-Z.]*$/;
    
    if (!validPattern.test(value)) {
        e.target.value = value.slice(0, -1);
    }
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const name = nameInput.value.trim();
    const title = titleInput.value.trim();
    
    // Validate name
    if (!name) {
        showError('Please enter your name');
        return;
    }
    
    if (name.length > 100) {
        showError('Name must be 100 characters or less');
        return;
    }
    
    if (title && title.length > 50) {
        showError('Title must be 50 characters or less');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideError();
    
    try {
        const response = await fetch(API_GREET_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                title: title || null
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showGreeting(data.message);
        } else {
            // Handle validation errors from backend
            const errorMsg = data.detail || 'Failed to get greeting. Please try again.';
            showError(errorMsg);
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Unable to connect to the greeting service. Please ensure the backend is running.');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Set loading state for the submit button
 */
function setLoadingState(isLoading) {
    submitBtn.disabled = isLoading;
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

/**
 * Display greeting message
 */
function showGreeting(message) {
    greetingMessage.textContent = message;
    responseArea.style.display = 'block';
    form.parentElement.style.display = 'none';
    errorArea.style.display = 'none';
}

/**
 * Display error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorArea.style.display = 'block';
    responseArea.style.display = 'none';
}

/**
 * Hide error message
 */
function hideError() {
    errorArea.style.display = 'none';
}

/**
 * Reset form to initial state
 */
function resetForm() {
    form.reset();
    responseArea.style.display = 'none';
    form.parentElement.style.display = 'block';
    errorArea.style.display = 'none';
    nameInput.focus();
}

/**
 * Check API health status
 */
async function checkAPIHealth() {
    apiStatus.textContent = 'Checking...';
    apiStatus.className = 'status-indicator checking';
    
    try {
        const response = await fetch(API_HEALTH_ENDPOINT);
        const data = await response.json();
        
        if (response.ok && data.status === 'healthy') {
            apiStatus.textContent = 'Online ✓';
            apiStatus.className = 'status-indicator online';
        } else {
            apiStatus.textContent = 'Offline ✗';
            apiStatus.className = 'status-indicator offline';
        }
    } catch (error) {
        console.error('Health check failed:', error);
        apiStatus.textContent = 'Offline ✗';
        apiStatus.className = 'status-indicator offline';
    }
    
    // Check again after 30 seconds
    setTimeout(checkAPIHealth, 30000);
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateNameInput,
        validateTitleInput,
        showGreeting,
        showError,
        hideError,
        resetForm
    };
}
