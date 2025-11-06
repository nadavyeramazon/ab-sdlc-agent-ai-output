// API Configuration - Fixed for proper port configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : `http://${window.location.hostname}:8000`;

// DOM Elements
const elements = {
    greetingForm: document.getElementById('greetingForm'),
    userNameInput: document.getElementById('userName'),
    greetingTypeSelect: document.getElementById('greetingType'),
    loadingSpinner: document.getElementById('loadingSpinner'),
    greetingResult: document.getElementById('greetingResult'),
    greetingMessage: document.getElementById('greetingMessage'),
    errorMessage: document.getElementById('errorMessage'),
    errorText: document.getElementById('errorText'),
    newGreetingBtn: document.getElementById('newGreetingBtn'),
    tryAgainBtn: document.getElementById('tryAgainBtn'),
    apiStatus: document.getElementById('apiStatus'),
    apiStatusText: document.getElementById('apiStatusText')
};

// Application State
let appState = {
    isLoading: false,
    apiHealthy: false,
    greetingTypes: []
};

// Utility Functions
function showElement(element) {
    element.classList.remove('hidden');
    element.classList.add('fade-in');
}

function hideElement(element) {
    element.classList.add('hidden');
    element.classList.remove('fade-in');
}

function setLoadingState(loading) {
    appState.isLoading = loading;
    if (loading) {
        hideElement(elements.greetingResult);
        hideElement(elements.errorMessage);
        showElement(elements.loadingSpinner);
    } else {
        hideElement(elements.loadingSpinner);
    }
}

function showError(message) {
    elements.errorText.textContent = message;
    hideElement(elements.loadingSpinner);
    hideElement(elements.greetingResult);
    showElement(elements.errorMessage);
}

function showGreeting(data) {
    elements.greetingMessage.textContent = data.message;
    document.getElementById('displayUserName').textContent = data.user_name;
    document.getElementById('displayGreetingType').textContent = formatGreetingType(data.greeting_type);
    
    hideElement(elements.loadingSpinner);
    hideElement(elements.errorMessage);
    showElement(elements.greetingResult);
}

function formatGreetingType(type) {
    return type.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function resetForm() {
    hideElement(elements.greetingResult);
    hideElement(elements.errorMessage);
    elements.userNameInput.focus();
}

// API Functions
async function checkApiHealth() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
        
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
            appState.apiHealthy = true;
            elements.apiStatus.classList.remove('error');
            elements.apiStatusText.textContent = 'API Connected';
            return true;
        } else {
            throw new Error(`API returned ${response.status}`);
        }
    } catch (error) {
        console.error('API Health Check Failed:', error);
        appState.apiHealthy = false;
        elements.apiStatus.classList.add('error');
        elements.apiStatusText.textContent = 'API Disconnected';
        return false;
    }
}

async function loadGreetingTypes() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        
        const response = await fetch(`${API_BASE_URL}/greeting-types`, {
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
            const data = await response.json();
            appState.greetingTypes = data.greeting_types;
            populateGreetingSelect();
        } else {
            throw new Error(`Failed to load greeting types: ${response.status}`);
        }
    } catch (error) {
        console.error('Failed to load greeting types:', error);
        // Use default options if API fails
        appState.greetingTypes = [
            {key: 'hello', label: 'Hello'},
            {key: 'hi', label: 'Hi'},
            {key: 'welcome', label: 'Welcome'},
            {key: 'good_morning', label: 'Good Morning'},
            {key: 'good_afternoon', label: 'Good Afternoon'},
            {key: 'good_evening', label: 'Good Evening'}
        ];
        populateGreetingSelect();
    }
}

function populateGreetingSelect() {
    const select = elements.greetingTypeSelect;
    select.innerHTML = ''; // Clear existing options
    
    appState.greetingTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type.key;
        option.textContent = type.label;
        select.appendChild(option);
    });
}

