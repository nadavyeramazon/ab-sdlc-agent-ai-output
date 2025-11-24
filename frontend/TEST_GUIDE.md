# Frontend Testing Guide

## Overview

This project uses **Vitest**, **React Testing Library**, and **fast-check** for comprehensive frontend testing. The test suite combines traditional integration tests with property-based testing to ensure correctness.

## Testing Philosophy

The test suite uses a dual testing approach:

- **Integration Tests**: Verify complete user workflows (create, edit, delete tasks)
- **Property-Based Tests**: Verify universal properties using fast-check with 100+ random examples

## Test Coverage

The test suite includes:
- ✅ **Task Creation Tests** - Form submission, validation, and list updates
- ✅ **Task Display Tests** - Rendering tasks, empty states, completion styling
- ✅ **Task Editing Tests** - Inline editing, validation, cancel functionality
- ✅ **Task Deletion Tests** - Delete operations and UI updates
- ✅ **Completion Toggle Tests** - Status changes and visual feedback
- ✅ **Loading State Tests** - Loading indicators for all async operations
- ✅ **Error Handling Tests** - Network errors, validation errors, 404 handling
- ✅ **Property-Based Tests** - Task ordering consistency with random data

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

Tests are organized in the `src/__tests__/` directory following React best practices:

```
frontend/
├── src/
│   ├── __tests__/
│   │   └── App.test.jsx          # Main application tests
│   ├── test/
│   │   └── setup.js              # Test configuration
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── vite.config.js                 # Vitest configuration
└── package.json
```

### File: `src/__tests__/App.test.jsx`

The test suite is organized into the following sections:

#### 1. Task Creation Flow
- ✅ Renders task creation form
- ✅ Creates task with valid title and description
- ✅ Validates empty title rejection
- ✅ Clears form after successful creation
- ✅ Updates task list with new task
- ✅ Displays validation errors from backend

#### 2. Task Display
- ✅ Fetches and displays all tasks on mount
- ✅ Shows empty state when no tasks exist
- ✅ Displays task title, description, and status
- ✅ Shows loading indicator during fetch
- ✅ Handles fetch errors gracefully

#### 3. Task Editing Flow
- ✅ Shows edit form when edit button clicked
- ✅ Pre-fills form with current task data
- ✅ Updates task with valid changes
- ✅ Validates empty title in edit mode
- ✅ Cancels editing and discards changes
- ✅ Updates UI after successful edit

#### 4. Task Completion Toggle
- ✅ Toggles completion status on click
- ✅ Updates visual styling (strikethrough)
- ✅ Persists changes to backend
- ✅ Handles toggle errors

#### 5. Task Deletion
- ✅ Deletes task on button click
- ✅ Removes task from UI immediately
- ✅ Handles 404 errors (already deleted)
- ✅ Shows error message on failure

#### 6. Loading States
- ✅ Shows loading indicator for all operations
- ✅ Disables buttons during loading
- ✅ Clears loading state after completion

#### 7. Error Handling
- ✅ Network errors show user-friendly messages
- ✅ Validation errors (422) display field-specific messages
- ✅ Not found errors (404) handled appropriately
- ✅ Server errors (500) show generic messages

#### 8. Property-Based Tests
- ✅ **Property 10: Task ordering consistency** - Tasks always ordered by creation date (newest first)
  - Runs 100+ iterations with randomly generated task lists
  - Validates: Requirements 2.4

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

## Property-Based Testing with fast-check

### What is Property-Based Testing?

Property-based testing verifies that certain properties hold true across all possible inputs, rather than testing specific examples. fast-check automatically generates test cases to find edge cases.

### How It Works

1. Define a property that should always be true
2. fast-check generates random test data
3. The property is tested with 100+ different inputs
4. If a failure is found, fast-check minimizes the failing example
5. The minimal counterexample is displayed in the test output

### Example Property Test

```javascript
import fc from 'fast-check';

test('Property 10: Task ordering consistency', () => {
  fc.assert(
    fc.property(
      fc.array(taskArbitrary, { minLength: 2, maxLength: 10 }),
      (tasks) => {
        // Verify tasks are ordered by creation date (newest first)
        for (let i = 0; i < tasks.length - 1; i++) {
          const current = new Date(tasks[i].created_at);
          const next = new Date(tasks[i + 1].created_at);
          expect(current >= next).toBe(true);
        }
      }
    ),
    { numRuns: 100 }
  );
});
```

