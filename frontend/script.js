// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const nameInput = document.getElementById('nameInput');
const greetButton = document.getElementById('greetButton');
const resultSection = document.getElementById('resultSection');
const greetingMessage = document.getElementById('greetingMessage');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
nameInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        getGreeting();
    }
});

/**
 * Fetch greeting from the backend API
 */
async function getGreeting() {
    const name = nameInput.value.trim();
    
    // Validate input
    if (!name) {
        showError('Please enter your name!');
        return;
    }
    
    // Hide previous messages
    hideMessages();
    
    // Disable button during request
    greetButton.disabled = true;
    greetButton.textContent = 'Loading...';
    
    try {
        // Make API request
        const response = await fetch(`${API_BASE_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showGreeting(data.message);
        
    } catch (error) {
        console.error('Error fetching greeting:', error);
        showError('Unable to connect to the backend. Please ensure the server is running!');
    } finally {
        // Re-enable button
        greetButton.disabled = false;
        greetButton.textContent = 'Get Greeting';
    }
}

/**
 * Display greeting message
 */
function showGreeting(message) {
    greetingMessage.textContent = message;
    resultSection.classList.remove('hidden');
    errorSection.classList.add('hidden');
}

/**
 * Display error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    resultSection.classList.add('hidden');
}

/**
 * Hide all messages
 */
function hideMessages() {
    resultSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

/**
 * Check backend health on page load
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('Backend is healthy!');
        }
    } catch (error) {
        console.warn('Backend health check failed:', error);
    }
}

// Initialize
checkBackendHealth();
