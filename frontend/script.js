// Green Greeting App - Frontend JavaScript

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    TIMEOUT: 10000, // 10 seconds
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000 // 1 second
};

// DOM Elements
const elements = {
    form: document.getElementById('greetingForm'),
    nameInput: document.getElementById('nameInput'),
    messageInput: document.getElementById('messageInput'),
    greetButton: document.getElementById('greetButton'),
    responseSection: document.getElementById('responseSection'),
    greetingMessage: document.getElementById('greetingMessage'),
    greetingDetails: document.getElementById('greetingDetails'),
    clearButton: document.getElementById('clearButton'),
    errorSection: document.getElementById('errorSection'),
    errorMessage: document.getElementById('errorMessage'),
    retryButton: document.getElementById('retryButton'),
    loadingSection: document.getElementById('loadingSection'),
    apiStatus: document.getElementById('apiStatus'),
    apiStatusText: document.getElementById('apiStatusText')
};

// State management
let currentRequest = null;
let retryCount = 0;

// Utility functions
class GreetingApp {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkApiStatus();
        this.focusNameInput();
    }

    bindEvents() {
        // Form submission
        elements.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Clear button
        elements.clearButton.addEventListener('click', () => {
            this.clearResults();
        });

        // Retry button
        elements.retryButton.addEventListener('click', () => {
            this.hideError();
            this.handleSubmit();
        });

        // Input validation
        elements.nameInput.addEventListener('input', () => {
            this.validateInput();
        });

        // Enter key on message input
        elements.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.handleSubmit();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.handleSubmit();
                } else if (e.key === 'r') {
                    e.preventDefault();
                    this.clearResults();
                }
            }
        });
    }

    async handleSubmit() {
        const name = elements.nameInput.value.trim();
        const message = elements.messageInput.value.trim();

        if (!this.validateForm(name)) {
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResponse();

        try {
            const response = await this.sendGreetingRequest(name, message);
            this.showResponse(response);
            retryCount = 0; // Reset retry count on success
        } catch (error) {
            console.error('Greeting request failed:', error);
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    validateForm(name) {
        if (!name) {
            this.showError('Please enter your name.');
            elements.nameInput.focus();
            return false;
        }

        if (name.length > 100) {
            this.showError('Name is too long. Please keep it under 100 characters.');
            elements.nameInput.focus();
            return false;
        }

        return true;
    }

    validateInput() {
        const name = elements.nameInput.value.trim();
        const isValid = name.length > 0 && name.length <= 100;
        
        elements.greetButton.disabled = !isValid;
        
        // Visual feedback
        if (name.length > 0) {
            elements.nameInput.style.borderColor = isValid ? 'var(--success-green)' : '#f44336';
        } else {
            elements.nameInput.style.borderColor = 'var(--border-color)';
        }
    }

    async sendGreetingRequest(name, message) {
        // Cancel previous request if it exists
        if (currentRequest) {
            currentRequest.abort();
        }

        const controller = new AbortController();
        currentRequest = controller;

        const timeoutId = setTimeout(() => {
            controller.abort();
        }, CONFIG.TIMEOUT);

        try {
            const requestBody = { name };
            if (message) {
                requestBody.message = message;
            }

            const response = await fetch(`${CONFIG.API_BASE_URL}/greet`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(requestBody),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred' }));
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new Error('Request was cancelled or timed out. Please try again.');
            }
            
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('Cannot connect to the server. Please check if the backend is running.');
            }
            
            throw error;
        } finally {
            currentRequest = null;
        }
    }

    showResponse(data) {
        elements.greetingMessage.textContent = data.greeting;
        
        const timestamp = new Date(data.timestamp).toLocaleString();
        elements.greetingDetails.innerHTML = `
            <strong>Name:</strong> ${this.escapeHtml(data.name)}<br>
            <strong>Time:</strong> ${timestamp}
        `;
        
        elements.responseSection.classList.remove('hidden');
        elements.responseSection.classList.add('fade-in');
        
        // Scroll to response
        setTimeout(() => {
            elements.responseSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }, 100);
    }

    showError(message) {
        elements.errorMessage.textContent = message;
        elements.errorSection.classList.remove('hidden');
        elements.errorSection.classList.add('fade-in');
        
        // Scroll to error
        setTimeout(() => {
            elements.errorSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }, 100);
    }

    showLoading() {
        elements.loadingSection.classList.remove('hidden');
        elements.greetButton.disabled = true;
        elements.greetButton.innerHTML = `
            <span class="button-text">Processing...</span>
            <span class="button-icon">⏳</span>
        `;
    }

    hideLoading() {
        elements.loadingSection.classList.add('hidden');
        elements.greetButton.disabled = false;
        elements.greetButton.innerHTML = `
            <span class="button-text">Get Greeting</span>
            <span class="button-icon">✨</span>
        `;
    }

    hideResponse() {
        elements.responseSection.classList.add('hidden');
        elements.responseSection.classList.remove('fade-in');
    }

    hideError() {
        elements.errorSection.classList.add('hidden');
        elements.errorSection.classList.remove('fade-in');
    }

    clearResults() {
        elements.nameInput.value = '';
        elements.messageInput.value = '';
        this.hideResponse();
        this.hideError();
        this.hideLoading();
        elements.nameInput.style.borderColor = 'var(--border-color)';
        elements.greetButton.disabled = true;
        this.focusNameInput();
    }

    focusNameInput() {
        setTimeout(() => {
            elements.nameInput.focus();
        }, 100);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async checkApiStatus() {
        try {
            elements.apiStatus.textContent = '🔄';
            elements.apiStatusText.textContent = 'Checking API...';
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);
            
            const response = await fetch(`${CONFIG.API_BASE_URL}/health`, {
                method: 'GET',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                elements.apiStatus.textContent = '🟢';
                elements.apiStatus.className = 'status-indicator connected';
                elements.apiStatusText.textContent = 'API Connected';
            } else {
                throw new Error('API not responding correctly');
            }
        } catch (error) {
            elements.apiStatus.textContent = '🔴';
            elements.apiStatus.className = 'status-indicator error';
            elements.apiStatusText.textContent = 'API Disconnected';
            console.warn('API health check failed:', error.message);
        }
    }

    // Public method to retry API status check
    retryApiStatus() {
        this.checkApiStatus();
    }
}

// Initialize the app when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.greetingApp = new GreetingApp();
    });
} else {
    window.greetingApp = new GreetingApp();
}

// Periodic API status check
setInterval(() => {
    if (window.greetingApp) {
        window.greetingApp.retryApiStatus();
    }
}, 30000); // Check every 30 seconds

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.greetingApp) {
        window.greetingApp.retryApiStatus();
    }
});

// Global error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    event.preventDefault();
});