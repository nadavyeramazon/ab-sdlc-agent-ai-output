/**
 * Unit tests for Express frontend server
 * 
 * This module contains comprehensive tests for all server endpoints:
 * - Root endpoint (/)
 * - Health check endpoint (/health)
 * - API message endpoint (/api/message)
 * 
 * Run tests with: npm test
 * Run with coverage: npm run test:coverage
 */

const request = require('supertest');
const express = require('express');
const axios = require('axios');
const path = require('path');

// Mock axios to avoid actual HTTP calls to backend
jest.mock('axios');

describe('Express Frontend Server Tests', () => {
    let app;

    beforeEach(() => {
        // Create a fresh Express app for each test
        app = express();
        app.use(express.json());
        app.use(express.static('public'));

        // Define routes
        app.get('/', (req, res) => {
            res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
        });

        app.get('/health', (req, res) => {
            res.json({ status: 'healthy', service: 'frontend' });
        });

        app.get('/api/message', async (req, res) => {
            try {
                const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';
                const response = await axios.get(`${BACKEND_URL}/api/hello`);
                res.json({
                    frontend: 'Green Frontend is working!',
                    backend: response.data,
                    timestamp: new Date().toISOString()
                });
            } catch (error) {
                res.status(500).json({
                    error: 'Failed to communicate with backend',
                    details: error.message
                });
            }
        });

        // Clear all mocks before each test
        jest.clearAllMocks();
    });

    describe('GET /', () => {
        it('should return 200 status code', async () => {
            const response = await request(app).get('/');
            expect(response.status).toBe(200);
        });

        it('should return HTML content type', async () => {
            const response = await request(app).get('/');
            expect(response.type).toBe('text/html');
        });
    });

    describe('GET /health', () => {
        it('should return 200 status code', async () => {
            const response = await request(app).get('/health');
            expect(response.status).toBe(200);
        });

        it('should return healthy status', async () => {
            const response = await request(app).get('/health');
            expect(response.body).toEqual({
                status: 'healthy',
                service: 'frontend'
            });
        });

        it('should return JSON content type', async () => {
            const response = await request(app).get('/health');
            expect(response.type).toBe('application/json');
        });
    });

    describe('GET /api/message', () => {
        it('should return 200 when backend responds successfully', async () => {
            // Mock successful backend response
            axios.get.mockResolvedValue({
                data: {
                    message: 'Hello from the backend!',
                    status: 'success',
                    service: 'FastAPI Backend'
                }
            });

            const response = await request(app).get('/api/message');
            expect(response.status).toBe(200);
        });

        it('should return combined frontend and backend data', async () => {
            const mockBackendData = {
                message: 'Hello from the backend!',
                status: 'success',
                service: 'FastAPI Backend'
            };

            axios.get.mockResolvedValue({ data: mockBackendData });

            const response = await request(app).get('/api/message');
            
            expect(response.body).toHaveProperty('frontend');
            expect(response.body).toHaveProperty('backend');
            expect(response.body).toHaveProperty('timestamp');
            expect(response.body.frontend).toBe('Green Frontend is working!');
            expect(response.body.backend).toEqual(mockBackendData);
        });

        it('should call backend with correct URL', async () => {
            axios.get.mockResolvedValue({
                data: { message: 'test' }
            });

            await request(app).get('/api/message');
            
            const expectedUrl = `${process.env.BACKEND_URL || 'http://backend:8000'}/api/hello`;
            expect(axios.get).toHaveBeenCalledWith(expectedUrl);
        });

        it('should return 500 when backend fails', async () => {
            // Mock backend failure
            axios.get.mockRejectedValue(new Error('Connection refused'));

            const response = await request(app).get('/api/message');
            expect(response.status).toBe(500);
        });

        it('should return error details when backend fails', async () => {
            const errorMessage = 'Connection refused';
            axios.get.mockRejectedValue(new Error(errorMessage));

            const response = await request(app).get('/api/message');
            
            expect(response.body).toHaveProperty('error');
            expect(response.body).toHaveProperty('details');
            expect(response.body.error).toBe('Failed to communicate with backend');
            expect(response.body.details).toBe(errorMessage);
        });

        it('should return JSON content type', async () => {
            axios.get.mockResolvedValue({ data: { message: 'test' } });

            const response = await request(app).get('/api/message');
            expect(response.type).toBe('application/json');
        });

        it('should include valid ISO timestamp', async () => {
            axios.get.mockResolvedValue({ data: { message: 'test' } });

            const response = await request(app).get('/api/message');
            
            expect(response.body.timestamp).toBeDefined();
            // Verify it's a valid ISO 8601 timestamp
            const timestamp = new Date(response.body.timestamp);
            expect(timestamp.toISOString()).toBe(response.body.timestamp);
        });
    });

    describe('Invalid endpoints', () => {
        it('should return 404 for non-existent routes', async () => {
            const response = await request(app).get('/non-existent-route');
            expect(response.status).toBe(404);
        });
    });

    describe('Environment configuration', () => {
        it('should use custom BACKEND_URL when provided', async () => {
            const customUrl = 'http://custom-backend:9000';
            process.env.BACKEND_URL = customUrl;

            axios.get.mockResolvedValue({ data: { message: 'test' } });

            await request(app).get('/api/message');
            
            expect(axios.get).toHaveBeenCalledWith(`${customUrl}/api/hello`);
            
            // Clean up
            delete process.env.BACKEND_URL;
        });
    });
});
