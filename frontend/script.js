// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Service status tracking
let serviceStatus = {
    healthy: true,
    lastCheck: null,
    retryCount: 0,
    maxRetries: 3
};

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
    console.log('🌿 Greeting App initialized with enhanced error handling');
    nameInput.focus();
    updateButtonState();
    
    // Check if backend is accessible
    checkBackendHealth();
}

// Enhanced backend health check with retry logic
async function checkBackendHealth() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout for health check
        
        const response = await fetch(`${API_BASE_URL}/health`, {
            signal: controller.signal,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
            const healthData = await response.json();
            serviceStatus.healthy = true;
            serviceStatus.lastCheck = new Date();
            serviceStatus.retryCount = 0;
            console.log('✅ Backend is healthy:', healthData);
        } else {
            throw new Error(`Health check failed with status: ${response.status}`);
        }
    } catch (error) {
        serviceStatus.healthy = false;
        serviceStatus.lastCheck = new Date();
        console.warn('⚠️ Backend health check failed:', error.message);
        
        // Show user-friendly message for service issues
        if (error.message.includes('serviceUnavailableException') || 
            error.message.includes('Bedrock') ||
            error.message.includes('503')) {
            showServiceUnavailableMessage();
        }
    }
}

// Show service unavailable message
function showServiceUnavailableMessage() {
    const message = 'Service temporarily unavailable. Retrying automatically...';
    showError(message);
    
    // Auto-retry after delay
    setTimeout(() => {
        if (serviceStatus.retryCount < serviceStatus.maxRetries) {
            serviceStatus.retryCount++;
            console.log(`🔄 Retrying health check (attempt ${serviceStatus.retryCount}/${serviceStatus.maxRetries})`);
            checkBackendHealth();
        }
    }, 3000);
}

// Handle greeting request with enhanced error handling
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
        const greeting = await fetchGreetingWithRetry(name);
        showGreeting(greeting);
        
        // Add some celebration effect
        celebrateSuccess();
        
    } catch (error) {
        console.error('Error fetching greeting:', error);
        handleGreetingError(error, name);
    } finally {
        setLoading(false);
    }
}

// Fetch greeting with retry mechanism for service unavailable scenarios
async function fetchGreetingWithRetry(name, attempt = 1) {
    const maxAttempts = 3;
    
    try {
        return await fetchGreeting(name);
    } catch (error) {
        console.warn(`Greeting attempt ${attempt} failed:`, error.message);
        
        // Handle specific service unavailable scenarios
        if ((error.message.includes('serviceUnavailableException') || 
             error.message.includes('Bedrock') ||
             error.message.includes('503')) && 
            attempt < maxAttempts) {
            
            console.log(`🔄 Retrying greeting request (attempt ${attempt + 1}/${maxAttempts})`);
            
            // Exponential backoff: wait longer between retries
            const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
            await new Promise(resolve => setTimeout(resolve, delay));
            
            return await fetchGreetingWithRetry(name, attempt + 1);
        }
        
        throw error;
    }
}

