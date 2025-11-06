// Configuration - Use environment variable or fallback to relative API path
const API_URL = window.API_URL || '/api';

// Get DOM elements
const greetingForm = document.getElementById('greetingForm');
const nameInput = document.getElementById('nameInput');
const responseArea = document.getElementById('responseArea');
const greetingMessage = document.getElementById('greetingMessage');
const errorArea = document.getElementById('errorArea');
const errorMessage = document.getElementById('errorMessage');

// Form submit handler
greetingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = nameInput.value.trim();
    
    if (!name) {
        showError('Please enter a name');
        return;
    }
    
    // Hide previous messages
    hideMessages();
    
    try {
        // Call the backend API
        const response = await fetch(`${API_URL}/greet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const errorMsg = errorData.detail || `HTTP error! status: ${response.status}`;
            throw new Error(errorMsg);
        }
        
        const data = await response.json();
        showGreeting(data.message);
        
    } catch (error) {
        console.error('Error:', error);
        let errorMsg = 'Failed to connect to the server. Please make sure the backend is running.';
        
        if (error.message.includes('422')) {
            errorMsg = 'Invalid input. Please check your name and try again.';
        } else if (error.message.includes('500')) {
            errorMsg = 'Server error. Please try again later.';
        } else if (error.message && !error.message.includes('Failed to fetch')) {
            errorMsg = error.message;
        }
        
        showError(errorMsg);
    }
});

// Show greeting message
function showGreeting(message) {
    greetingMessage.textContent = message;
    responseArea.style.display = 'block';
    errorArea.style.display = 'none';
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorArea.style.display = 'block';
    responseArea.style.display = 'none';
}

// Hide all messages
function hideMessages() {
    responseArea.style.display = 'none';
    errorArea.style.display = 'none';
}

// Add some visual feedback on input
nameInput.addEventListener('input', () => {
    if (errorArea.style.display !== 'none') {
        hideMessages();
    }
});
