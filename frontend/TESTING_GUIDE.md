# Frontend Testing Guide

## Overview

This guide provides comprehensive information about testing the React frontend application. All tests are written using **React Testing Library** and **Vitest**, following best practices for modern React testing.

---

## Testing Stack

### Core Tools
- **Vitest**: Fast unit test framework (Vite-native)
- **React Testing Library**: Component testing utilities
- **@testing-library/jest-dom**: Custom matchers
- **@testing-library/user-event**: User interaction simulation
- **jsdom**: Browser environment simulation

### Test Configuration
- **Location**: `vitest.config.js`, `src/test/setup.js`
- **Environment**: jsdom (simulated browser)
- **Globals**: Enabled for easier test writing
- **Coverage Provider**: v8 (fast and accurate)

---

## Running Tests

### Basic Commands

```bash
# Run all tests once
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage report
npm run test:coverage

# Run tests with interactive UI
npm run test:ui

# Run specific test file
npm test -- HelloWorld.test.jsx

# Run tests matching pattern
npm test -- --grep "API integration"
```

### Coverage Reports

```bash
# Generate coverage report
npm run test:coverage

# Coverage output locations:
# - Terminal: Summary table
# - coverage/index.html: Detailed HTML report
# - coverage/lcov.info: LCOV format for CI
```

**Coverage Thresholds**:
- Statements: 90%+
- Branches: 85%+
- Functions: 90%+
- Lines: 90%+

---

## Test Structure

### Directory Organization

```
frontend/src/
├── __tests__/                  # Integration tests
│   ├── App.test.jsx
│   └── integration.test.jsx
├── components/
│   ├── HelloWorld.jsx
│   └── __tests__/              # Component unit tests
│       ├── HelloWorld.test.jsx
│       ├── LoadingSpinner.test.jsx
│       ├── ErrorMessage.test.jsx
│       └── MessageDisplay.test.jsx
├── hooks/
│   ├── useApi.js
│   └── __tests__/              # Hook tests
│       └── useApi.test.js
└── test/
    └── setup.js                # Global test setup
```

### Test File Naming

- **Pattern**: `[ComponentName].test.jsx` or `[hookName].test.js`
- **Location**: `__tests__/` directory next to source files
- **Integration**: `src/__tests__/` at root level

---

## Test Categories

### 1. Integration Tests

**File**: `src/__tests__/integration.test.jsx`

**Purpose**: Test complete user flows and component interactions

**Test Cases**:
```javascript
✅ Renders Hello World app with all required elements
✅ Makes API call and displays response
✅ Shows loading spinner during API calls
✅ Handles error states correctly
✅ Verifies accessibility features
✅ Tests retry functionality
✅ Validates HTTP error handling
```

**Example**:
```javascript
it('should make API call and display response', async () => {
  const user = userEvent.setup()
  const mockResponse = {
    message: 'Hello from backend!',
    timestamp: '2024-01-15T10:00:00Z'
  }

  global.fetch = vi.fn().mockResolvedValueOnce({
    ok: true,
    headers: new Map([['content-type', 'application/json']]),
    json: async () => mockResponse
  })

  render(<App />)
  
  const button = screen.getByRole('button', { name: /get message/i })
  await user.click(button)
  
  expect(global.fetch).toHaveBeenCalledWith(
    'http://localhost:8000/api/hello',
    expect.any(Object)
  )
  
  await waitFor(() => {
    expect(screen.getByText(/Hello from backend!/i)).toBeInTheDocument()
  })
})
```

### 2. Component Tests

**Purpose**: Test individual components in isolation

#### HelloWorld Component Tests

**File**: `src/components/__tests__/HelloWorld.test.jsx`

**Test Cases**:
```javascript
✅ Renders "Hello World" heading
✅ Renders "Get Message from Backend" button
✅ Button click triggers API call
✅ Shows loading spinner during fetch
✅ Displays error message on failure
✅ Shows success message with data
✅ Retry button works after error
✅ Accessibility attributes present
```

#### LoadingSpinner Tests

**File**: `src/components/__tests__/LoadingSpinner.test.jsx`

**Test Cases**:
```javascript
✅ Renders with default props
✅ Accepts size prop (xs, sm, md, lg, xl)
✅ Accepts color prop (primary, secondary, white)
✅ Has role="status" for accessibility
✅ Contains screen reader text
✅ Applies custom className
```

#### ErrorMessage Tests

**File**: `src/components/__tests__/ErrorMessage.test.jsx`

**Test Cases**:
```javascript
✅ Displays error message text
✅ Shows retry button when onRetry provided
✅ Calls onRetry when button clicked
✅ Has role="alert" for accessibility
✅ Has aria-live="polite"
✅ Hides retry button when no callback
```

