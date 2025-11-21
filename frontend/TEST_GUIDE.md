# Frontend Testing Guide

## Overview

This project uses **Vitest** and **React Testing Library** for comprehensive frontend testing.

## Test Coverage

The test suite includes:
- ✅ **Component Rendering Tests** - Verifies the App component renders correctly
- ✅ **Button Click Interaction Tests** - Tests user interactions and state changes
- ✅ **Loading State Tests** - Validates loading indicators and UI behavior
- ✅ **Error Handling Tests** - Tests error states, messages, and recovery scenarios
- ✅ **API Integration Tests** - Mocks and tests fetch calls to backend

## Running Tests

### Install Dependencies

```bash
cd frontend
npm install
```

### Run All Tests

```bash
npm test
```

### Run Tests in Watch Mode (for development)

```bash
npm run test:watch
```

### Run Tests with Coverage Report

```bash
npm run test:coverage
```

## Test Structure

### File: `src/App.test.jsx`

The test suite is organized into the following sections:

#### 1. Component Rendering
- Tests that the component renders without crashing
- Verifies all key UI elements are present (heading, button, containers)
- Checks initial state of the component

#### 2. Button Click Interactions
- Tests that clicking the button calls the fetch API
- Verifies success messages are displayed correctly
- Tests clearing of previous messages
- Handles responses with different data structures

#### 3. Loading States
- Tests loading indicator display during fetch
- Verifies button is disabled during loading
- Tests loading indicator disappears after fetch completes
- Ensures button is re-enabled after loading

#### 4. Error Handling
- Tests error messages for different HTTP status codes
- Tests network error handling
- Verifies error CSS classes are applied
- Tests error recovery scenarios
- Tests clearing of previous errors

#### 5. API URL Configuration
- Tests that environment variable VITE_API_URL is used correctly

#### 6. Message Display
- Tests correct CSS classes are applied
- Verifies conditional rendering logic

## Environment Variables

### VITE_API_URL

The API URL can be configured using the `VITE_API_URL` environment variable.

**Default:** `http://localhost:8000`

**Usage:**

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your API URL:
   ```
   VITE_API_URL=http://your-backend-url:8000
   ```

3. Restart the development server for changes to take effect.

## Test Best Practices

### Mocking

The test suite uses Vitest's `vi.fn()` to mock the global `fetch` API:

```javascript
global.fetch = vi.fn();
```

Each test clears mocks before running:

```javascript
beforeEach(() => {
  vi.clearAllMocks();
});
```

### User Interactions

Tests use `@testing-library/user-event` for realistic user interactions:

```javascript
const user = userEvent.setup();
await user.click(button);
```

### Async Testing

Tests use `waitFor` for async operations:

```javascript
await waitFor(() => {
  expect(screen.getByText('Success!')).toBeInTheDocument();
});
```

### Querying Elements

Tests use accessible queries from React Testing Library:

- `getByRole()` - Preferred for accessibility
- `getByText()` - For text content
- `queryBy...()` - When element may not exist
- `getBy...()` - When element must exist

## Common Test Patterns

### Testing Successful API Call

```javascript
global.fetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({ message: 'Success!' }),
});
```

### Testing API Error

```javascript
global.fetch.mockResolvedValueOnce({
  ok: false,
  status: 500,
});
```

### Testing Network Error

```javascript
global.fetch.mockRejectedValueOnce(new Error('Network error'));
```

## CI/CD Integration

The test command (`npm test`) is designed to:
- Run all tests once and exit
- Return non-zero exit code on failure (for CI/CD pipelines)
- Output results in a CI-friendly format

## Troubleshooting

### Tests Fail with "fetch is not defined"

Make sure the test setup correctly mocks the global fetch:
```javascript
global.fetch = vi.fn();
```

### Tests Fail with Missing DOM Matchers

Ensure `@testing-library/jest-dom` is properly configured in `src/test/setup.js`.

### Environment Variables Not Working in Tests

Vitest loads environment variables automatically. If needed, you can set them in `vite.config.js`:

```javascript
test: {
  env: {
    VITE_API_URL: 'http://test-api:8000'
  }
}
```

## Additional Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
