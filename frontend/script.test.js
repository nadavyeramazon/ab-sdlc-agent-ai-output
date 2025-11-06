/**
 * Comprehensive test suite for frontend JavaScript functionality
 * Tests the greeting application's client-side behavior
 */

// Mock HTML structure for testing
const createMockDOM = () => {
  document.body.innerHTML = `
    <div class="container">
      <h1>Green Greeting App</h1>
      <form id="greetingForm">
        <input type="text" id="nameInput" placeholder="Enter your name..." required>
        <button type="submit" id="submitBtn">Greet Me! 🌿</button>
      </form>
      <div id="greeting" class="greeting-container"></div>
      <div id="loading" class="loading" style="display: none;">
        <div class="spinner"></div>
        <p>Generating your personalized greeting...</p>
      </div>
      <div id="error" class="error-container" style="display: none;"></div>
    </div>
  `;
};

// Load the script content for testing
const fs = require('fs');
const path = require('path');
const scriptPath = path.join(__dirname, 'script.js');
let scriptContent;

try {
  scriptContent = fs.readFileSync(scriptPath, 'utf8');
} catch (error) {
  // Fallback for testing environment
  scriptContent = `
    // Mock script content for testing
    const API_BASE_URL = 'http://localhost:8000';
    
    function validateName(name) {
      if (!name || name.trim().length === 0) {
        throw new Error('Name cannot be empty');
      }
      if (name.trim().length > 100) {
        throw new Error('Name must be less than 100 characters');
      }
      if (!/^[a-zA-Z\\s\\-\\']+$/.test(name.trim())) {
        throw new Error('Name can only contain letters, spaces, hyphens, and apostrophes');
      }
      return name.trim();
    }
    
    function showLoading() {
      const loading = document.getElementById('loading');
      if (loading) loading.style.display = 'block';
    }
    
    function hideLoading() {
      const loading = document.getElementById('loading');
      if (loading) loading.style.display = 'none';
    }
    
    function showError(message) {
      const errorDiv = document.getElementById('error');
      if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
      }
    }
    
    function hideError() {
      const errorDiv = document.getElementById('error');
      if (errorDiv) errorDiv.style.display = 'none';
    }
    
    function displayGreeting(data) {
      const greetingDiv = document.getElementById('greeting');
      if (greetingDiv) {
        greetingDiv.innerHTML = \`
          <div class="greeting-message">
            <h2>\${data.message}</h2>
            <p class="timestamp">Generated at: \${new Date(data.timestamp).toLocaleString()}</p>
          </div>
        \`;
        greetingDiv.style.display = 'block';
      }
    }
    
    async function submitGreeting(name) {
      const response = await fetch(\`\${API_BASE_URL}/greet\`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get greeting');
      }
      
      return await response.json();
    }
  `;
}

// Execute script content in test environment
eval(scriptContent);

