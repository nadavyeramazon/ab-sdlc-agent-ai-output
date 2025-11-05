/**
 * Express Frontend Server
 * 
 * A simple Express.js server that serves a green-themed frontend
 * and communicates with the FastAPI backend microservice.
 * 
 * Environment Variables:
 *   PORT: Server port (default: 3000)
 *   BACKEND_URL: Backend service URL (default: http://backend:8000)
 *   LOG_LEVEL: Logging level (default: info)
 */

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

// Simple logging utility
const logger = {
    info: (msg) => console.log(`[INFO] ${new Date().toISOString()} - ${msg}`),
    error: (msg) => console.error(`[ERROR] ${new Date().toISOString()} - ${msg}`),
    warn: (msg) => console.warn(`[WARN] ${new Date().toISOString()} - ${msg}`)
};

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

logger.info('Frontend server initializing...');
logger.info(`Backend URL configured as: ${BACKEND_URL}`);

// Serve the main HTML page
app.get('/', (req, res) => {
    logger.info('Root endpoint accessed');
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API endpoint to communicate with backend
app.get('/api/message', async (req, res) => {
    logger.info('API message endpoint accessed');
    try {
        const response = await axios.get(`${BACKEND_URL}/api/hello`);
        logger.info('Successfully received response from backend');
        res.json({
            frontend: 'Green Frontend is working!',
            backend: response.data,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        logger.error(`Error communicating with backend: ${error.message}`);
        res.status(500).json({
            error: 'Failed to communicate with backend',
            details: error.message
        });
    }
});

// Health check
app.get('/health', (req, res) => {
    logger.info('Health check endpoint accessed');
    res.json({ status: 'healthy', service: 'frontend' });
});

// Only start server if not in test environment
if (process.env.NODE_ENV !== 'test') {
    app.listen(PORT, '0.0.0.0', () => {
        logger.info(`Frontend server running on port ${PORT}`);
    });
}

// Export app for testing
module.exports = app;
