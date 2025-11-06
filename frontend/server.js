const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS
app.use(cors());

// Serve static files
app.use(express.static(path.join(__dirname)));

// Serve index.html for all routes (SPA)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🌱 Frontend server running on http://localhost:${PORT}`);
    console.log(`🚀 Green Greeting App is ready!`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('👋 Shutting down frontend server...');
    process.exit(0);
});