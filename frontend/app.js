/**
 * Greeting App - Vanilla JavaScript Frontend
 * Blue-themed application for personalized greetings
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

// Howdy-specific DOM Elements
const howdyForm = document.getElementById('howdyForm');
const howdyNameInput = document.getElementById('howdyNameInput');
const howdyLanguageSelect = document.getElementById('howdyLanguageSelect');
const howdyStyleSelect = document.getElementById('howdyStyleSelect');
const howdyResult = document.getElementById('howdyResult');
const howdyText = document.getElementById('howdyText');
const howdyName = document.getElementById('howdyName');
const howdyLanguage = document.getElementById('howdyLanguage');
const howdyStyle = document.getElementById('howdyStyle');
const howdyErrorMessage = document.getElementById('howdyErrorMessage');

// Tab elements
const greetTab = document.getElementById('greetTab');
const howdyTab = document.getElementById('howdyTab');
const greetSection = document.getElementById('greetSection');
const howdySection = document.getElementById('howdySection');

/**
 * Initialize the application
 */
function init() {
    // Add form submit event listeners
    greetingForm.addEventListener('submit', handleGreetingFormSubmit);
    howdyForm.addEventListener('submit', handleHowdyFormSubmit);
    
    // Add input validation
    nameInput.addEventListener('input', () => clearError('greet'));
    howdyNameInput.addEventListener('input', () => clearError('howdy'));
    
    // Add tab click event listeners
    greetTab.addEventListener('click', () => switchTab('greet'));
    howdyTab.addEventListener('click', () => switchTab('howdy'));
    
    // Log initialization
    console.log('✅ Greeting App initialized');
    console.log('🌊 Blue theme loaded');
}

/**
 * Switch between tabs
 * @param {string} tab - Tab to switch to ('greet' or 'howdy')
 */
function switchTab(tab) {
    if (tab === 'greet') {
        greetTab.classList.add('active');
        howdyTab.classList.remove('active');
        greetSection.classList.remove('hidden');
        howdySection.classList.add('hidden');
    } else if (tab === 'howdy') {
        howdyTab.classList.add('active');
        greetTab.classList.remove('active');
        howdySection.classList.remove('hidden');
        greetSection.classList.add('hidden');
    }
}

/**
 * Handle greeting form submission
 * @param {Event} event - Form submit event
 */
async function handleGreetingFormSubmit(event) {
    event.preventDefault();
    
    // Clear previous results and errors
    hideResult('greet');
    hideError('greet');
    
    // Get form values
    const name = nameInput.value.trim();
    const language = languageSelect.value;
    
    // Validate input
    if (!name) {
        showError('greet', 'Please enter your name');
        return;
    }
    
    // Disable form while processing
    setFormDisabled('greet', true);
    
    try {
        // Make API request
        const greeting = await fetchGreeting(name, language);
        
        // Display result
        showResult('greet', greeting);
    } catch (error) {
        console.error('Error fetching greeting:', error);
        showError(
            'greet',
            error.message || 'Failed to fetch greeting. Please try again.'
        );
    } finally {
        // Re-enable form
        setFormDisabled('greet', false);
    }
}

/**
 * Handle howdy form submission
 * @param {Event} event - Form submit event
 */
async function handleHowdyFormSubmit(event) {
    event.preventDefault();
    
    // Clear previous results and errors
    hideResult('howdy');
    hideError('howdy');
    
    // Get form values
    const name = howdyNameInput.value.trim();
    const language = howdyLanguageSelect.value;
    const style = howdyStyleSelect.value;
    
    // Validate input
    if (!name) {
        showError('howdy', 'Please enter your name');
        return;
    }
    
    // Disable form while processing
    setFormDisabled('howdy', true);
    
    try {
        // Make API request
        const greeting = await fetchHowdy(name, language, style);
        
        // Display result
        showResult('howdy', greeting);
    } catch (error) {
        console.error('Error fetching howdy:', error);
        showError(
            'howdy',
            error.message || 'Failed to fetch howdy. Please try again.'
        );
    } finally {
        // Re-enable form
        setFormDisabled('howdy', false);
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
 * Fetch howdy from API
 * @param {string} name - User's name
 * @param {string} language - Selected language code
 * @param {string} style - Selected greeting style
 * @returns {Promise<Object>} Howdy response
 */
async function fetchHowdy(name, language, style) {
    const url = `${API_BASE_URL}/api/howdy`;
    
    console.log(`📡 Fetching howdy for ${name} in ${language} with ${style} style...`);
    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            language: language,
            style: style
        })
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
            errorData.detail || `HTTP error! status: ${response.status}`
        );
    }
    
    const data = await response.json();
    console.log('✅ Howdy received:', data);
    
    return data;
}

/**
 * Display result
 * @param {string} type - Type of result ('greet' or 'howdy')
 * @param {Object} data - Response data
 */
function showResult(type, data) {
    if (type === 'greet') {
        greetingText.textContent = data.message;
        greetingName.textContent = data.name;
        greetingLanguage.textContent = data.language.toUpperCase();
        greetingResult.classList.remove('hidden');
    } else if (type === 'howdy') {
        howdyText.textContent = data.message;
        howdyName.textContent = data.name;
        howdyLanguage.textContent = data.language.toUpperCase();
        howdyStyle.textContent = data.style.charAt(0).toUpperCase() + data.style.slice(1);
        howdyResult.classList.remove('hidden');
    }
    
    console.log(`✨ ${type} result displayed`);
}

/**
 * Hide result
 * @param {string} type - Type of result ('greet' or 'howdy')
 */
function hideResult(type) {
    if (type === 'greet') {
        greetingResult.classList.add('hidden');
    } else if (type === 'howdy') {
        howdyResult.classList.add('hidden');
    }
}

/**
 * Display error message
 * @param {string} type - Type of error ('greet' or 'howdy')
 * @param {string} message - Error message to display
 */
function showError(type, message) {
    const errorElement = type === 'greet' ? errorMessage : howdyErrorMessage;
    errorElement.textContent = `❌ ${message}`;
    errorElement.classList.remove('hidden');
    
    console.error(`Error (${type}):`, message);
}

/**
 * Hide error message
 * @param {string} type - Type of error ('greet' or 'howdy')
 */
function hideError(type) {
    const errorElement = type === 'greet' ? errorMessage : howdyErrorMessage;
    errorElement.classList.add('hidden');
}

/**
 * Clear error on input
 * @param {string} type - Type of form ('greet' or 'howdy')
 */
function clearError(type) {
    const errorElement = type === 'greet' ? errorMessage : howdyErrorMessage;
    if (!errorElement.classList.contains('hidden')) {
        hideError(type);
    }
}

/**
 * Enable or disable form inputs
 * @param {string} type - Type of form ('greet' or 'howdy')
 * @param {boolean} disabled - Whether to disable the form
 */
function setFormDisabled(type, disabled) {
    if (type === 'greet') {
        nameInput.disabled = disabled;
        languageSelect.disabled = disabled;
        
        const submitButton = greetingForm.querySelector('button[type="submit"]');
        submitButton.disabled = disabled;
        submitButton.textContent = disabled ? 'Loading... ⏳' : 'Get Greeting 👋';
    } else if (type === 'howdy') {
        howdyNameInput.disabled = disabled;
        howdyLanguageSelect.disabled = disabled;
        howdyStyleSelect.disabled = disabled;
        
        const submitButton = howdyForm.querySelector('button[type="submit"]');
        submitButton.disabled = disabled;
        submitButton.textContent = disabled ? 'Loading... ⏳' : 'Get Howdy 🤠';
    }
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}