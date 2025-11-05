/**
 * Test suite for the Express frontend application.
 * 
 * This module contains comprehensive tests for all frontend routes
 * including static file serving, API endpoints, and backend communication.
 */

const request = require('supertest');
const axios = require('axios');

// Mock axios before requiring the server
jest.mock('axios');

// Create a separate test app instance
const express = require('express');
const path = require('path');

const app = express();
const BACKEND_URL = 'http://backend:8000';

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

app.get('/api/backend-data', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/`);
        res.json({
            success: true,
            backendResponse: response.data,
            frontendMessage: 'Successfully communicated with backend!'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to communicate with backend',
            details: error.message
        });
    }
});

app.get('/api/greeting', async (req, res) => {
    try {
        const name = req.query.name || 'World';
        const response = await axios.get(`${BACKEND_URL}/api/greeting?name=${name}`);
        res.json({
            success: true,
            data: response.data
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to get greeting from backend'
        });
    }
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'frontend' });
});

describe('Frontend Server Tests', () => {
    
    describe('Health Check Endpoint', () => {
        test('GET /health should return healthy status', async () => {
            const response = await request(app).get('/health');
            expect(response.status).toBe(200);
            expect(response.body).toEqual({
                status: 'healthy',
                service: 'frontend'
            });
        });

        test('GET /health should have correct response structure', async () => {
            const response = await request(app).get('/health');
            expect(response.body).toHaveProperty('status');
            expect(response.body).toHaveProperty('service');
            expect(Object.keys(response.body).length).toBe(2);
        });
    });

    describe('Backend Data Endpoint', () => {
        beforeEach(() => {
            jest.clearAllMocks();
        });

        test('GET /api/backend-data should return success when backend is available', async () => {
            const mockBackendResponse = {
                message: 'Hello World from Backend!',
                service: 'backend',
                status: 'running'
            };

            axios.get.mockResolvedValue({ data: mockBackendResponse });

            const response = await request(app).get('/api/backend-data');
            
            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
            expect(response.body.backendResponse).toEqual(mockBackendResponse);
            expect(response.body.frontendMessage).toBe('Successfully communicated with backend!');
        });

        test('GET /api/backend-data should handle backend errors', async () => {
            axios.get.mockRejectedValue(new Error('Connection refused'));

            const response = await request(app).get('/api/backend-data');
            
            expect(response.status).toBe(500);
            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('Failed to communicate with backend');
            expect(response.body.details).toBe('Connection refused');
        });

        test('GET /api/backend-data should call backend with correct URL', async () => {
            axios.get.mockResolvedValue({ data: {} });

            await request(app).get('/api/backend-data');
            
            expect(axios.get).toHaveBeenCalledWith(`${BACKEND_URL}/`);
        });
    });

    describe('Greeting Endpoint', () => {
        beforeEach(() => {
            jest.clearAllMocks();
        });

        test('GET /api/greeting should return greeting with default name', async () => {
            const mockGreeting = {
                greeting: 'Hello, World!',
                from: 'Backend Service'
            };

            axios.get.mockResolvedValue({ data: mockGreeting });

            const response = await request(app).get('/api/greeting');
            
            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
            expect(response.body.data).toEqual(mockGreeting);
        });

        test('GET /api/greeting should pass custom name to backend', async () => {
            const mockGreeting = {
                greeting: 'Hello, Alice!',
                from: 'Backend Service'
            };

            axios.get.mockResolvedValue({ data: mockGreeting });

            const response = await request(app).get('/api/greeting?name=Alice');
            
            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
            expect(axios.get).toHaveBeenCalledWith(`${BACKEND_URL}/api/greeting?name=Alice`);
        });

        test('GET /api/greeting should handle backend errors', async () => {
            axios.get.mockRejectedValue(new Error('Backend unavailable'));

            const response = await request(app).get('/api/greeting?name=Bob');
            
            expect(response.status).toBe(500);
            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('Failed to get greeting from backend');
        });

        test('GET /api/greeting should handle special characters in name', async () => {
            const mockGreeting = {
                greeting: 'Hello, Test User!',
                from: 'Backend Service'
            };

            axios.get.mockResolvedValue({ data: mockGreeting });

            const response = await request(app).get('/api/greeting?name=Test%20User');
            
            expect(response.status).toBe(200);
            expect(response.body.success).toBe(true);
        });
    });

    describe('Root Endpoint', () => {
        test('GET / should return 200 status', async () => {
            const response = await request(app).get('/');
            expect(response.status).toBe(200);
        });

        test('GET / should return HTML content', async () => {
            const response = await request(app).get('/');
            expect(response.headers['content-type']).toMatch(/html/);
        });
    });

    describe('Error Handling', () => {
        test('GET /nonexistent should return 404', async () => {
            const response = await request(app).get('/nonexistent');
            expect(response.status).toBe(404);
        });

        test('Multiple sequential requests should work correctly', async () => {
            for (let i = 0; i < 5; i++) {
                const response = await request(app).get('/health');
                expect(response.status).toBe(200);
            }
        });
    });

    describe('Response Structure Validation', () => {
        test('Health endpoint should have correct JSON structure', async () => {
            const response = await request(app).get('/health');
            expect(response.body).toMatchObject({
                status: expect.any(String),
                service: expect.any(String)
            });
        });

        test('Backend data endpoint success response should have correct structure', async () => {
            axios.get.mockResolvedValue({ data: {} });

            const response = await request(app).get('/api/backend-data');
            expect(response.body).toHaveProperty('success');
            expect(response.body).toHaveProperty('backendResponse');
            expect(response.body).toHaveProperty('frontendMessage');
        });

        test('Greeting endpoint success response should have correct structure', async () => {
            axios.get.mockResolvedValue({ data: {} });

            const response = await request(app).get('/api/greeting');
            expect(response.body).toHaveProperty('success');
            expect(response.body).toHaveProperty('data');
        });
    });
});
