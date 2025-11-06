// Jest setup file for DOM testing
// This file is referenced in package.json jest configuration

// Mock fetch for testing
global.fetch = jest.fn();

// Setup DOM environment
require('@testing-library/jest-dom');

// Mock window.location
delete window.location;
window.location = {
  hostname: 'localhost',
  port: '3000',
  protocol: 'http:',
  href: 'http://localhost:3000'
};

// Reset mocks before each test
beforeEach(() => {
  jest.resetAllMocks();
  fetch.mockClear();
});
