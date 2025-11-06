// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const nameInput = document.getElementById('nameInput');
const greetButton = document.getElementById('greetButton');
const responseContainer = document.getElementById('responseContainer');
const errorContainer = document.getElementById('errorContainer');
const greetingMessage = document.getElementById('greetingMessage');
const errorMessage = document.getElementById('errorMessage');
const loader = document.getElementById('loader');

// Event Listeners
greetButton.addEventListener('click', handleGreetClick);
nameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleGreetClick();
    }
});

nameInput.addEventListener('input', () => {
    hideMessages();
});

// Main greeting function
async function handleGreetClick() {
    const name = nameInput.value.trim();
    
    // Validate input
    if (!name) {
        showError('Please enter your name!');
        nameInput.focus();
        return;
    }
    
    // Show loader and disable button
    showLoader();
    greetButton.disabled = true;
    
    try {
        // Call the backend API
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
        
        // Display the greeting
        showGreeting(data.message);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the server. Please make sure the backend is running on port 8000.');
    } finally {
        hideLoader();
        greetButton.disabled = false;
    }
}

// Helper Functions
function showGreeting(message) {
    hideMessages();
    greetingMessage.textContent = message;
    responseContainer.classList.remove('hidden');
}

function showError(message) {
    hideMessages();
    errorMessage.textContent = message;
    errorContainer.classList.remove('hidden');
}

function hideMessages() {
    responseContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
}

function showLoader() {
    loader.classList.remove('hidden');
    hideMessages();
}

function hideLoader() {
    loader.classList.add('hidden');
}

// Check backend health on page load
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('Backend is healthy and ready!');
        }
    } catch (error) {
        console.warn('Backend is not responding. Make sure to start it with Docker Compose.');
    }
});
