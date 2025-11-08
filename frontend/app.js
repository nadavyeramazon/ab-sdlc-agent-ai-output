/**
 * Greeting App - Vanilla JavaScript Frontend
 * Green-themed application for personalized greetings
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const greetingForm = document.getElementById('greetingForm');
const nameInput = document.getElementById('nameInput');
const languageSelect = document.getElementById('languageSelect');
const greetingResult = document.getElementById('greetingResult');
const greetingText = document.getElementById('greetingText');
const greetingName = document.getElementById('greetingName');
const greetingLanguage = document.getElementById('greetingLanguage');
const errorMessage = document.getElementById('errorMessage');

/**
 * Initialize the application
 */
function init() {
    // Add form submit event listener
    greetingForm.addEventListener('submit', handleFormSubmit);
    
    // Add input validation
    nameInput.addEventListener('input', clearError);
    
    // Log initialization
    console.log('✅ Greeting App initialized');
    console.log('🌿 Green theme loaded');
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Clear previous results and errors
    hideResult();
    hideError();
    
    // Get form values
    const name = nameInput.value.trim();
    const language = languageSelect.value;
    
    // Validate input
    if (!name) {
        showError('Please enter your name');
        return;
    }
    
    // Disable form while processing
    setFormDisabled(true);
    
    try {
        // Make API request
        const greeting = await fetchGreeting(name, language);
        
        // Display result
        showResult(greeting);
    } catch (error) {
        console.error('Error fetching greeting:', error);
        showError(
            error.message || 'Failed to fetch greeting. Please try again.'
        );
    } finally {
        // Re-enable form
        setFormDisabled(false);
    }
}

/**
 * Fetch greeting from API
 * @param {string} name - User's name
 * @param {string} language - Selected language code
 * @returns {Promise<Object>} Greeting response
 */
async function fetchGreeting(name, language) {
    const url = `${API_BASE_URL}/api/greet`;
    
    console.log(`📡 Fetching greeting for ${name} in ${language}...`);
    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            language: language
        })
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
            errorData.detail || `HTTP error! status: ${response.status}`
        );
    }
    
    const data = await response.json();
    console.log('✅ Greeting received:', data);
    
    return data;
}

/**
 * Display greeting result
 * @param {Object} greeting - Greeting data
 */
function showResult(greeting) {
    greetingText.textContent = greeting.message;
    greetingName.textContent = greeting.name;
    greetingLanguage.textContent = greeting.language.toUpperCase();
    
    greetingResult.classList.remove('hidden');
    
    console.log('✨ Result displayed');
}

/**
 * Hide greeting result
 */
function hideResult() {
    greetingResult.classList.add('hidden');
}

/**
 * Display error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorMessage.textContent = `❌ ${message}`;
    errorMessage.classList.remove('hidden');
    
    console.error('Error:', message);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.classList.add('hidden');
}

/**
 * Clear error on input
 */
function clearError() {
    if (!errorMessage.classList.contains('hidden')) {
        hideError();
    }
}

/**
 * Enable or disable form inputs
 * @param {boolean} disabled - Whether to disable the form
 */
function setFormDisabled(disabled) {
    nameInput.disabled = disabled;
    languageSelect.disabled = disabled;
    
    const submitButton = greetingForm.querySelector('button[type="submit"]');
    submitButton.disabled = disabled;
    submitButton.textContent = disabled ? 'Loading... ⏳' : 'Get Greeting 👋';
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}