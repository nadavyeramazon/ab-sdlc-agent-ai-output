// Configuration
const BACKEND_URL = 'http://localhost:8000';

// DOM Elements
const fetchBtn = document.getElementById('fetchBtn');
const responseBox = document.getElementById('response');
const responseContent = document.getElementById('responseContent');
const errorBox = document.getElementById('error');
const errorContent = document.getElementById('errorContent');

// Fetch data from backend
async function fetchDataFromBackend() {
    try {
        // Show loading state
        fetchBtn.disabled = true;
        fetchBtn.textContent = 'Loading...';
        
        // Hide previous messages
        responseBox.style.display = 'none';
        errorBox.style.display = 'none';
        
        // Fetch from backend
        const response = await fetch(`${BACKEND_URL}/api/hello`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display response
        responseContent.textContent = JSON.stringify(data, null, 2);
        responseBox.style.display = 'block';
        
        console.log('Backend response:', data);
        
    } catch (error) {
        console.error('Error fetching data:', error);
        
        // Display error
        errorContent.textContent = `Failed to connect to backend: ${error.message}. Make sure the backend is running on ${BACKEND_URL}`;
        errorBox.style.display = 'block';
        
    } finally {
        // Reset button state
        fetchBtn.disabled = false;
        fetchBtn.textContent = 'Fetch Message from Backend';
    }
}

// Event Listeners
fetchBtn.addEventListener('click', fetchDataFromBackend);

// Optional: Fetch data on page load
window.addEventListener('load', () => {
    console.log('Frontend application loaded');
    console.log(`Backend URL configured as: ${BACKEND_URL}`);
});
