/**
 * Green Themed API Interface - Vanilla JavaScript
 * 
 * This script handles all interactions with the FastAPI backend.
 * No frameworks used - pure JavaScript for simplicity and performance.
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Utility Functions

/**
 * Display result in a result box
 * @param {string} elementId - The ID of the result box element
 * @param {string} message - The message to display
 * @param {string} type - The type of message ('success', 'error', 'loading')
 */
function displayResult(elementId, message, type = 'success') {
    const resultBox = document.getElementById(elementId);
    if (!resultBox) return;
    
    resultBox.className = `result-box show ${type}`;
    resultBox.textContent = message;
}

/**
 * Make an API request
 * @param {string} endpoint - The API endpoint to call
 * @returns {Promise<Object>} The JSON response
 */
async function makeApiRequest(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Format JSON for display
 * @param {Object} data - The data to format
 * @returns {string} Formatted JSON string
 */
function formatJSON(data) {
    return JSON.stringify(data, null, 2);
}

// Event Handlers

/**
 * Handle health check button click
 */
async function handleHealthCheck() {
    const resultId = 'healthResult';
    const button = document.getElementById('healthCheckBtn');
    
    // Show loading state
    button.disabled = true;
    displayResult(resultId, 'Checking health status...', 'loading');
    
    // Make API request
    const result = await makeApiRequest('/health');
    
    // Display result
    if (result.success) {
        const statusEmoji = result.data.status === 'healthy' ? '✅' : '⚠️';
        displayResult(
            resultId,
            `${statusEmoji} Status: ${result.data.status}\n\nFull Response:\n${formatJSON(result.data)}`,
            'success'
        );
    } else {
        displayResult(
            resultId,
            `❌ Error: ${result.error}\n\nPlease ensure the backend is running on ${API_BASE_URL}`,
            'error'
        );
    }
    
    button.disabled = false;
}

/**
 * Handle hello world button click
 */
async function handleHelloWorld() {
    const resultId = 'helloWorldResult';
    const button = document.getElementById('helloWorldBtn');
    
    // Show loading state
    button.disabled = true;
    displayResult(resultId, 'Fetching message...', 'loading');
    
    // Make API request
    const result = await makeApiRequest('/');
    
    // Display result
    if (result.success) {
        displayResult(
            resultId,
            `🎉 ${result.data.message}\n\nFull Response:\n${formatJSON(result.data)}`,
            'success'
        );
    } else {
        displayResult(
            resultId,
            `❌ Error: ${result.error}\n\nPlease ensure the backend is running on ${API_BASE_URL}`,
            'error'
        );
    }
    
    button.disabled = false;
}

/**
 * Handle personalized greeting
 */
async function handleGreeting() {
    const resultId = 'greetResult';
    const button = document.getElementById('greetBtn');
    const nameInput = document.getElementById('nameInput');
    const name = nameInput.value.trim();
    
    // Validate input
    if (!name) {
        displayResult(resultId, '⚠️ Please enter a name first!', 'error');
        nameInput.focus();
        return;
    }
    
    // Show loading state
    button.disabled = true;
    displayResult(resultId, 'Fetching personalized greeting...', 'loading');
    
    // Make API request
    const result = await makeApiRequest(`/hello/${encodeURIComponent(name)}`);
    
    // Display result
    if (result.success) {
        displayResult(
            resultId,
            `👋 ${result.data.message}\n\nFull Response:\n${formatJSON(result.data)}`,
            'success'
        );
    } else {
        displayResult(
            resultId,
            `❌ Error: ${result.error}\n\nPlease ensure the backend is running on ${API_BASE_URL}`,
            'error'
        );
    }
    
    button.disabled = false;
}

// Initialize Event Listeners

/**
 * Set up all event listeners when DOM is loaded
 */
function initializeEventListeners() {
    // Health Check button
    const healthCheckBtn = document.getElementById('healthCheckBtn');
    if (healthCheckBtn) {
        healthCheckBtn.addEventListener('click', handleHealthCheck);
    }
    
    // Hello World button
    const helloWorldBtn = document.getElementById('helloWorldBtn');
    if (helloWorldBtn) {
        helloWorldBtn.addEventListener('click', handleHelloWorld);
    }
    
    // Greet button
    const greetBtn = document.getElementById('greetBtn');
    if (greetBtn) {
        greetBtn.addEventListener('click', handleGreeting);
    }
    
    // Name input - allow Enter key to trigger greeting
    const nameInput = document.getElementById('nameInput');
    if (nameInput) {
        nameInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                handleGreeting();
            }
        });
    }
}

// Wait for DOM to be fully loaded before initializing
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeEventListeners);
} else {
    // DOM is already loaded
    initializeEventListeners();
}

// Log initialization
console.log('🌿 Green Themed API Interface initialized');
console.log(`📡 API Base URL: ${API_BASE_URL}`);