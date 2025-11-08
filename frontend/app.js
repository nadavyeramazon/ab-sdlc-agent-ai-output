/**
 * Greeting App - Vanilla JavaScript
 * Handles form submission and API communication
 */

// Configuration
// Auto-detect API URL based on environment
// In Docker: Use same origin (nginx proxy)
// In Development: Use localhost:8000
const API_BASE_URL = window.location.hostname === 'localhost' && window.location.port === '' 
    ? 'http://localhost:8000' 
    : `${window.location.protocol}//${window.location.hostname}:8000`;

const GREET_ENDPOINT = '/api/greet';
const HEALTH_ENDPOINT = '/health';

// DOM Elements
let form;
let userNameInput;
let languageSelect;
let submitBtn;
let resultDiv;
let errorDiv;
let loadingDiv;
let greetingMessage;
let greetingDetails;

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    attachEventListeners();
    checkBackendHealth();
    console.log('Greeting App initialized successfully');
    console.log('API Base URL:', API_BASE_URL);
});

/**
 * Initialize DOM element references
 */
function initializeElements() {
    form = document.getElementById('greetingForm');
    userNameInput = document.getElementById('userName');
    languageSelect = document.getElementById('language');
    submitBtn = document.getElementById('submitBtn');
    resultDiv = document.getElementById('result');
    errorDiv = document.getElementById('error');
    loadingDiv = document.getElementById('loading');
    greetingMessage = document.getElementById('greetingMessage');
    greetingDetails = document.getElementById('greetingDetails');
}

/**
 * Attach event listeners to form elements
 */
function attachEventListeners() {
    form.addEventListener('submit', handleFormSubmit);
    
    // Add input validation
    userNameInput.addEventListener('input', () => {
        clearError();
        validateInput();
    });
    
    languageSelect.addEventListener('change', () => {
        clearError();
    });
}

/**
 * Check backend health on initialization
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}${HEALTH_ENDPOINT}`);
        if (response.ok) {
            console.log('✅ Backend is healthy and reachable');
        } else {
            console.warn('⚠️ Backend responded but may have issues');
        }
    } catch (error) {
        console.warn('⚠️ Backend health check failed:', error.message);
        console.log('This is normal if backend is not running yet');
    }
}

/**
 * Handle form submission
 * @param {Event} event - The submit event
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Clear previous messages
    clearMessages();
    
    // Validate input
    if (!validateInput()) {
        return;
    }
    
    // Get form values and sanitize
    const userName = sanitizeInput(userNameInput.value.trim());
    const language = languageSelect.value;
    
    // Show loading state
    showLoading();
    
    try {
        // Call API
        const response = await fetchGreeting(userName, language);
        
        // Display success
        displayGreeting(response);
        
    } catch (error) {
        // Display error
        displayError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Sanitize user input to prevent XSS
 * @param {string} input - Raw user input
 * @returns {string} - Sanitized input
 */
function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

/**
 * Validate user input
 * @returns {boolean} - True if input is valid
 */
function validateInput() {
    const userName = userNameInput.value.trim();
    
    if (!userName) {
        displayError('Please enter your name');
        return false;
    }
    
    if (userName.length < 1) {
        displayError('Name must be at least 1 character');
        return false;
    }
    
    if (userName.length > 100) {
        displayError('Name must be 100 characters or less');
        return false;
    }
    
    return true;
}

/**
 * Fetch greeting from API
 * @param {string} name - User name
 * @param {string} language - Language code
 * @returns {Promise<Object>} - API response
 */
async function fetchGreeting(name, language) {
    const url = `${API_BASE_URL}${GREET_ENDPOINT}`;
    
    const requestBody = {
        name: name,
        language: language
    };
    
    console.log('📤 Sending request to:', url);
    console.log('📦 Request body:', requestBody);
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        console.log('📥 Response status:', response.status);
        
        // Handle non-OK responses
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const errorMessage = errorData.detail || `Server error: ${response.status} ${response.statusText}`;
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        console.log('✅ Received response:', data);
        
        return data;
        
    } catch (error) {
        console.error('❌ API Error:', error);
        
        // Provide user-friendly error messages
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            throw new Error(
                'Unable to connect to the server. Please ensure the backend is running at ' + API_BASE_URL
            );
        }
        
        throw error;
    }
}

/**
 * Display greeting message with animation
 * @param {Object} data - API response data
 */
function displayGreeting(data) {
    // Sanitize the message before displaying
    const safeMessage = sanitizeInput(data.message);
    const safeName = sanitizeInput(data.name);
    
    greetingMessage.textContent = safeMessage;
    greetingDetails.textContent = `✨ Greeted ${safeName} in ${getLanguageName(data.language)}`;
    
    resultDiv.classList.remove('hidden');
    
    // Add animation
    resultDiv.style.animation = 'none';
    setTimeout(() => {
        resultDiv.style.animation = 'fadeIn 0.5s ease';
    }, 10);
}

/**
 * Display error message
 * @param {string} message - Error message
 */
function displayError(message) {
    const safeMessage = sanitizeInput(message);
    errorDiv.textContent = `❌ ${safeMessage}`;
    errorDiv.classList.remove('hidden');
    
    // Add shake animation
    errorDiv.style.animation = 'none';
    setTimeout(() => {
        errorDiv.style.animation = 'shake 0.5s ease';
    }, 10);
}

/**
 * Clear all messages
 */
function clearMessages() {
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
}

/**
 * Clear only error message
 */
function clearError() {
    errorDiv.classList.add('hidden');
}

/**
 * Show loading indicator
 */
function showLoading() {
    loadingDiv.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Loading...';
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    loadingDiv.classList.add('hidden');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Get Greeting';
}

/**
 * Get full language name from code
 * @param {string} code - Language code
 * @returns {string} - Full language name
 */
function getLanguageName(code) {
    const languages = {
        'en': 'English 🇬🇧',
        'es': 'Spanish 🇪🇸',
        'fr': 'French 🇫🇷',
        'de': 'German 🇩🇪',
        'it': 'Italian 🇮🇹'
    };
    return languages[code] || code;
}