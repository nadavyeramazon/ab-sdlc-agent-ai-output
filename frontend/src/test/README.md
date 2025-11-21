# Frontend Testing Guide

## Overview

This directory contains the test setup and utilities for the frontend application. Tests are written using:

- **Vitest** - Fast unit test framework compatible with Vite
- **React Testing Library** - For testing React components
- **@testing-library/user-event** - For simulating user interactions
- **@testing-library/jest-dom** - For enhanced DOM matchers

## Running Tests

### Install dependencies
```bash
npm install
```

### Run all tests once
```bash
npm test
```

### Run tests in watch mode (interactive)
```bash
npm run test:watch
```

### Run tests with coverage report
```bash
npm run test:coverage
```

Coverage reports will be generated in the `coverage/` directory.

## Test Structure

### Test Files Location
- Component tests are colocated with their components (e.g., `App.test.jsx` next to `App.jsx`)
- Test utilities and setup are in `src/test/`

### Test Categories

Our tests are organized into the following categories:

1. **Initial Render Tests** - Verify components render correctly
2. **State Management Tests** - Test React state updates and hooks
3. **API Integration Tests** - Mock and test API calls
4. **Validation Tests** - Test form validation logic
5. **User Interaction Tests** - Test click handlers, input changes, etc.
6. **Loading States Tests** - Test loading indicators and disabled states
7. **Error Handling Tests** - Test error messages and edge cases
8. **Accessibility Tests** - Test ARIA labels, keyboard navigation, etc.

## Test Coverage Requirements

The App component tests cover:

✅ **Component Rendering** (8 tests)
- Initial render of all UI elements
- Proper element attributes and ARIA labels

✅ **State Management** (10+ tests)
- useState hooks for message, loading, error states
- Greeting feature states
- State clearing and updates

✅ **API Call Handling** (15+ tests)
- Mocked fetch requests
- Success and error responses
- Proper HTTP methods and headers
- Response parsing

✅ **Validation Logic** (3 tests)
- Empty input validation
- Whitespace trimming
- Error message display

✅ **User Interactions** (12+ tests)
- Button clicks
- Input typing
- Form submissions
- Rapid consecutive clicks

✅ **Error Handling** (8+ tests)
- Network errors
- API errors with/without detail messages
- Malformed responses
- Empty responses

✅ **Edge Cases** (7 tests)
- Special characters in names
- Multiple rapid clicks
- Empty API responses
- Malformed JSON

✅ **Accessibility** (3 tests)
- Input labels
- Button roles
- Focus management

**Total: 65+ comprehensive tests**

## Writing New Tests

### Basic Test Structure

```javascript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('ComponentName', () => {
  beforeEach(() => {
    // Setup before each test
    vi.clearAllMocks();
  });

  it('should do something', async () => {
    // Arrange
    render(<ComponentName />);
    
    // Act
    await userEvent.click(screen.getByRole('button'));
    
    // Assert
    expect(screen.getByText('Expected text')).toBeInTheDocument();
  });
});
```

### Mocking Fetch

```javascript
global.fetch = vi.fn();

beforeEach(() => {
  fetch.mockClear();
});

// Mock successful response
fetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({ data: 'value' })
});

// Mock error response
fetch.mockRejectedValueOnce(new Error('Network error'));
```

### Testing Async Operations

```javascript
it('should handle async operations', async () => {
  render(<Component />);
  
  await userEvent.click(screen.getByRole('button'));
  
  await waitFor(() => {
    expect(screen.getByText('Success')).toBeInTheDocument();
  });
});
```

## Best Practices

1. **Test behavior, not implementation** - Focus on what users see and do
2. **Use accessible queries** - Prefer `getByRole`, `getByLabelText` over `getByTestId`
3. **Mock external dependencies** - Always mock fetch, localStorage, etc.
4. **Test user interactions** - Use `@testing-library/user-event` for realistic interactions
5. **Handle async operations** - Use `waitFor` for async state updates
6. **Clear mocks between tests** - Use `beforeEach` to reset mocks
7. **Test error states** - Don't just test the happy path
8. **Keep tests independent** - Each test should run in isolation

## Common Testing Patterns

### Testing Form Inputs
```javascript
const input = screen.getByPlaceholderText('Enter name');
await userEvent.type(input, 'John Doe');
expect(input).toHaveValue('John Doe');
```

### Testing Buttons
```javascript
const button = screen.getByRole('button', { name: /submit/i });
await userEvent.click(button);
```

### Testing Loading States
```javascript
expect(screen.getByText(/loading/i)).toBeInTheDocument();
```

### Testing Error Messages
```javascript
await waitFor(() => {
  expect(screen.getByText(/error message/i)).toBeInTheDocument();
});
```

## Debugging Tests

### View rendered output
```javascript
import { screen } from '@testing-library/react';
screen.debug(); // Prints the DOM
```

### Run specific test file
```bash
npm test App.test.jsx
```

### Run specific test
```bash
npm test -- -t "test name pattern"
```

## CI/CD Integration

Tests are automatically run in the CI/CD pipeline. All tests must pass before merging.

```bash
# This is run in CI
npm install
npm test
```

## Troubleshooting

### Tests timing out
- Increase timeout in vitest.config.js
- Check for unresolved promises
- Ensure async operations use `waitFor`

### Mock not working
- Verify `vi.clearAllMocks()` in `beforeEach`
- Check mock is defined before component render
- Ensure mock returns a Promise for async functions

### Element not found
- Use `screen.debug()` to see rendered output
- Check if element is rendered conditionally
- Try `findBy` queries for async elements

## Additional Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library Docs](https://testing-library.com/react)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
