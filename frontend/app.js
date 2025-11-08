/**
 * Greeting App - Vanilla JavaScript
 * Handles form submission and API communication
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';
const GREET_ENDPOINT = '/api/greet';

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
    console.log('Greeting App initialized successfully');
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
    
    // Get form values
    const userName = userNameInput.value.trim();
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
 * Validate user input
 * @returns {boolean} - True if input is valid
 */
function validateInput() {
    const userName = userNameInput.value.trim();
    
    if (!userName) {
        displayError('Please enter your name');
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
    
    console.log('Sending request to:', url, 'with data:', requestBody);
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        // Handle non-OK responses
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const errorMessage = errorData.detail || `Server error: ${response.status}`;
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        console.log('Received response:', data);
        
        return data;
        
    } catch (error) {
        console.error('API Error:', error);
        
        // Provide user-friendly error messages
        if (error.message.includes('Failed to fetch')) {
            throw new Error('Unable to connect to the server. Please make sure the backend is running.');
        }
        
        throw error;
    }
}

/**
 * Display greeting message
 * @param {Object} data - API response data
 */
function displayGreeting(data) {
    greetingMessage.textContent = data.message;
    greetingDetails.textContent = `Greeted ${data.name} in ${getLanguageName(data.language)}`;
    
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
    errorDiv.textContent = `❌ ${message}`;
    errorDiv.classList.remove('hidden');
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
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian'
    };
    return languages[code] || code;
}