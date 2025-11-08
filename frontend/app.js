/**
 * Blue Greeting App - Frontend JavaScript
 * Vanilla JavaScript implementation for greeting users
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
let greetingForm;
let nameInput;
let languageSelect;
let submitBtn;
let resultContainer;
let greetingMessage;
let greetingDetails;
let resetBtn;
let errorContainer;
let errorMessage;
let errorResetBtn;
let loadingContainer;
let apiStatus;

// Initialize the application
function init() {
    // Get DOM elements
    greetingForm = document.getElementById('greetingForm');
    nameInput = document.getElementById('nameInput');
    languageSelect = document.getElementById('languageSelect');
    submitBtn = document.getElementById('submitBtn');
    resultContainer = document.getElementById('resultContainer');
    greetingMessage = document.getElementById('greetingMessage');
    greetingDetails = document.getElementById('greetingDetails');
    resetBtn = document.getElementById('resetBtn');
    errorContainer = document.getElementById('errorContainer');
    errorMessage = document.getElementById('errorMessage');
    errorResetBtn = document.getElementById('errorResetBtn');
    loadingContainer = document.getElementById('loadingContainer');
    apiStatus = document.getElementById('apiStatus');

    // Set up event listeners
    greetingForm.addEventListener('submit', handleSubmit);
    resetBtn.addEventListener('click', resetForm);
    errorResetBtn.addEventListener('click', resetForm);

    // Check API health on load
    checkApiHealth();
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleSubmit(event) {
    event.preventDefault();

    const name = nameInput.value.trim();
    const language = languageSelect.value;

    if (!name) {
        showError('Please enter your name');
        return;
    }

    // Show loading state
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/api/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, language }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get greeting');
        }

        const data = await response.json();
        showResult(data);
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to connect to the server. Please try again.');
    }
}

/**
 * Show loading state
 */
function showLoading() {
    greetingForm.classList.add('hidden');
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
    loadingContainer.classList.remove('hidden');
    submitBtn.disabled = true;
}

/**
 * Show greeting result
 * @param {Object} data - API response data
 */
function showResult(data) {
    loadingContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
    greetingForm.classList.add('hidden');

    greetingMessage.textContent = data.message;
    greetingDetails.textContent = `Greeted in ${getLanguageName(data.language)} for ${data.name}`;

    resultContainer.classList.remove('hidden');
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    loadingContainer.classList.add('hidden');
    resultContainer.classList.add('hidden');
    greetingForm.classList.add('hidden');

    errorMessage.textContent = message;
    errorContainer.classList.remove('hidden');
}

/**
 * Reset form to initial state
 */
function resetForm() {
    loadingContainer.classList.add('hidden');
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');

    nameInput.value = '';
    languageSelect.value = 'en';
    submitBtn.disabled = false;

    greetingForm.classList.remove('hidden');
    nameInput.focus();
}

/**
 * Get language name from code
 * @param {string} code - Language code
 * @returns {string} - Language name
 */
function getLanguageName(code) {
    const languages = {
        en: 'English',
        es: 'Spanish',
        fr: 'French',
        de: 'German',
    };
    return languages[code] || code;
}

/**
 * Check API health status
 */
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            apiStatus.textContent = `API Status: ${data.status} ✅`;
            apiStatus.style.color = 'var(--secondary-green)';
        } else {
            throw new Error('API not healthy');
        }
    } catch (error) {
        console.error('API health check failed:', error);
        apiStatus.textContent = 'API Status: Offline ❌';
        apiStatus.style.color = 'var(--error-red)';
    }
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleSubmit,
        showResult,
        showError,
        resetForm,
        getLanguageName,
        checkApiHealth,
    };
}
