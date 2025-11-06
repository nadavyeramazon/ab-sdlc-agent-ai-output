// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const nameInput = document.getElementById('nameInput');
const greetButton = document.getElementById('greetButton');
const clearButton = document.getElementById('clearButton');
const greetingResult = document.getElementById('greetingResult');
const greetingMessage = document.getElementById('greetingMessage');
const greetingName = document.getElementById('greetingName');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// State management
let isLoading = false;

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

nameInput.addEventListener('input', function() {
    clearMessages();
    updateButtonState();
});

// Allow Enter key to submit
nameInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !isLoading && nameInput.value.trim()) {
        handleGreeting();
    }
});

greetButton.addEventListener('click', handleGreeting);
clearButton.addEventListener('click', handleClear);

// Initialize the application
function initializeApp() {
    console.log('🌿 Greeting App initialized');
    nameInput.focus();
    updateButtonState();
    
    // Check if backend is accessible
    checkBackendHealth();
}

// Check backend health
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend is healthy');
        } else {
            console.warn('⚠️ Backend health check failed');
        }
    } catch (error) {
        console.warn('⚠️ Could not connect to backend:', error.message);
    }
}

// Handle greeting request
async function handleGreeting() {
    const name = nameInput.value.trim();
    
    if (!name) {
        showError('Please enter your name first!');
        nameInput.focus();
        return;
    }
    
    if (name.length > 50) {
        showError('Name is too long! Please keep it under 50 characters.');
        return;
    }
    
    setLoading(true);
    clearMessages();
    
    try {
        const greeting = await fetchGreeting(name);
        showGreeting(greeting);
        
        // Add some celebration effect
        celebrateSuccess();
        
    } catch (error) {
        console.error('Error fetching greeting:', error);
        showError(`Failed to get greeting: ${error.message}`);
    } finally {
        setLoading(false);
    }
}

// Fetch greeting from backend
async function fetchGreeting(name) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
    
    try {
        const response = await fetch(`${API_BASE_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please try again.');
        }
        
        if (error.message.includes('fetch')) {
            throw new Error('Could not connect to server. Please make sure the backend is running.');
        }
        
        throw error;
    }
}

// Show greeting result
function showGreeting(greeting) {
    greetingMessage.textContent = greeting.message;
    greetingName.textContent = `For: ${greeting.name}`;
    greetingResult.classList.remove('hidden');
    
    // Scroll to result
    greetingResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error message
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

// Clear all messages
function clearMessages() {
    greetingResult.classList.add('hidden');
    errorMessage.classList.add('hidden');
}

// Handle clear button
function handleClear() {
    nameInput.value = '';
    clearMessages();
    updateButtonState();
    nameInput.focus();
}

// Set loading state
function setLoading(loading) {
    isLoading = loading;
    
    if (loading) {
        loadingSpinner.classList.remove('hidden');
        greetButton.disabled = true;
        greetButton.textContent = 'Getting Greeting...';
    } else {
        loadingSpinner.classList.add('hidden');
        greetButton.disabled = false;
        greetButton.textContent = 'Get Greeting';
        updateButtonState();
    }
}

// Update button state based on input
function updateButtonState() {
    const hasInput = nameInput.value.trim().length > 0;
    greetButton.disabled = !hasInput || isLoading;
}

// Celebration effect
function celebrateSuccess() {
    // Add a subtle animation class
    greetingResult.style.transform = 'scale(1.02)';
    setTimeout(() => {
        greetingResult.style.transform = 'scale(1)';
    }, 200);
}

// Handle connection errors gracefully
window.addEventListener('online', function() {
    console.log('🌐 Connection restored');
    checkBackendHealth();
});

window.addEventListener('offline', function() {
    console.log('🌐 Connection lost');
    showError('Internet connection lost. Please check your connection.');
});

// Handle unhandled errors
window.addEventListener('error', function(e) {
    console.error('Unhandled error:', e.error);
    showError('An unexpected error occurred. Please refresh the page.');
});

// Debug mode (for development)
if (localStorage.getItem('debug') === 'true') {
    console.log('🐛 Debug mode enabled');
    window.greetingApp = {
        nameInput,
        greetButton,
        clearButton,
        API_BASE_URL,
        fetchGreeting,
        showGreeting,
        showError,
        clearMessages
    };
}
