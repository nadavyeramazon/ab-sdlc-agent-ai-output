/**
 * Green Greeter Frontend JavaScript
 * 
 * Handles user interactions and API communication for the green-themed greeting application.
 */

// Configuration for API endpoints
const API_CONFIG = {
    // Use environment-aware API base URL
    BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : 'http://backend:8000',
    ENDPOINTS: {
        GREET: '/greet',
        HEALTH: '/health'
    }
};

// DOM elements
let nameInput;
let greetButton;
let clearButton;
let resultDiv;
let loadingDiv;
let errorDiv;

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    setupEventListeners();
    checkBackendHealth();
});

/**
 * Initialize DOM element references
 */
function initializeElements() {
    nameInput = document.getElementById('nameInput');
    greetButton = document.getElementById('greetButton');
    clearButton = document.getElementById('clearButton');
    resultDiv = document.getElementById('result');
    loadingDiv = document.getElementById('loading');
    errorDiv = document.getElementById('error');
    
    // Validate that all required elements exist
    const requiredElements = {
        nameInput: 'nameInput',
        greetButton: 'greetButton', 
        clearButton: 'clearButton',
        resultDiv: 'result',
        loadingDiv: 'loading',
        errorDiv: 'error'
    };
    
    for (const [variable, id] of Object.entries(requiredElements)) {
        if (!eval(variable)) {
            console.error(`Required element not found: ${id}`);
        }
    }
}

/**
 * Setup event listeners for user interactions
 */
function setupEventListeners() {
    if (greetButton) {
        greetButton.addEventListener('click', handleGreetClick);
    }
    
    if (clearButton) {
        clearButton.addEventListener('click', handleClearClick);
    }
    
    if (nameInput) {
        nameInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                handleGreetClick();
            }
        });
        
        nameInput.addEventListener('input', function() {
            if (nameInput.value.trim()) {
                enableButton(greetButton);
            } else {
                disableButton(greetButton);
            }
        });
    }
}

/**
 * Handle greet button click
 */
async function handleGreetClick() {
    const name = nameInput?.value?.trim();
    
    if (!name) {
        showError('Please enter your name');
        return;
    }
    
    if (name.length > 100) {
        showError('Name is too long (maximum 100 characters)');
        return;
    }
    
    await greetUser(name);
}

/**
 * Handle clear button click
 */
function handleClearClick() {
    if (nameInput) {
        nameInput.value = '';
        nameInput.focus();
    }
    
    hideAllMessages();
    disableButton(greetButton);
}

/**
 * Send greeting request to backend API
 * @param {string} name - The user's name
 */
async function greetUser(name) {
    try {
        showLoading();
        hideError();
        hideResult();
        
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.GREET}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || `HTTP error! status: ${response.status}`);
        }
        
        // Handle the response with 'message' field
        if (data.message) {
            showResult(data.message);
        } else {
            throw new Error('Invalid response format');
        }
        
    } catch (error) {
        console.error('Error greeting user:', error);
        showError(`Failed to get greeting: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * Check backend health status
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HEALTH}`);
        const data = await response.json();
        
        if (response.ok && data.status === 'healthy') {
            console.log('Backend is healthy');
        } else {
            console.warn('Backend health check failed');
        }
    } catch (error) {
        console.error('Backend health check error:', error);
    }
}

/**
 * Show loading state
 */
function showLoading() {
    if (loadingDiv) {
        loadingDiv.style.display = 'block';
    }
    disableButton(greetButton);
}

/**
 * Hide loading state
 */
function hideLoading() {
    if (loadingDiv) {
        loadingDiv.style.display = 'none';
    }
    if (nameInput?.value?.trim()) {
        enableButton(greetButton);
    }
}

/**
 * Show greeting result
 * @param {string} message - The greeting message to display
 */
function showResult(message) {
    if (resultDiv) {
        resultDiv.textContent = message;
        resultDiv.style.display = 'block';
        resultDiv.classList.add('show');
    }
}

/**
 * Hide greeting result
 */
function hideResult() {
    if (resultDiv) {
        resultDiv.style.display = 'none';
        resultDiv.classList.remove('show');
    }
}

/**
 * Show error message
 * @param {string} message - The error message to display
 */
function showError(message) {
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.classList.add('show');
    }
}

/**
 * Hide error message
 */
function hideError() {
    if (errorDiv) {
        errorDiv.style.display = 'none';
        errorDiv.classList.remove('show');
    }
}

/**
 * Hide all message divs
 */
function hideAllMessages() {
    hideResult();
    hideError();
    hideLoading();
}

/**
 * Enable a button
 * @param {HTMLElement} button - The button to enable
 */
function enableButton(button) {
    if (button) {
        button.disabled = false;
        button.classList.remove('disabled');
    }
}

/**
 * Disable a button
 * @param {HTMLElement} button - The button to disable
 */
function disableButton(button) {
    if (button) {
        button.disabled = true;
        button.classList.add('disabled');
    }
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        greetUser,
        handleGreetClick,
        handleClearClick,
        showResult,
        showError,
        hideAllMessages,
        checkBackendHealth
    };
}