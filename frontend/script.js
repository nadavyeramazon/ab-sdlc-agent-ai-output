// Green Greeter Frontend JavaScript

// Utility function to get API base URL based on environment
function getApiBaseUrl() {
    // Check if we're running in a Docker environment
    if (window.location.hostname === 'localhost' && window.location.port === '8080') {
        // Running in Docker, use backend service name
        return 'http://backend:8000';
    }
    // Development or other environments
    return window.API_BASE_URL || 'http://localhost:8000';
}

// DOM elements
const nameInput = document.getElementById('nameInput');
const greetButton = document.getElementById('greetButton');
const resultDiv = document.getElementById('result');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const greetingMessage = document.getElementById('greetingMessage');
const timestamp = document.getElementById('timestamp');

// Utility functions for showing/hiding elements
function showElement(element) {
    element.classList.remove('hidden');
}

function hideElement(element) {
    element.classList.add('hidden');
}

// Function to add sparkle animation
function addSparkleEffect() {
    const sparkles = document.querySelectorAll('.sparkle');
    sparkles.forEach(sparkle => sparkle.remove());
    
    for (let i = 0; i < 10; i++) {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.style.left = Math.random() * 100 + '%';
        sparkle.style.top = Math.random() * 100 + '%';
        sparkle.style.animationDelay = Math.random() * 2 + 's';
        sparkle.innerHTML = '✨';
        document.body.appendChild(sparkle);
        
        setTimeout(() => {
            sparkle.remove();
        }, 3000);
    }
}

// Function to validate input
function validateInput(name) {
    const trimmedName = name.trim();
    if (trimmedName.length > 100) {
        throw new Error('Name is too long (maximum 100 characters)');
    }
    return trimmedName;
}

// Function to make API call
async function greetUser(name) {
    const apiUrl = getApiBaseUrl();
    const response = await fetch(`${apiUrl}/greet`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name })
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Function to format timestamp
function formatTimestamp(isoString) {
    try {
        const date = new Date(isoString);
        return date.toLocaleString(undefined, {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    } catch (error) {
        return 'Unknown time';
    }
}

// Main function to handle greeting
async function handleGreeting() {
    try {
        const rawName = nameInput.value;
        const validatedName = validateInput(rawName);
        
        // Hide previous results and show loading
        hideElement(resultDiv);
        hideElement(errorDiv);
        showElement(loadingDiv);
        
        // Disable button to prevent multiple requests
        greetButton.disabled = true;
        greetButton.textContent = 'Getting Greeting...';
        
        // Make API call
        const data = await greetUser(validatedName);
        
        // Display results
        greetingMessage.textContent = data.greeting;
        timestamp.textContent = `Generated at: ${formatTimestamp(data.timestamp)}`;
        
        // Hide loading and show results
        hideElement(loadingDiv);
        showElement(resultDiv);
        
        // Add visual effects
        resultDiv.classList.add('animate');
        addSparkleEffect();
        
        // Remove animation class after animation completes
        setTimeout(() => {
            resultDiv.classList.remove('animate');
        }, 600);
        
    } catch (error) {
        console.error('Error during greeting:', error);
        
        // Hide loading and show error
        hideElement(loadingDiv);
        showElement(errorDiv);
        
        // Update error message based on error type
        const errorElement = errorDiv.querySelector('p');
        if (error.message.includes('Name is too long')) {
            errorElement.textContent = '🌿 Name is too long! Please keep it under 100 characters.';
        } else if (error.message.includes('HTTP error')) {
            errorElement.textContent = '🌿 Server error! Please try again in a moment.';
        } else {
            errorElement.textContent = '🌿 Oops! Something went wrong. Please try again.';
        }
        
    } finally {
        // Re-enable button
        greetButton.disabled = false;
        greetButton.textContent = 'Get Green Greeting 🍃';
    }
}

// Event listeners
if (greetButton) {
    greetButton.addEventListener('click', handleGreeting);
}

if (nameInput) {
    nameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleGreeting();
        }
    });
    
    // Clear error when user starts typing
    nameInput.addEventListener('input', function() {
        if (!errorDiv.classList.contains('hidden')) {
            hideElement(errorDiv);
        }
    });
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Focus on input field when page loads
    if (nameInput) {
        nameInput.focus();
    }
    
    // Add some initial visual flair
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 100);
});

// Add sparkle animation styles dynamically
const sparkleStyles = `
.sparkle {
    position: fixed;
    pointer-events: none;
    z-index: 9999;
    font-size: 20px;
    animation: sparkleFloat 3s ease-out forwards;
}

@keyframes sparkleFloat {
    0% {
        opacity: 1;
        transform: translateY(0) scale(0);
    }
    50% {
        opacity: 1;
        transform: translateY(-50px) scale(1);
    }
    100% {
        opacity: 0;
        transform: translateY(-100px) scale(0.5);
    }
}

.loaded {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
`;

// Inject sparkle styles
const styleSheet = document.createElement('style');
styleSheet.textContent = sparkleStyles;
document.head.appendChild(styleSheet);

// Make functions available for testing (only in test environment)
if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    window.testHelpers = {
        getApiBaseUrl,
        greetUser,
        handleGreeting,
        showElement,
        hideElement,
        validateInput,
        formatTimestamp
    };
}
