const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Serve the main HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API endpoint to communicate with backend
app.get('/api/message', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/api/hello`);
        res.json({
            frontend: 'Green Frontend is working!',
            backend: response.data,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        console.error('Error communicating with backend:', error.message);
        res.status(500).json({
            error: 'Failed to communicate with backend',
            details: error.message
        });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'frontend' });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Frontend server running on port ${PORT}`);
    console.log(`Backend URL configured as: ${BACKEND_URL}`);
});