### Benefits

- ✅ Catches edge cases developers don't think of
- ✅ Tests hundreds of inputs automatically
- ✅ Provides mathematical confidence in correctness
- ✅ Complements traditional integration tests

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
await user.type(input, 'Task title');
```

### Async Testing

Tests use `waitFor` for async operations:

```javascript
await waitFor(() => {
  expect(screen.getByText('Task created')).toBeInTheDocument();
});
```

### Querying Elements

Tests use accessible queries from React Testing Library:

- `getByRole()` - Preferred for accessibility
- `getByText()` - For text content
- `getByLabelText()` - For form inputs
- `queryBy...()` - When element may not exist
- `getBy...()` - When element must exist

## Common Test Patterns

### Testing Task Creation

```javascript
global.fetch.mockResolvedValueOnce({
  ok: true,
  status: 201,
  json: async () => ({
    id: '123',
    title: 'New Task',
    description: 'Description',
    completed: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }),
});

const user = userEvent.setup();
await user.type(screen.getByLabelText(/title/i), 'New Task');
await user.click(screen.getByRole('button', { name: /add task/i }));
```

### Testing Task List Fetch

```javascript
global.fetch.mockResolvedValueOnce({
  ok: true,
  json: async () => ({
    tasks: [
      { id: '1', title: 'Task 1', completed: false, ... },
      { id: '2', title: 'Task 2', completed: true, ... }
    ]
  }),
});
```

### Testing Validation Error (422)

```javascript
global.fetch.mockResolvedValueOnce({
  ok: false,
  status: 422,
  json: async () => ({
    detail: [
      { loc: ['body', 'title'], msg: 'Title cannot be empty' }
    ]
  }),
});
```

### Testing Not Found Error (404)

```javascript
global.fetch.mockResolvedValueOnce({
  ok: false,
  status: 404,
  json: async () => ({ detail: 'Task not found' }),
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

### Property Test Failures

When a property test fails:

1. **Review the counterexample**: fast-check shows the failing input
2. **Check if it's a bug**: Does the code violate the property?
3. **Check if it's a test issue**: Is the property correctly specified?
4. **Simplify**: fast-check automatically minimizes the failing example

Example failure output:
```
Property failed after 42 tests
Counterexample: [
  { id: '1', created_at: '2024-01-15T10:00:00Z' },
  { id: '2', created_at: '2024-01-15T11:00:00Z' }
]
```

### fast-check Not Found

If you see errors about fast-check:
```bash
npm install --save-dev fast-check
```

### Environment Variables Not Working in Tests

Vitest loads environment variables automatically. If needed, you can set them in `vite.config.js`:

```javascript
test: {
  env: {
    VITE_API_URL: 'http://test-api:8000'
  }
}
```

### Async Tests Timing Out

Increase the timeout for slow operations:
```javascript
test('slow operation', async () => {
  // test code
}, 10000); // 10 second timeout
```

## Test Maintenance

When adding new features:

1. **Update Requirements**: Add acceptance criteria
2. **Define Properties**: Add correctness properties to design doc
3. **Write Integration Tests**: Test complete user workflows
4. **Write Property Tests**: Test universal properties with random data
5. **Verify Coverage**: Ensure all user interactions are tested

### Adding Property-Based Tests

When adding a new property test:

1. Reference the design document property in a comment:
   ```javascript
   // Feature: task-manager-app, Property 10: Task ordering consistency
   // Validates: Requirements 2.4
   ```

2. Use appropriate fast-check arbitraries:
   ```javascript
   import fc from 'fast-check';
   
   const taskArbitrary = fc.record({
     id: fc.uuid(),
     title: fc.string({ minLength: 1, maxLength: 200 }),
     created_at: fc.date().map(d => d.toISOString())
   });
   ```

3. Configure for 100+ examples:
   ```javascript
   fc.assert(
     fc.property(taskArbitrary, (task) => {
       // Test implementation
     }),
     { numRuns: 100 }
   );
   ```

## Additional Resources

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [fast-check Documentation](https://fast-check.dev/)
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)

---

**Test Framework**: Vitest + React Testing Library + fast-check  
**Property Tests**: 1 correctness property with 100+ examples  
**Integration Tests**: Complete user workflow coverage  
**Last Updated**: 2024-01-23
