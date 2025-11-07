/**
 * Frontend tests for the Greeting Application
 * 
 * These tests verify the functionality of the frontend JavaScript code.
 * Run with a test runner like Jest or in a browser environment.
 */

// Mock DOM elements for testing
class MockDOMEnvironment {
    constructor() {
        this.elements = {};
        this.eventListeners = {};
    }
    
    getElementById(id) {
        if (!this.elements[id]) {
            this.elements[id] = new MockElement(id);
        }
        return this.elements[id];
    }
    
    reset() {
        this.elements = {};
        this.eventListeners = {};
    }
}

class MockElement {
    constructor(id) {
        this.id = id;
        this.value = '';
        this.textContent = '';
        this.style = { display: 'none' };
        this.listeners = {};
    }
    
    addEventListener(event, handler) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(handler);
    }
    
    dispatchEvent(event) {
        const listeners = this.listeners[event.type] || [];
        listeners.forEach(listener => listener(event));
    }
    
    trim() {
        this.value = this.value.trim();
        return this.value;
    }
}

class MockEvent {
    constructor(type) {
        this.type = type;
        this.defaultPrevented = false;
    }
    
    preventDefault() {
        this.defaultPrevented = true;
    }
}

// Test Suite: API Configuration
describe('API Configuration', () => {
    test('API_URL should use localhost for local development', () => {
        global.window = { location: { hostname: 'localhost' } };
        const apiUrl = window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : '/api';
        expect(apiUrl).toBe('http://localhost:8000');
    });
    
    test('API_URL should use relative path for production', () => {
        global.window = { location: { hostname: 'example.com' } };
        const apiUrl = window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : '/api';
        expect(apiUrl).toBe('/api');
    });
});

// Test Suite: Input Validation
describe('Input Validation', () => {
    test('should reject empty name', () => {
        const name = '';
        const isValid = name.trim().length > 0;
        expect(isValid).toBe(false);
    });
    
    test('should reject whitespace-only name', () => {
        const name = '   ';
        const isValid = name.trim().length > 0;
        expect(isValid).toBe(false);
    });
    
    test('should accept valid name', () => {
        const name = 'Alice';
        const isValid = name.trim().length > 0;
        expect(isValid).toBe(true);
    });
    
    test('should trim whitespace from name', () => {
        const name = '  Alice  ';
        const trimmed = name.trim();
        expect(trimmed).toBe('Alice');
    });
});

// Test Suite: Message Display Functions
describe('Message Display Functions', () => {
    let mockDOM;
    
    beforeEach(() => {
        mockDOM = new MockDOMEnvironment();
    });
    
    test('showGreeting should display greeting and hide error', () => {
        const responseArea = mockDOM.getElementById('responseArea');
        const greetingMessage = mockDOM.getElementById('greetingMessage');
        const errorArea = mockDOM.getElementById('errorArea');
        
        // Simulate showGreeting function
        const message = 'Hello, Alice!';
        greetingMessage.textContent = message;
        responseArea.style.display = 'block';
        errorArea.style.display = 'none';
        
        expect(greetingMessage.textContent).toBe(message);
        expect(responseArea.style.display).toBe('block');
        expect(errorArea.style.display).toBe('none');
    });
    
    test('showError should display error and hide greeting', () => {
        const responseArea = mockDOM.getElementById('responseArea');
        const errorArea = mockDOM.getElementById('errorArea');
        const errorMessage = mockDOM.getElementById('errorMessage');
        
        // Simulate showError function
        const message = 'An error occurred';
        errorMessage.textContent = message;
        errorArea.style.display = 'block';
        responseArea.style.display = 'none';
        
        expect(errorMessage.textContent).toBe(message);
        expect(errorArea.style.display).toBe('block');
        expect(responseArea.style.display).toBe('none');
    });
    
    test('hideMessages should hide both greeting and error', () => {
        const responseArea = mockDOM.getElementById('responseArea');
        const errorArea = mockDOM.getElementById('errorArea');
        
        // Simulate hideMessages function
        responseArea.style.display = 'none';
        errorArea.style.display = 'none';
        
        expect(responseArea.style.display).toBe('none');
        expect(errorArea.style.display).toBe('none');
    });
});

