// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const greetingForm = document.getElementById('greetingForm');
const nameInput = document.getElementById('nameInput');
const languageSelect = document.getElementById('languageSelect');
const submitBtn = document.getElementById('submitBtn');
const resultContainer = document.getElementById('resultContainer');
const errorContainer = document.getElementById('errorContainer');
const greetingMessage = document.getElementById('greetingMessage');
const resultName = document.getElementById('resultName');
const resultLanguage = document.getElementById('resultLanguage');
const errorMessage = document.getElementById('errorMessage');
const apiStatus = document.getElementById('apiStatus');

/**
 * Check API health status on page load
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            apiStatus.textContent = data.status === 'healthy' ? '✅ Healthy' : '⚠️ Unknown';
            apiStatus.classList.remove('checking');
            apiStatus.classList.add('healthy');
        } else {
            throw new Error('Health check failed');
        }
    } catch (error) {
        apiStatus.textContent = '❌ Offline';
        apiStatus.classList.remove('checking', 'healthy');
        console.error('API health check failed:', error);
    }
}

/**
 * Show result container with greeting message
 * @param {Object} data - Greeting response data
 */
function showResult(data) {
    // Hide error if visible
    errorContainer.classList.add('hidden');
    
    // Update result content
    greetingMessage.textContent = data.message;
    resultName.textContent = data.name;
    resultLanguage.textContent = getLanguageName(data.language);
    
    // Show result
    resultContainer.classList.remove('hidden');
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show error container with error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    // Hide result if visible
    resultContainer.classList.add('hidden');
    
    // Update error content
    errorMessage.textContent = message;
    
    // Show error
    errorContainer.classList.remove('hidden');
    
    // Scroll to error
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Get full language name from code
 * @param {string} code - Language code
 * @returns {string} Full language name
 */
function getLanguageName(code) {
    const languages = {
        'en': 'English',
        'es': 'Español',
        'fr': 'Français',
        'de': 'Deutsch'
    };
    return languages[code] || code.toUpperCase();
}

/**
 * Validate name input
 * @param {string} name - Name to validate
 * @returns {Object} Validation result
 */
function validateName(name) {
    const trimmedName = name.trim();
    
    if (trimmedName.length === 0) {
        return { valid: false, message: 'Name cannot be empty' };
    }
    
    if (trimmedName.length > 100) {
        return { valid: false, message: 'Name is too long (max 100 characters)' };
    }
    
    return { valid: true, name: trimmedName };
}

/**
 * Fetch greeting from API
 * @param {string} name - User's name
 * @param {string} language - Language code
 */
async function fetchGreeting(name, language) {
    try {
        // Disable submit button
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Loading...';
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                language: language
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult(data);
        } else {
            // Handle error response from API
            const errorMsg = data.detail || 'An error occurred while fetching the greeting';
            showError(errorMsg);
        }
    } catch (error) {
        console.error('Error fetching greeting:', error);
        showError('Failed to connect to the API. Please make sure the backend server is running on ' + API_BASE_URL);
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = 'Get Greeting';
    }
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
function handleSubmit(event) {
    event.preventDefault();
    
    const name = nameInput.value;
    const language = languageSelect.value;
    
    // Validate name
    const validation = validateName(name);
    
    if (!validation.valid) {
        showError(validation.message);
        return;
    }
    
    // Fetch greeting
    fetchGreeting(validation.name, language);
}

/**
 * Initialize application
 */
function init() {
    // Check API health
    checkAPIHealth();
    
    // Add form submit listener
    greetingForm.addEventListener('submit', handleSubmit);
    
    // Add input listener to hide errors on typing
    nameInput.addEventListener('input', () => {
        if (!errorContainer.classList.contains('hidden')) {
            errorContainer.classList.add('hidden');
        }
    });
    
    // Focus on name input
    nameInput.focus();
    
    console.log('Greeting App initialized successfully!');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
