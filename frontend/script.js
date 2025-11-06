// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM elements
const nameInput = document.getElementById('nameInput');
const greetButton = document.getElementById('greetButton');
const greetingResult = document.getElementById('greetingResult');
const greetingMessage = document.getElementById('greetingMessage');
const errorMessage = document.getElementById('errorMessage');
const loadingSpinner = document.getElementById('loadingSpinner');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Focus on input when page loads
    nameInput.focus();
    
    // Add enter key support
    nameInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            greetUser();
        }
    });
    
    // Clear messages when user starts typing
    nameInput.addEventListener('input', function() {
        hideMessages();
        toggleGreetButton();
    });
    
    // Initial button state
    toggleGreetButton();
    
    // Check API health on load
    checkAPIHealth();
});

// Main greeting function
async function greetUser() {
    const name = nameInput.value.trim();
    
    // Validate input
    if (!name) {
        showError('Please enter your name!');
        nameInput.focus();
        return;
    }
    
    if (name.length > 50) {
        showError('Name is too long! Please keep it under 50 characters.');
        nameInput.focus();
        return;
    }
    
    try {
        // Show loading state
        showLoading();
        disableButton();
        
        // Make API call
        const response = await fetch(`${API_BASE_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showGreeting(data.message);
        } else {
            throw new Error(data.detail || 'Failed to get greeting');
        }
        
    } catch (error) {
        console.error('Error greeting user:', error);
        
        if (error.message.includes('fetch')) {
            showError('Unable to connect to the server. Please make sure the backend is running!');
        } else {
            showError(error.message || 'An unexpected error occurred. Please try again.');
        }
    } finally {
        hideLoading();
        enableButton();
    }
}

// Check if the API is running
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend API is running and healthy');
        }
    } catch (error) {
        console.warn('⚠️ Backend API appears to be offline');
        showError('Backend server is not running. Please start the backend service.');
    }
}

// UI utility functions
function showGreeting(message) {
    hideMessages();
    greetingMessage.textContent = message;
    greetingResult.classList.remove('hidden');
    
    // Add some celebration effect
    greetingResult.style.animation = 'none';
    greetingResult.offsetHeight; // Trigger reflow
    greetingResult.style.animation = 'slideIn 0.5s ease-out';
}

function showError(message) {
    hideMessages();
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

function showLoading() {
    hideMessages();
    loadingSpinner.style.display = 'block';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function hideMessages() {
    greetingResult.classList.add('hidden');
    errorMessage.classList.add('hidden');
    hideLoading();
}

function disableButton() {
    greetButton.disabled = true;
    greetButton.textContent = 'Greeting...';
}

function enableButton() {
    greetButton.disabled = false;
    greetButton.textContent = 'Greet Me!';
}

function toggleGreetButton() {
    const hasName = nameInput.value.trim().length > 0;
    greetButton.style.opacity = hasName ? '1' : '0.7';
}

// Add some nice interactions
nameInput.addEventListener('focus', function() {
    this.style.transform = 'scale(1.02)';
});

nameInput.addEventListener('blur', function() {
    this.style.transform = 'scale(1)';
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to greet
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        greetUser();
    }
    
    // Escape to clear
    if (event.key === 'Escape') {
        nameInput.value = '';
        hideMessages();
        nameInput.focus();
        toggleGreetButton();
    }
});

// Add some easter eggs
let clickCount = 0;
document.querySelector('header h1').addEventListener('click', function() {
    clickCount++;
    if (clickCount === 5) {
        this.style.animation = 'spin 1s ease-in-out';
        setTimeout(() => {
            this.style.animation = '';
            clickCount = 0;
        }, 1000);
        
        // Show a fun message
        showGreeting('🌿 You found the secret! You must really love green! 🌿');
    }
});

// Auto-clear greeting after some time
let greetingTimeout;
function showGreeting(message) {
    hideMessages();
    greetingMessage.textContent = message;
    greetingResult.classList.remove('hidden');
    
    // Add some celebration effect
    greetingResult.style.animation = 'none';
    greetingResult.offsetHeight; // Trigger reflow
    greetingResult.style.animation = 'slideIn 0.5s ease-out';
    
    // Auto-clear after 10 seconds
    clearTimeout(greetingTimeout);
    greetingTimeout = setTimeout(() => {
        greetingResult.style.opacity = '0.5';
    }, 10000);
}

// Restore opacity when user interacts
nameInput.addEventListener('input', function() {
    if (greetingResult.style.opacity === '0.5') {
        greetingResult.style.opacity = '1';
    }
});