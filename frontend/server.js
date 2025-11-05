const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

// Serve static files
app.use(express.static('public'));

// Root route - serve the HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API endpoint to communicate with backend
app.get('/api/backend-data', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/`);
        res.json({
            success: true,
            backendResponse: response.data,
            frontendMessage: 'Successfully communicated with backend!'
        });
    } catch (error) {
        console.error('Error communicating with backend:', error.message);
        res.status(500).json({
            success: false,
            error: 'Failed to communicate with backend',
            details: error.message
        });
    }
});

// Get greeting from backend
app.get('/api/greeting', async (req, res) => {
    try {
        const name = req.query.name || 'World';
        const response = await axios.get(`${BACKEND_URL}/api/greeting?name=${name}`);
        res.json({
            success: true,
            data: response.data
        });
    } catch (error) {
        console.error('Error getting greeting from backend:', error.message);
        res.status(500).json({
            success: false,
            error: 'Failed to get greeting from backend'
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'frontend' });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Frontend server running on port ${PORT}`);
    console.log(`Backend URL: ${BACKEND_URL}`);
});