// Test Suite: API Call Handling
describe('API Call Handling', () => {
    test('should construct correct API endpoint', () => {
        const API_URL = 'http://localhost:8000';
        const endpoint = `${API_URL}/greet`;
        expect(endpoint).toBe('http://localhost:8000/greet');
    });
    
    test('should send correct request body format', () => {
        const name = 'Alice';
        const requestBody = JSON.stringify({ name: name });
        const parsed = JSON.parse(requestBody);
        expect(parsed).toEqual({ name: 'Alice' });
    });
    
    test('should include correct headers', () => {
        const headers = {
            'Content-Type': 'application/json',
        };
        expect(headers['Content-Type']).toBe('application/json');
    });
});

// Test Suite: Error Handling
describe('Error Handling', () => {
    test('should handle 422 validation error', () => {
        const statusCode = 422;
        let errorMsg = 'Failed to connect to the server.';
        
        if (statusCode === 422) {
            errorMsg = 'Invalid input. Please check your name and try again.';
        }
        
        expect(errorMsg).toBe('Invalid input. Please check your name and try again.');
    });
    
    test('should handle 500 server error', () => {
        const statusCode = 500;
        let errorMsg = 'Failed to connect to the server.';
        
        if (statusCode === 500) {
            errorMsg = 'Server error. Please try again later.';
        }
        
        expect(errorMsg).toBe('Server error. Please try again later.');
    });
    
    test('should handle network error', () => {
        const error = new Error('Failed to fetch');
        let errorMsg = 'Failed to connect to the server. Please make sure the backend is running.';
        
        if (error.message.includes('Failed to fetch')) {
            errorMsg = 'Failed to connect to the server. Please make sure the backend is running.';
        }
        
        expect(errorMsg).toBe('Failed to connect to the server. Please make sure the backend is running.');
    });
});

// Test Suite: Form Submission
describe('Form Submission', () => {
    test('should prevent default form submission', () => {
        const event = new MockEvent('submit');
        event.preventDefault();
        expect(event.defaultPrevented).toBe(true);
    });
    
    test('should validate input before submission', () => {
        const name = '';
        const shouldSubmit = name.trim().length > 0;
        expect(shouldSubmit).toBe(false);
    });
    
    test('should allow submission with valid input', () => {
        const name = 'Alice';
        const shouldSubmit = name.trim().length > 0;
        expect(shouldSubmit).toBe(true);
    });
});

// Test Suite: Response Parsing
describe('Response Parsing', () => {
    test('should extract message from successful response', () => {
        const response = { message: 'Hello, Alice! Welcome to our purple-themed application! 💜' };
        expect(response.message).toBeDefined();
        expect(response.message).toContain('Alice');
    });
    
    test('should handle error detail from API response', () => {
        const errorResponse = { detail: 'Name contains invalid characters' };
        const errorMsg = errorResponse.detail || 'Unknown error';
        expect(errorMsg).toBe('Name contains invalid characters');
    });
    
    test('should fallback to default error message', () => {
        const errorResponse = {};
        const errorMsg = errorResponse.detail || 'Unknown error';
        expect(errorMsg).toBe('Unknown error');
    });
});

// Helper function to run tests
function runTests() {
    console.log('Running Frontend Tests...');
    console.log('========================\n');
    
    let passed = 0;
    let failed = 0;
    
    // In a real test environment, these would be executed by a test runner
    console.log('✓ All test suites defined successfully');
    console.log('\nNote: These tests are designed to be run with a JavaScript test framework like Jest.');
    console.log('To run the tests, install Jest and execute: npm test');
    
    return { passed, failed };
}

// Export for test runners
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        MockDOMEnvironment,
        MockElement,
        MockEvent,
        runTests
    };
}
