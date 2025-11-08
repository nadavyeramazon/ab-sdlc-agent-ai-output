/**
 * Greeting Application - Vanilla JavaScript
 * Handles user interactions and API communication
 */

// Configuration - supports environment-based URLs
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : `${window.location.protocol}//${window.location.hostname}:8000`,
    ENDPOINTS: {
        GREET: '/greet',
        HEALTH: '/health'
    },
    REQUEST_TIMEOUT: 10000, // 10 seconds
    MAX_RETRIES: 3
};

// DOM Elements
const elements = {
    form: null,
    nameInput: null,
    languageSelect: null,
    responseContainer: null,
    greetingMessage: null,
    responseName: null,
    responseLanguage: null,
    errorContainer: null,
    errorMessage: null,
    loadingContainer: null
};

/**
 * Initialize the application
 */
function init() {
    console.log('Initializing Greeting Application...');
    
    // Get DOM elements
    elements.form = document.getElementById('greetingForm');
    elements.nameInput = document.getElementById('nameInput');
    elements.languageSelect = document.getElementById('languageSelect');
    elements.responseContainer = document.getElementById('responseContainer');
    elements.greetingMessage = document.getElementById('greetingMessage');
    elements.responseName = document.getElementById('responseName');
    elements.responseLanguage = document.getElementById('responseLanguage');
    elements.errorContainer = document.getElementById('errorContainer');
    elements.errorMessage = document.getElementById('errorMessage');
    elements.loadingContainer = document.getElementById('loadingContainer');

    // Validate all elements exist
    if (!validateElements()) {
        console.error('Failed to initialize: Required DOM elements not found');
        return;
    }

    // Add event listeners
    elements.form.addEventListener('submit', handleSubmit);
    elements.nameInput.addEventListener('input', clearErrorOnInput);
    
    // Focus on name input for better UX
    elements.nameInput.focus();
    
    // Check API health on load
    checkAPIHealth();
    
    console.log('Greeting Application initialized successfully');
}

/**
 * Validate that all required DOM elements exist
 * @returns {boolean} True if all elements exist
 */
function validateElements() {
    for (const [key, element] of Object.entries(elements)) {
        if (element === null) {
            console.error(`Required element not found: ${key}`);
            return false;
        }
    }
    return true;
}

/**
 * Clear error message when user starts typing
 */
function clearErrorOnInput() {
    if (!elements.errorContainer.classList.contains('hidden')) {
        elements.errorContainer.classList.add('hidden');
    }
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleSubmit(event) {
    event.preventDefault();
    
    // Get form data
    const name = elements.nameInput.value.trim();
    const language = elements.languageSelect.value;
    
    // Validate input
    if (!name) {
        showError('Please enter your name');
        elements.nameInput.focus();
        return;
    }
    
    if (name.length > 100) {
        showError('Name is too long (maximum 100 characters)');
        return;
    }
    
    // Clear previous messages
    hideAllMessages();
    showLoading();
    
    try {
        // Call the API with retry logic
        const response = await greetUserWithRetry(name, language);
        
        // Display the greeting
        displayGreeting(response);
    } catch (error) {
        console.error('Error greeting user:', error);
        showError(error.message || 'An unexpected error occurred');
    } finally {
        hideLoading();
    }
}

/**
 * Call the greet API endpoint with retry logic
 * @param {string} name - User's name
 * @param {string} language - Selected language code
 * @param {number} retryCount - Current retry attempt
 * @returns {Promise<Object>} - API response
 */
async function greetUserWithRetry(name, language, retryCount = 0) {
    try {
        return await greetUser(name, language);
    } catch (error) {
        if (retryCount < CONFIG.MAX_RETRIES && error.message.includes('Cannot connect')) {
            console.log(`Retrying... Attempt ${retryCount + 1} of ${CONFIG.MAX_RETRIES}`);
            await sleep(1000 * (retryCount + 1)); // Exponential backoff
            return await greetUserWithRetry(name, language, retryCount + 1);
        }
        throw error;
    }
}

/**
 * Sleep for specified milliseconds
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise<void>}
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Call the greet API endpoint
 * @param {string} name - User's name
 * @param {string} language - Selected language code
 * @returns {Promise<Object>} - API response
 */
async function greetUser(name, language) {
    const url = `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.GREET}`;
    
    const requestData = {
        name: name,
        language: language
    };
    
    console.log(`Sending greeting request to ${url}`);
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.REQUEST_TIMEOUT);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({
                detail: 'Failed to get greeting from server'
            }));
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Greeting received successfully');
        return data;
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout. Please try again.');
        }
        if (error instanceof TypeError) {
            throw new Error('Cannot connect to server. Please ensure the backend is running.');
        }
        throw error;
    }
}

/**
 * Check API health status
 */
async function checkAPIHealth() {
    const url = `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.HEALTH}`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            signal: AbortSignal.timeout(5000)
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ API is healthy:', data);
        } else {
            console.warn('⚠️ API returned non-OK status:', response.status);
        }
    } catch (error) {
        console.error('❌ Cannot reach API:', error.message);
    }
}

/**
 * Display the greeting response
 * @param {Object} data - Response data from API
 */
function displayGreeting(data) {
    // Sanitize and display data
    elements.greetingMessage.textContent = sanitizeText(data.message);
    elements.responseName.textContent = sanitizeText(data.name);
    elements.responseLanguage.textContent = getLanguageName(data.language);
    
    elements.responseContainer.classList.remove('hidden');
    
    // Announce to screen readers
    announceToScreenReader(`Greeting received: ${data.message}`);
}

/**
 * Sanitize text to prevent XSS
 * @param {string} text - Text to sanitize
 * @returns {string} - Sanitized text
 */
function sanitizeText(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.textContent;
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    elements.errorMessage.textContent = sanitizeText(message);
    elements.errorContainer.classList.remove('hidden');
    
    // Announce to screen readers
    announceToScreenReader(`Error: ${message}`);
}

/**
 * Show loading indicator
 */
function showLoading() {
    elements.loadingContainer.classList.remove('hidden');
    elements.loadingContainer.setAttribute('aria-live', 'polite');
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    elements.loadingContainer.classList.add('hidden');
}

/**
 * Hide all message containers
 */
function hideAllMessages() {
    elements.responseContainer.classList.add('hidden');
    elements.errorContainer.classList.add('hidden');
    elements.loadingContainer.classList.add('hidden');
}

/**
 * Get full language name from code
 * @param {string} code - Language code
 * @returns {string} - Full language name
 */
function getLanguageName(code) {
    const languages = {
        'en': 'English',
        'es': 'Spanish (Español)',
        'fr': 'French (Français)',
        'de': 'German (Deutsch)',
        'it': 'Italian (Italiano)'
    };
    return languages[code] || code;
}

/**
 * Announce message to screen readers
 * @param {string} message - Message to announce
 */
function announceToScreenReader(message) {
    const announcement = document.getElementById('sr-announcement');
    if (announcement) {
        announcement.textContent = message;
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}