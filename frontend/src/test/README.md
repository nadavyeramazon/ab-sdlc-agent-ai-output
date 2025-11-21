# Frontend Testing Documentation

This directory contains test utilities and configurations for testing the React frontend application.

## Test Stack

- **Vitest**: Fast unit test framework powered by Vite
- **React Testing Library**: Testing utilities for React components
- **@testing-library/user-event**: Simulates user interactions
- **@testing-library/jest-dom**: Custom matchers for DOM elements
- **jsdom**: Browser environment simulation

## Running Tests

### Install Dependencies

```bash
npm install
```

### Run All Tests

```bash
npm test
```

### Run Tests in Watch Mode

```bash
npm test -- --watch
```

### Run Tests with UI

```bash
npm run test:ui
```

### Generate Coverage Report

```bash
npm run test:coverage
```

## Test Structure

### Test Files

- `App.test.jsx` - Comprehensive tests for the main App component
- `setup.js` - Global test configuration and setup
- `utils.jsx` - Reusable test utilities and helpers

### Test Organization

Tests are organized into descriptive test suites:

1. **Initial Rendering** - Tests for component mounting and initial state
2. **User Interactions** - Tests for button clicks and user events
3. **Loading State** - Tests for loading indicators and states
4. **Successful API Response** - Tests for successful data fetching
5. **Error Handling - Network Errors** - Tests for network failures
6. **Error Handling - HTTP Errors** - Tests for HTTP error responses
7. **State Management** - Tests for state transitions and updates
8. **Edge Cases** - Tests for unusual scenarios and boundary conditions
9. **Accessibility** - Tests for accessibility features

## Test Coverage

The test suite provides comprehensive coverage including:

- ✅ Component rendering and initial state
- ✅ User interactions (button clicks)
- ✅ Loading state management
- ✅ Successful API responses
- ✅ Network error handling
- ✅ HTTP error responses (404, 500, 403)
- ✅ State clearing and transitions
- ✅ Edge cases (rapid clicks, empty data, missing fields)
- ✅ Accessibility features

## Writing Tests

### Best Practices

1. **Test User Behavior, Not Implementation**
   - Use `screen.getByRole()` and `screen.getByText()` instead of querying by class names
   - Test what users see and do, not internal state

2. **Use User Event for Interactions**
   ```javascript
   const user = userEvent.setup()
   await user.click(button)
   ```

3. **Wait for Async Operations**
   ```javascript
   await waitFor(() => {
     expect(screen.getByText(/message/i)).toBeInTheDocument()
   })
   ```

4. **Mock External Dependencies**
   ```javascript
   const fetchMock = setupFetchMock()
   fetchMock.mockResolvedValueOnce(createMockResponse(data))
   ```

### Test Utilities

#### `renderWithProviders(component, options)`
Custom render function for wrapping components with providers.

#### `createMockResponse(data, options)`
Creates a mock fetch response object.

#### `setupFetchMock()`
Sets up global fetch mock for testing.

#### `resetFetchMock()`
Resets the fetch mock between tests.

## Example Test

```javascript
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'
import { createMockResponse, setupFetchMock } from './test/utils'

describe('App Component', () => {
  let fetchMock

  beforeEach(() => {
    fetchMock = setupFetchMock()
  })

  it('should display message on successful fetch', async () => {
    const user = userEvent.setup()
    const mockData = { message: 'Hello', timestamp: '2024-01-01' }
    fetchMock.mockResolvedValueOnce(createMockResponse(mockData))

    render(<App />)
    const button = screen.getByRole('button', { name: /get message/i })
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByText(/hello/i)).toBeInTheDocument()
    })
  })
})
```

## Debugging Tests

### View Test Results in Browser

```bash
npm run test:ui
```

### Debug Specific Test

```bash
npm test -- App.test.jsx --reporter=verbose
```

### Watch Mode for Development

```bash
npm test -- --watch
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

```bash
# Run tests once with coverage
npm run test:coverage

# Run tests in CI mode
npm test -- --run
```

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