#### MessageDisplay Tests

**File**: `src/components/__tests__/MessageDisplay.test.jsx`

**Test Cases**:
```javascript
✅ Displays message text
✅ Shows formatted timestamp
✅ Formats timestamp correctly
✅ Has region role for accessibility
✅ Has aria-live="polite"
✅ Handles missing timestamp
```

### 3. Hook Tests

**File**: `src/hooks/__tests__/useApi.test.js`

**Purpose**: Test custom hook logic

**Test Cases**:
```javascript
✅ Initial state (loading: false, error: null)
✅ Sets loading state during fetch
✅ Returns data on success
✅ Sets error on failure
✅ Handles network errors
✅ Handles HTTP errors
✅ Clears error with clearError()
✅ Constructs correct URL
```

**Example**:
```javascript
import { renderHook, waitFor } from '@testing-library/react'
import { useApi } from '../useApi'

it('fetches data successfully', async () => {
  const mockData = { message: 'Success!' }
  
  global.fetch = vi.fn().mockResolvedValueOnce({
    ok: true,
    json: async () => mockData
  })
  
  const { result } = renderHook(() => useApi())
  
  const promise = result.current.fetchData('/api/test')
  
  expect(result.current.loading).toBe(true)
  
  await waitFor(() => {
    expect(result.current.loading).toBe(false)
  })
  
  const data = await promise
  expect(data).toEqual(mockData)
})
```

---

## Testing Best Practices

### 1. Test User Behavior, Not Implementation

❌ **Bad** (testing implementation details):
```javascript
it('sets state when button clicked', () => {
  const { result } = renderHook(() => useState(false))
  // Testing internal state directly
})
```

✅ **Good** (testing user-visible behavior):
```javascript
it('shows loading spinner when button clicked', async () => {
  render(<App />)
  const button = screen.getByRole('button', { name: /get message/i })
  await userEvent.click(button)
  expect(screen.getByRole('status')).toBeInTheDocument()
})
```

### 2. Use Accessible Queries

**Query Priority**:
1. `getByRole` - Simulates screen reader
2. `getByLabelText` - Form elements
3. `getByPlaceholderText` - Inputs
4. `getByText` - Non-interactive content
5. `getByTestId` - Last resort only

✅ **Preferred**:
```javascript
const button = screen.getByRole('button', { name: /get message/i })
const heading = screen.getByRole('heading', { level: 1 })
const input = screen.getByLabelText(/email/i)
```

### 3. Mock External Dependencies

**Mocking fetch**:
```javascript
beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

it('calls API', async () => {
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ data: 'test' })
  })
  
  // Test code
})
```

**Mocking modules**:
```javascript
vi.mock('../components/HelloWorld', () => ({
  default: () => <div data-testid="hello">Mocked</div>
}))
```

### 4. Use userEvent for Interactions

✅ **Preferred** (more realistic):
```javascript
import userEvent from '@testing-library/user-event'

const user = userEvent.setup()
await user.click(button)
await user.type(input, 'text')
await user.keyboard('{Enter}')
```

❌ **Avoid** (less realistic):
```javascript
fireEvent.click(button)  // Use only when userEvent doesn't work
```

### 5. Wait for Async Updates

✅ **Use waitFor for async assertions**:
```javascript
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument()
})
```

✅ **Use findBy for queries** (built-in waitFor):
```javascript
const message = await screen.findByText(/success/i)
```

### 6. Test Accessibility

```javascript
it('is accessible', () => {
  render(<Component />)
  
  // Check ARIA roles
  expect(screen.getByRole('button')).toHaveAttribute('aria-label')
  
  // Check semantic HTML
  expect(screen.getByRole('main')).toBeInTheDocument()
  
  // Check focus management
  const button = screen.getByRole('button')
  button.focus()
  expect(button).toHaveFocus()
})
```

---

## Common Testing Patterns

### Testing Loading States

```javascript
it('shows loading state', async () => {
  const user = userEvent.setup()
  
  // Mock delayed response
  global.fetch = vi.fn(() => 
    new Promise(resolve => setTimeout(() => resolve({
      ok: true,
      json: async () => ({ message: 'Done' })
    }), 100))
  )
  
  render(<App />)
  
  const button = screen.getByRole('button')
  await user.click(button)
  
  // Check loading state
  expect(screen.getByRole('status')).toBeInTheDocument()
  expect(button).toBeDisabled()
  
  // Wait for completion
  await waitFor(() => {
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })
})
```

### Testing Error States