// Enhanced fetch greeting with better error handling
async function fetchGreeting(name) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout
    
    try {
        const response = await fetch(`${API_BASE_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ name }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            
            // Handle specific HTTP status codes
            if (response.status === 503) {
                throw new Error('serviceUnavailableException: Service temporarily unavailable');
            } else if (response.status === 500) {
                throw new Error('Internal server error occurred');
            } else if (response.status === 400) {
                throw new Error(errorData.detail || 'Invalid request');
            }
            
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update service status on successful response
        serviceStatus.healthy = true;
        serviceStatus.retryCount = 0;
        
        return data;
        
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please try again.');
        }
        
        if (error.message.includes('fetch') && !error.message.includes('serviceUnavailableException')) {
            throw new Error('Could not connect to server. Please make sure the backend is running.');
        }
        
        throw error;
    }
}

// Enhanced error handling for greeting requests
function handleGreetingError(error, name) {
    let errorMessage = error.message;
    let showFallbackOption = false;
    
    // Handle specific error types
    if (error.message.includes('serviceUnavailableException') || 
        error.message.includes('Bedrock') ||
        error.message.includes('503')) {
        
        errorMessage = 'External service temporarily unavailable. ';
        showFallbackOption = true;
        
    } else if (error.message.includes('timeout')) {
        errorMessage = 'Request timed out. Please check your connection and try again.';
        
    } else if (error.message.includes('connect')) {
        errorMessage = 'Cannot connect to server. Please make sure the backend is running.';
        
    } else if (error.message.includes('400')) {
        errorMessage = 'Invalid input. Please check your name and try again.';
    }
    
    // Show error with optional fallback
    if (showFallbackOption) {
        showErrorWithFallback(errorMessage, name);
    } else {
        showError(errorMessage);
    }
}

// Show error with fallback option
function showErrorWithFallback(message, name) {
    const fallbackMessage = `${message}Would you like to use a simple greeting instead?`;
    
    // Create a custom error message with retry button
    errorText.innerHTML = `
        <div class="error-content">
            <p>${fallbackMessage}</p>
            <button id="fallbackButton" class="fallback-btn" onclick="showFallbackGreeting('${name}')">
                Use Simple Greeting
            </button>
            <button id="retryButton" class="retry-btn" onclick="retryGreeting('${name}')">
                Retry Request
            </button>
        </div>
    `;
    
    errorMessage.classList.remove('hidden');
    
    // Auto-hide error after 10 seconds
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 10000);
}

// Show fallback greeting when service is unavailable
function showFallbackGreeting(name) {
    const fallbackGreetings = [
        `Hello, ${name}! Welcome to our green-themed application!`,
        `Greetings, ${name}! Thanks for visiting our eco-friendly platform!`,
        `Hi ${name}! We're glad you're here!`,
        `Welcome, ${name}! Enjoy your stay!`
    ];
    
    // Use a simple method to pick a greeting
    const greetingIndex = name.length % fallbackGreetings.length;
    const fallbackMessage = fallbackGreetings[greetingIndex] + ' (Offline mode)';
    
    const fallbackGreeting = {
        message: fallbackMessage,
        name: name,
        status: 'fallback'
    };
    
    showGreeting(fallbackGreeting);
    clearMessages();
    
    console.log('🔄 Showed fallback greeting for:', name);
}

// Retry greeting request
function retryGreeting(name) {
    clearMessages();
    nameInput.value = name;
    handleGreeting();
}

// Show greeting result with status indication
function showGreeting(greeting) {
    greetingMessage.textContent = greeting.message;
    greetingName.textContent = `For: ${greeting.name}`;
    
    // Add status indicator
    if (greeting.status === 'fallback') {
        greetingName.textContent += ' (Offline Mode)';
        greetingResult.classList.add('fallback-mode');
    } else {
        greetingResult.classList.remove('fallback-mode');
    }
    
    greetingResult.classList.remove('hidden');
    
    // Scroll to result
    greetingResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error message
function showError(message) {
    errorText.innerHTML = `<p>${message}</p>`;
    errorMessage.classList.remove('hidden');
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

// Clear all messages
function clearMessages() {
    greetingResult.classList.remove('hidden');
    errorMessage.classList.add('hidden');
    greetingResult.classList.remove('fallback-mode');
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

// Enhanced connection monitoring
window.addEventListener('online', function() {
    console.log('🌐 Connection restored');
    serviceStatus.retryCount = 0;
    checkBackendHealth();
    showError('Connection restored! You can try again now.');
});

window.addEventListener('offline', function() {
    console.log('🌐 Connection lost');
    serviceStatus.healthy = false;
    showError('Internet connection lost. Please check your connection.');
});

// Handle unhandled errors with specific service unavailable handling
window.addEventListener('error', function(e) {
    console.error('Unhandled error:', e.error);
    
    if (e.error && (e.error.message.includes('serviceUnavailableException') || 
                   e.error.message.includes('Bedrock'))) {
        showError('Service temporarily unavailable. Please try again in a moment.');
    } else {
        showError('An unexpected error occurred. Please refresh the page.');
    }
});

// Periodic health check (every 30 seconds)
setInterval(() => {
    if (!serviceStatus.healthy && serviceStatus.retryCount < serviceStatus.maxRetries) {
        console.log('🔄 Periodic health check...');
        checkBackendHealth();
    }
}, 30000);

// Debug mode (for development)
if (localStorage.getItem('debug') === 'true') {
    console.log('🐛 Debug mode enabled');
    window.greetingApp = {
        nameInput,
        greetButton,
        clearButton,
        API_BASE_URL,
        serviceStatus,
        fetchGreeting,
        showGreeting,
        showError,
        clearMessages,
        showFallbackGreeting,
        checkBackendHealth
    };
}