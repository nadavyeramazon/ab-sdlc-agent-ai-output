/**
 * Greeting Application - Vanilla JavaScript
 * Handles user interactions and API communication
 */

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    ENDPOINTS: {
        GREET: '/greet',
        HEALTH: '/health'
    }
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

    // Add event listeners
    elements.form.addEventListener('submit', handleSubmit);
    
    // Focus on name input
    elements.nameInput.focus();
    
    // Check API health on load
    checkAPIHealth();
    
    console.log('Greeting Application initialized');
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
        return;
    }
    
    // Clear previous messages
    hideAllMessages();
    showLoading();
    
    try {
        // Call the API
        const response = await greetUser(name, language);
        
        // Display the greeting
        displayGreeting(response);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
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
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get greeting from server');
        }
        
        return await response.json();
    } catch (error) {
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
        const response = await fetch(url);
        if (response.ok) {
            console.log('✅ API is healthy and reachable');
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
    elements.greetingMessage.textContent = data.message;
    elements.responseName.textContent = data.name;
    elements.responseLanguage.textContent = getLanguageName(data.language);
    
    elements.responseContainer.classList.remove('hidden');
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorContainer.classList.remove('hidden');
}

/**
 * Show loading indicator
 */
function showLoading() {
    elements.loadingContainer.classList.remove('hidden');
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

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