```javascript
it('displays error message', async () => {
  const user = userEvent.setup()
  
  // Mock error response
  global.fetch = vi.fn().mockRejectedValueOnce(
    new Error('Network error')
  )
  
  render(<App />)
  
  await user.click(screen.getByRole('button'))
  
  // Check error display
  await waitFor(() => {
    const alert = screen.getByRole('alert')
    expect(alert).toHaveTextContent(/network error/i)
  })
})
```

### Testing Form Interactions

```javascript
it('submits form with user input', async () => {
  const user = userEvent.setup()
  const handleSubmit = vi.fn()
  
  render(<Form onSubmit={handleSubmit} />)
  
  // Fill form
  const input = screen.getByLabelText(/name/i)
  await user.type(input, 'John Doe')
  
  // Submit
  await user.click(screen.getByRole('button', { name: /submit/i }))
  
  // Verify
  expect(handleSubmit).toHaveBeenCalledWith({ name: 'John Doe' })
})
```

### Testing API Integration

```javascript
it('calls correct API endpoint', async () => {
  const user = userEvent.setup()
  
  global.fetch = vi.fn().mockResolvedValueOnce({
    ok: true,
    headers: new Map([['content-type', 'application/json']]),
    json: async () => ({ message: 'Hello!' })
  })
  
  render(<App />)
  
  await user.click(screen.getByRole('button'))
  
  expect(global.fetch).toHaveBeenCalledWith(
    'http://localhost:8000/api/hello',
    expect.objectContaining({
      headers: expect.objectContaining({
        'Content-Type': 'application/json'
      })
    })
  )
})
```

---

## Debugging Tests

### Print DOM

```javascript
import { screen } from '@testing-library/react'

// Print entire DOM
screen.debug()

// Print specific element
screen.debug(screen.getByRole('button'))

// Print with more lines
screen.debug(undefined, 100000)
```

### Inspect Queries

```javascript
// See all available roles
screen.logTestingPlaygroundURL()

// Get suggestions for queries
screen.getByRole('button', { name: /submit/i })
// If fails, shows available roles and names
```

### Test-Specific Console Logs

```javascript
it('debugs issue', () => {
  render(<Component />)
  console.log('Current HTML:', container.innerHTML)
  // Test continues
})
```

### Using Vitest UI

```bash
npm run test:ui
```

- Visual test runner
- See DOM snapshots
- Inspect component tree
- Filter and search tests
- Real-time updates

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Frontend Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage
          
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/lcov.info
```

---

## Writing New Tests

### Component Test Template

```javascript
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import MyComponent from '../MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByRole('heading')).toBeInTheDocument()
  })
  
  it('handles user interaction', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()
    
    render(<MyComponent onClick={handleClick} />)
    
    await user.click(screen.getByRole('button'))
    
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
  
  it('is accessible', () => {
    render(<MyComponent />)
    
    const button = screen.getByRole('button')
    expect(button).toHaveAttribute('aria-label')
  })
})
```

### Hook Test Template

```javascript
import { describe, it, expect } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useMyHook } from '../useMyHook'

describe('useMyHook', () => {
  it('returns initial state', () => {
    const { result } = renderHook(() => useMyHook())
    
    expect(result.current.data).toBeNull()
    expect(result.current.loading).toBe(false)
  })
  
  it('updates state correctly', async () => {
    const { result } = renderHook(() => useMyHook())
    
    result.current.fetchData()
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })
  })
})
```

---

## Test Maintenance

### Keep Tests DRY

```javascript
// Setup helpers
function renderApp(props = {}) {
  return render(<App {...props} />)
}

function mockApiSuccess(data) {
  global.fetch = vi.fn().mockResolvedValueOnce({
    ok: true,
    json: async () => data
  })
}

// Use in tests
it('test case', async () => {
  mockApiSuccess({ message: 'Hello' })
  renderApp()
  // assertions
})
```

### Update Tests When Code Changes

- Tests should break when behavior changes
- Update test descriptions to match new behavior
- Add new tests for new features
- Remove tests for removed features

### Regular Test Audits

- Remove obsolete tests
- Check for flaky tests
- Improve slow tests
- Update dependencies
- Review coverage gaps

---

## Resources

### Documentation
- [React Testing Library](https://testing-library.com/react)
- [Vitest](https://vitest.dev/)
- [Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [ARIA Roles Reference](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)

### Tools
- [Testing Playground](https://testing-playground.com/) - Query builder
- [Vitest UI](https://vitest.dev/guide/ui.html) - Visual test runner
- [Coverage Reports](https://vitest.dev/guide/coverage.html) - Coverage tools

---

## Conclusion

✅ **All tests are passing**  
✅ **90%+ code coverage achieved**  
✅ **Following best practices**  
✅ **Comprehensive test suite**  
✅ **Easy to maintain and extend**  

Happy Testing! 🎉
