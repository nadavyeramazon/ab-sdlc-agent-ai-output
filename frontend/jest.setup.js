// Jest setup file for frontend testing
import '@testing-library/jest-dom';

// Mock fetch API for testing
global.fetch = jest.fn();

// Setup DOM testing environment
Object.defineProperty(window, 'location', {
  value: {
    href: 'http://localhost:3000',
    hostname: 'localhost',
    port: '3000',
    protocol: 'http:'
  },
  writable: true
});

// Mock console methods to reduce noise in tests
global.console = {
  ...console,
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
};

// Clean up after each test
afterEach(() => {
  jest.clearAllMocks();
  // Reset DOM
  document.body.innerHTML = '';
  document.head.innerHTML = '';
});