async function submitGreeting(name, greetingType) {
    try {
        const requestData = {
            name: name.trim(),
            greeting_type: greetingType
        };
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
        
        const response = await fetch(`${API_BASE_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
            const data = await response.json();
            return { success: true, data };
        } else {
            const errorData = await response.json().catch(() => ({}));
            return { 
                success: false, 
                error: errorData.detail || `Server error: ${response.status}` 
            };
        }
    } catch (error) {
        console.error('Submit Greeting Error:', error);
        
        if (error.name === 'AbortError') {
            return { 
                success: false, 
                error: 'Request timeout. Please check your connection and try again.' 
            };
        }
        
        return { 
            success: false, 
            error: 'Network error. Please check if the backend is running on port 8000.' 
        };
    }
}

// Event Handlers
function handleFormSubmit(event) {
    event.preventDefault();
    
    if (appState.isLoading) return;
    
    const name = elements.userNameInput.value.trim();
    const greetingType = elements.greetingTypeSelect.value;
    
    // Validation
    if (!name) {
        showError('Please enter your name!');
        elements.userNameInput.focus();
        return;
    }
    
    if (name.length > 100) {
        showError('Name is too long! Please use a shorter name.');
        return;
    }
    
    // Basic client-side validation for invalid characters
    if (/[<>"']/.test(name)) {
        showError('Name contains invalid characters. Please use only letters, numbers, and basic punctuation.');
        return;
    }
    
    // Submit the greeting
    processGreeting(name, greetingType);
}

async function processGreeting(name, greetingType) {
    setLoadingState(true);
    
    try {
        const result = await submitGreeting(name, greetingType);
        
        if (result.success) {
            showGreeting(result.data);
        } else {
            showError(result.error);
        }
    } catch (error) {
        console.error('Processing Error:', error);
        showError('An unexpected error occurred. Please try again.');
    } finally {
        setLoadingState(false);
    }
}

function handleNewGreeting() {
    resetForm();
    elements.userNameInput.value = '';
    elements.greetingTypeSelect.selectedIndex = 0;
}

function handleTryAgain() {
    resetForm();
    elements.userNameInput.focus();
}

// Input Enhancement
function enhanceInputs() {
    // Add input animation and validation feedback
    elements.userNameInput.addEventListener('input', function() {
        const value = this.value.trim();
        if (value.length > 100) {
            this.style.borderColor = '#f56565';
        } else if (value.length > 0) {
            this.style.borderColor = 'var(--primary-green)';
        } else {
            this.style.borderColor = 'var(--mint-green)';
        }
        
        // Check for invalid characters
        if (/[<>"']/.test(value)) {
            this.style.borderColor = '#f56565';
        }
    });
    
    // Add enter key support for form submission
    elements.userNameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !appState.isLoading) {
            handleFormSubmit(e);
        }
    });
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (!elements.greetingResult.classList.contains('hidden') ||
                !elements.errorMessage.classList.contains('hidden')) {
                resetForm();
            }
        }
    });
}

// Initialization
async function initializeApp() {
    console.log('🌱 Initializing Green Greeting App...');
    console.log('API Base URL:', API_BASE_URL);
    
    // Set up event listeners
    elements.greetingForm.addEventListener('submit', handleFormSubmit);
    elements.newGreetingBtn.addEventListener('click', handleNewGreeting);
    elements.tryAgainBtn.addEventListener('click', handleTryAgain);
    
    // Enhance inputs
    enhanceInputs();
    
    // Check API health
    await checkApiHealth();
    
    // Load greeting types from API
    await loadGreetingTypes();
    
    // Focus on name input
    elements.userNameInput.focus();
    
    // Set up periodic health check
    setInterval(checkApiHealth, 30000); // Check every 30 seconds
    
    console.log('✅ App initialized successfully!');
}

// Error Handling
window.addEventListener('error', function(event) {
    console.error('Global Error:', event.error);
    if (elements.errorMessage && elements.errorMessage.classList.contains('hidden')) {
        showError('An unexpected error occurred. Please refresh the page.');
    }
});

// Start the application when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Export for debugging (optional)
if (typeof window !== 'undefined') {
    window.greetingApp = {
        elements,
        appState,
        checkApiHealth,
        loadGreetingTypes,
        submitGreeting,
        API_BASE_URL
    };
}