// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const nameInput = document.getElementById('nameInput');
const greetButton = document.getElementById('greetButton');
const greetingResult = document.getElementById('greetingResult');
const errorMessage = document.getElementById('errorMessage');

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners
    if (nameInput) {
        nameInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                getGreeting();
            }
        });
        
        // Clear error messages when user starts typing
        nameInput.addEventListener('input', function() {
            clearMessages();
        });
    }
    
    if (greetButton) {
        greetButton.addEventListener('click', getGreeting);
    }
});

// Main function to get greeting from backend
async function getGreeting() {
    const name = nameInput ? nameInput.value.trim() : '';
    
    // Clear previous messages
    clearMessages();
    
    // Validation
    if (!name) {
        showError('Please enter your name!');
        return;
    }
    
    if (name.length > 100) {
        showError('Name must be 100 characters or less!');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showGreeting(data.message);
        
    } catch (error) {
        console.error('Error fetching greeting:', error);
        
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showError('Unable to connect to the server. Please make sure the backend is running.');
        } else {
            showError(`Error: ${error.message}`);
        }
    } finally {
        hideLoading();
    }
}

// Display functions
function showGreeting(message) {
    if (greetingResult) {
        greetingResult.innerHTML = `<div class="success-message">${escapeHtml(message)}</div>`;
        greetingResult.style.display = 'block';
    }
}

function showError(message) {
    if (errorMessage) {
        errorMessage.innerHTML = `<div class="error-text">${escapeHtml(message)}</div>`;
        errorMessage.style.display = 'block';
    }
}

function showLoading() {
    if (greetButton) {
        greetButton.disabled = true;
        greetButton.textContent = 'Loading...';
    }
}

function hideLoading() {
    if (greetButton) {
        greetButton.disabled = false;
        greetButton.textContent = 'Get Greeting';
    }
}

function clearMessages() {
    if (greetingResult) {
        greetingResult.style.display = 'none';
        greetingResult.innerHTML = '';
    }
    if (errorMessage) {
        errorMessage.style.display = 'none';
        errorMessage.innerHTML = '';
    }
}

// Utility function to escape HTML and prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// Health check function for testing
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        return false;
    }
}

// Export functions for testing (if in a test environment)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getGreeting,
        showGreeting,
        showError,
        clearMessages,
        escapeHtml,
        checkBackendHealth
    };
}