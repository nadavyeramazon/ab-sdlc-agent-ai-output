// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const nameInput = document.getElementById('nameInput');
const greetingOutput = document.getElementById('greetingOutput');
const greetingMessage = document.getElementById('greetingMessage');
const errorOutput = document.getElementById('errorOutput');
const errorMessage = document.getElementById('errorMessage');

// Function to greet user
async function greetUser() {
    const name = nameInput.value.trim();
    
    // Validate input
    if (!name) {
        showError('Please enter your name!');
        return;
    }
    
    // Clear previous messages
    hideError();
    hideGreeting();
    
    try {
        // Make API call to backend
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
        
        // Display greeting message
        showGreeting(data.message);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the server. Please make sure the backend is running.');
    }
}

// Function to show greeting
function showGreeting(message) {
    greetingMessage.textContent = message;
    greetingOutput.classList.remove('hidden');
}

// Function to hide greeting
function hideGreeting() {
    greetingOutput.classList.add('hidden');
}

// Function to show error
function showError(message) {
    errorMessage.textContent = message;
    errorOutput.classList.remove('hidden');
}

// Function to hide error
function hideError() {
    errorOutput.classList.add('hidden');
}

// Add event listener for Enter key
nameInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        greetUser();
    }
});

// Clear error when user starts typing
nameInput.addEventListener('input', function() {
    if (!errorOutput.classList.contains('hidden')) {
        hideError();
    }
});

// Check backend health on page load
window.addEventListener('load', async function() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('Backend is healthy and ready!');
        }
    } catch (error) {
        console.warn('Backend is not responding. Make sure to start it with docker-compose up');
    }
});
