// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const fetchBtn = document.getElementById('fetchBtn');
const responseDiv = document.getElementById('response');
const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('messageInput');
const messageResponse = document.getElementById('messageResponse');

// Helper function to show response
function showResponse(element, message, isError = false) {
    element.className = `response-box show ${isError ? 'error' : 'success'}`;
    element.innerHTML = message;
}

// Helper function to hide response
function hideResponse(element) {
    element.className = 'response-box';
}

// Fetch data from backend
fetchBtn.addEventListener('click', async () => {
    const originalText = fetchBtn.innerHTML;
    fetchBtn.innerHTML = 'Loading<span class="loading"></span>';
    fetchBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showResponse(responseDiv, `
            <strong>Response from Backend:</strong><br>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `);
    } catch (error) {
        console.error('Error fetching data:', error);
        showResponse(responseDiv, `
            <strong>Error:</strong> ${error.message}<br>
            <small>Make sure the backend is running on ${API_BASE_URL}</small>
        `, true);
    } finally {
        fetchBtn.innerHTML = originalText;
        fetchBtn.disabled = false;
    }
});

// Handle form submission
messageForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    const submitBtn = messageForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = 'Sending<span class="loading"></span>';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showResponse(messageResponse, `
            <strong>Message sent successfully!</strong><br>
            <strong>Your message:</strong> ${data.received_message}<br>
            <strong>Response:</strong> ${data.response}<br>
            <strong>Timestamp:</strong> ${data.timestamp}
        `);
        
        // Clear input
        messageInput.value = '';
    } catch (error) {
        console.error('Error sending message:', error);
        showResponse(messageResponse, `
            <strong>Error:</strong> ${error.message}<br>
            <small>Make sure the backend is running on ${API_BASE_URL}</small>
        `, true);
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Health check on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✓ Backend is connected and healthy');
        }
    } catch (error) {
        console.warn('⚠ Backend is not reachable:', error.message);
    }
});