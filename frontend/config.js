// API Configuration
// This can be overridden by environment-specific builds
window.API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : '/api';