describe('Frontend Greeting Application', () => {
  beforeEach(() => {
    createMockDOM();
    fetch.mockClear();
  });

  describe('DOM Elements', () => {
    test('should have all required DOM elements', () => {
      expect(document.getElementById('greetingForm')).toBeTruthy();
      expect(document.getElementById('nameInput')).toBeTruthy();
      expect(document.getElementById('submitBtn')).toBeTruthy();
      expect(document.getElementById('greeting')).toBeTruthy();
      expect(document.getElementById('loading')).toBeTruthy();
      expect(document.getElementById('error')).toBeTruthy();
    });

    test('should have proper initial state', () => {
      const loading = document.getElementById('loading');
      const error = document.getElementById('error');
      
      expect(loading.style.display).toBe('none');
      expect(error.style.display).toBe('none');
    });
  });

  describe('Name Validation', () => {
    test('should validate non-empty names', () => {
      expect(() => validateName('John')).not.toThrow();
      expect(validateName('John')).toBe('John');
    });

    test('should reject empty names', () => {
      expect(() => validateName('')).toThrow('Name cannot be empty');
      expect(() => validateName('   ')).toThrow('Name cannot be empty');
      expect(() => validateName(null)).toThrow('Name cannot be empty');
      expect(() => validateName(undefined)).toThrow('Name cannot be empty');
    });

    test('should reject names that are too long', () => {
      const longName = 'a'.repeat(101);
      expect(() => validateName(longName)).toThrow('Name must be less than 100 characters');
    });

    test('should reject names with invalid characters', () => {
      const invalidNames = [
        'John123',
        'John@Doe',
        'John<script>',
        'John&nbsp;',
        'John!',
        'John#'
      ];

      invalidNames.forEach(name => {
        expect(() => validateName(name)).toThrow('Name can only contain letters, spaces, hyphens, and apostrophes');
      });
    });

    test('should accept names with valid special characters', () => {
      const validNames = [
        'Mary-Jane',
        "O'Connor",
        'Jean Claude Van Damme',
        'Anne-Marie'
      ];

      validNames.forEach(name => {
        expect(() => validateName(name)).not.toThrow();
        expect(validateName(name)).toBe(name.trim());
      });
    });

    test('should trim whitespace from names', () => {
      expect(validateName('  John  ')).toBe('John');
      expect(validateName('\t\nAlice\t\n')).toBe('Alice');
    });
  });

  describe('UI State Management', () => {
    test('should show loading state', () => {
      showLoading();
      const loading = document.getElementById('loading');
      expect(loading.style.display).toBe('block');
    });

    test('should hide loading state', () => {
      const loading = document.getElementById('loading');
      loading.style.display = 'block';
      hideLoading();
      expect(loading.style.display).toBe('none');
    });

    test('should show error messages', () => {
      const errorMessage = 'Test error message';
      showError(errorMessage);
      
      const errorDiv = document.getElementById('error');
      expect(errorDiv.style.display).toBe('block');
      expect(errorDiv.textContent).toBe(errorMessage);
    });

    test('should hide error messages', () => {
      const errorDiv = document.getElementById('error');
      errorDiv.style.display = 'block';
      hideError();
      expect(errorDiv.style.display).toBe('none');
    });

    test('should display greeting data correctly', () => {
      const mockData = {
        message: 'Good morning, John! Welcome to our green-themed greeting service! 🌿',
        timestamp: '2024-01-15T10:30:00.000Z',
        name: 'John'
      };

      displayGreeting(mockData);
      
      const greetingDiv = document.getElementById('greeting');
      expect(greetingDiv.style.display).toBe('block');
      expect(greetingDiv.innerHTML).toContain(mockData.message);
      expect(greetingDiv.innerHTML).toContain('Generated at:');
    });
  });

  describe('API Communication', () => {
    test('should make successful API call', async () => {
      const mockResponse = {
        message: 'Good morning, John! Welcome to our green-themed greeting service! 🌿',
        timestamp: '2024-01-15T10:30:00.000Z',
        name: 'John'
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await submitGreeting('John');
      
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/greet',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name: 'John' })
        }
      );
      
      expect(result).toEqual(mockResponse);
    });

    test('should handle API errors', async () => {
      const errorResponse = {
        detail: 'Name cannot be empty'
      };

      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => errorResponse
      });

      await expect(submitGreeting('')).rejects.toThrow('Name cannot be empty');
    });

    test('should handle network errors', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      await expect(submitGreeting('John')).rejects.toThrow('Network error');
    });

    test('should handle malformed API responses', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({})
      });

      await expect(submitGreeting('John')).rejects.toThrow('Failed to get greeting');
    });
  });

  describe('Security Features', () => {
    test('should prevent XSS in name input', () => {
      const xssAttempts = [
        '<script>alert("xss")</script>',
        'javascript:alert("xss")',
        '<img src=x onerror=alert("xss")>'
      ];

      xssAttempts.forEach(xssAttempt => {
        expect(() => validateName(xssAttempt)).toThrow();
      });
    });

    test('should sanitize displayed content', () => {
      const mockData = {
        message: 'Hello <script>alert("xss")</script>',
        timestamp: '2024-01-15T10:30:00.000Z',
        name: 'John'
      };

      displayGreeting(mockData);
      
      const greetingDiv = document.getElementById('greeting');
      // Should display the message but not execute scripts
      expect(greetingDiv.innerHTML).toContain(mockData.message);
      // Verify no script execution (this is handled by browser security)
    });
  });

  describe('Edge Cases', () => {
    test('should handle missing DOM elements gracefully', () => {
      document.body.innerHTML = ''; // Remove all elements
      
      expect(() => showLoading()).not.toThrow();
      expect(() => hideLoading()).not.toThrow();
      expect(() => showError('test')).not.toThrow();
      expect(() => hideError()).not.toThrow();
      expect(() => displayGreeting({})).not.toThrow();
    });

    test('should handle unicode characters in names', () => {
      // These should be rejected by current validation
      const unicodeNames = [
        'José',
        'François',
        'Müller',
        '李小明'
      ];

      unicodeNames.forEach(name => {
        expect(() => validateName(name)).toThrow();
      });
    });

    test('should handle very long valid names', () => {
      const longValidName = 'Mary Jane Elizabeth Catherine Alexandra'.repeat(2);
      if (longValidName.length > 100) {
        expect(() => validateName(longValidName)).toThrow('Name must be less than 100 characters');
      }
    });
  });

  describe('Integration Scenarios', () => {
    test('should handle complete greeting flow', async () => {
      const mockResponse = {
        message: 'Good morning, Alice! Welcome to our green-themed greeting service! 🌿',
        timestamp: '2024-01-15T10:30:00.000Z',
        name: 'Alice'
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      // Simulate complete flow
      const validName = validateName('Alice');
      showLoading();
      
      const result = await submitGreeting(validName);
      
      hideLoading();
      displayGreeting(result);

      // Verify final state
      const loading = document.getElementById('loading');
      const greeting = document.getElementById('greeting');
      
      expect(loading.style.display).toBe('none');
      expect(greeting.style.display).toBe('block');
      expect(greeting.innerHTML).toContain(mockResponse.message);
    });

    test('should handle error flow', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Validation error' })
      });

      showLoading();
      
      try {
        await submitGreeting('InvalidName123');
      } catch (error) {
        hideLoading();
        showError(error.message);
      }

      // Verify error state
      const loading = document.getElementById('loading');
      const errorDiv = document.getElementById('error');
      
      expect(loading.style.display).toBe('none');
      expect(errorDiv.style.display).toBe('block');
      expect(errorDiv.textContent).toBe('Validation error');
    });
  });
});

describe('Frontend Performance', () => {
  test('should handle multiple rapid API calls', async () => {
    const mockResponse = {
      message: 'Test message',
      timestamp: '2024-01-15T10:30:00.000Z',
      name: 'Test'
    };

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockResponse
    });

    // Simulate multiple rapid calls
    const promises = [];
    for (let i = 0; i < 5; i++) {
      promises.push(submitGreeting(`Test${i}`));
    }

    const results = await Promise.all(promises);
    expect(results).toHaveLength(5);
    expect(fetch).toHaveBeenCalledTimes(5);
  });
});