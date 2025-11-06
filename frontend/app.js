// Configuration
const API_URL = 'http://localhost:8000'; // Change this to your backend URL

// DOM Elements
const nameInput = document.getElementById('nameInput');
const greetButton = document.getElementById('greetButton');
const greetingResult = document.getElementById('greetingResult');
const greetingMessage = document.getElementById('greetingMessage');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
greetButton.addEventListener('click', handleGreeting);
nameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleGreeting();
    }
});

// Auto-focus on input when page loads
window.addEventListener('load', () => {
    nameInput.focus();
});

/**
 * Handle the greeting request
 */
async function handleGreeting() {
    const name = nameInput.value.trim();
    
    // Hide previous messages
    hideMessages();
    
    // Validate input
    if (!name) {
        showError('Please enter your name!');
        return;
    }
    
    // Disable button while processing
    setButtonLoading(true);
    
    try {
        // Make API request
        const response = await fetch(`${API_URL}/greet`, {
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
        
        // Display greeting
        showGreeting(data.message);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Unable to connect to the greeting service. Please make sure the backend is running on ' + API_URL);
    } finally {
        setButtonLoading(false);
    }
}

/**
 * Show the greeting message
 */
function showGreeting(message) {
    greetingMessage.textContent = message;
    greetingResult.classList.remove('hidden');
    greetingResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show error message
 */
function showError(message) {
    const errorText = errorMessage.querySelector('p');
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
}

/**
 * Hide all messages
 */
function hideMessages() {
    greetingResult.classList.add('hidden');
    errorMessage.classList.add('hidden');
}

/**
 * Set button loading state
 */
function setButtonLoading(isLoading) {
    greetButton.disabled = isLoading;
    const btnText = greetButton.querySelector('.btn-text');
    
    if (isLoading) {
        btnText.textContent = 'Greeting...';
    } else {
        btnText.textContent = 'Greet Me!';
    }
}

/**
 * Check backend health on load
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend is healthy and ready');
        }
    } catch (error) {
        console.warn('⚠️ Backend connection failed. Make sure the backend is running.');
        console.warn('Expected backend URL:', API_URL);
    }
}

// Check backend health when page loads
checkBackendHealth();
