# Frontend Test Suite

Comprehensive test coverage for the React frontend application using Vitest and React Testing Library.

## Test Structure

```
frontend/src/tests/
├── setup.js           # Test environment setup and global mocks
├── App.test.jsx       # Component tests for main App
└── README.md          # This file
```

## Running Tests

### Run all tests once
```bash
npm test
```

### Run tests in watch mode (for development)
```bash
npm run test:watch
```

### Generate coverage report
```bash
npm run test:coverage
```

Coverage reports will be generated in the `coverage/` directory.

## Test Coverage

### App Component Tests

The test suite covers:

#### 1. Initial Rendering (6 tests)
- Main heading display
- Fetch button presence
- No initial message/loading/error states
- Button enabled state

#### 2. User Interactions (2 tests)
- Button click triggers fetch
- Button disabled during loading

#### 3. Loading State (2 tests)
- Loading indicator display during fetch
- Previous messages hidden during loading

#### 4. Success Scenarios (3 tests)
- Display backend message on success
- Message structure validation
- Multiple successful fetches

#### 5. Error Handling (7 tests)
- Network errors
- HTTP error codes (404, 500)
- Error without message property
- Error clearing on new fetch
- Previous message clearing on error
- Error display structure

#### 6. State Management (3 tests)
- No simultaneous loading and message
- No simultaneous loading and error
- No simultaneous message and error

#### 7. Edge Cases (4 tests)
- Empty message handling
- JSON parsing errors
- Rapid consecutive clicks

#### 8. Accessibility (3 tests)
- Proper button role
- Proper heading role
- Button disabled attribute during loading

**Total: 30+ comprehensive tests**

## Testing Best Practices Used

### 1. User-Centric Testing
- Tests focus on user-facing behavior
- Use semantic queries (getByRole, getByText)
- Avoid testing implementation details

### 2. Proper Async Handling
- All async operations use `waitFor`
- Tests wait for UI updates before assertions
- Controlled promises for testing loading states

### 3. Isolated Tests
- Each test is independent
- Mocks reset between tests
- No shared state between tests

### 4. Comprehensive Coverage
- Happy path scenarios
- Error scenarios
- Edge cases
- State transitions

### 5. Accessibility Testing
- ARIA roles verified
- Disabled states tested
- Semantic HTML validation

## Mock Strategy

### Fetch API Mocking
The global `fetch` function is mocked using Vitest's `vi.fn()`. Each test sets up its own mock responses:

```javascript
// Success response
global.fetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({ message: 'Success!' })
});

// Error response
global.fetch.mockRejectedValueOnce(new Error('Network error'));

// HTTP error
global.fetch.mockResolvedValueOnce({
  ok: false,
  status: 404
});
```

## Test Configuration

### vitest.config.js
- Environment: jsdom (for DOM testing)
- Globals: true (for describe, it, expect)
- CSS: true (CSS imports don't break tests)
- Coverage provider: v8
- Setup file: src/tests/setup.js

### Test Setup (setup.js)
- Imports @testing-library/jest-dom matchers
- Cleans up after each test
- Mocks global fetch
- Resets all mocks between tests

## Writing New Tests

When adding new components or features, follow these patterns:

### 1. Component Test Template
```javascript
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import YourComponent from '../YourComponent';

describe('YourComponent', () => {
  beforeEach(() => {
    // Setup code
  });

  it('should render correctly', () => {
    render(<YourComponent />);
    expect(screen.getByRole('...')).toBeInTheDocument();
  });

  it('should handle user interaction', async () => {
    const user = userEvent.setup();
    render(<YourComponent />);
    
    await user.click(screen.getByRole('button'));
    
    expect(screen.getByText('...')).toBeInTheDocument();
  });
});
```

### 2. Testing Async Operations
```javascript
import { waitFor } from '@testing-library/react';

it('should handle async operation', async () => {
  // Trigger async operation
  await user.click(button);
  
  // Wait for async update
  await waitFor(() => {
    expect(screen.getByText('...')).toBeInTheDocument();
  });
});
```

### 3. Testing Loading States
```javascript
it('should show loading state', async () => {
  let resolvePromise;
  const promise = new Promise((resolve) => {
    resolvePromise = resolve;
  });
  
  global.fetch.mockReturnValueOnce(promise);
  
  // Trigger action
  await user.click(button);
  
  // Assert loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  // Resolve and assert final state
  resolvePromise({ ok: true, json: async () => ({}) });
  await waitFor(() => {
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });
});
```

## Troubleshooting

### Tests failing due to timing issues
- Use `waitFor` for async operations
- Increase timeout if needed: `waitFor(() => {...}, { timeout: 3000 })`

### "Not wrapped in act(...)" warnings
- Ensure all state updates are within `waitFor`
- Use `userEvent` instead of `fireEvent`

### Mock not working
- Check mock is set up before component renders
- Ensure `vi.resetAllMocks()` in beforeEach
- Use `mockResolvedValueOnce` for single use

### Coverage not 100%
- Check uncovered lines in coverage report
- Add tests for edge cases
- Test error boundaries

## CI/CD Integration

Tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: npm install
  working-directory: ./frontend

- name: Run tests
  run: npm test
  working-directory: ./frontend

- name: Generate coverage
  run: npm run test:coverage
  working-directory: ./frontend
```

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Jest-DOM Matchers](https://github.com/testing-library/jest-dom)
- [User Event](https://testing-library.com/docs/user-event/intro/)
