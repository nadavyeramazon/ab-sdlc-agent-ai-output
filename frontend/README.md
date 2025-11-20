# Fullstack Hello World - Frontend

A minimal React application with a green theme that integrates with a backend API.

## Features

- 🟢 Green-themed UI (#2ecc71, #27ae60)
- ⚡ Built with Vite for fast development
- 🎯 Simple functional components with React hooks
- 🔄 Backend API integration with loading states
- 🎨 Clean, centered responsive layout
- ❌ Proper error handling
- ✅ Comprehensive test coverage with Vitest

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **CSS** - Simple styling (no framework dependencies)
- **Vitest** - Testing framework
- **React Testing Library** - Component testing utilities

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm

### Installation

```bash
# Install dependencies (using npm install, not npm ci)
npm install
```

**Note:** Following demo mode guidelines, we use `npm install` instead of `npm ci` to avoid generating large package-lock.json files.

### Development

```bash
# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Testing

```bash
# Run tests once
npm test

# Run tests in watch mode (for development)
npm run test:watch

# Generate test coverage report
npm run test:coverage
```

For detailed testing documentation, see [Test Documentation](./src/tests/README.md).

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── index.html          # HTML entry point
├── package.json        # Dependencies and scripts
├── vite.config.js      # Vite configuration (dev server)
├── vitest.config.js    # Vitest configuration (testing)
├── .gitignore          # Git ignore rules
└── src/
    ├── main.jsx        # React entry point
    ├── App.jsx         # Main App component
    ├── App.css         # Application styles
    └── tests/
        ├── setup.js           # Test environment setup
        ├── App.test.jsx       # Unit tests for App component
        ├── integration.test.jsx  # Integration tests
        └── README.md          # Test documentation
```

## Component Overview

### App.jsx

Main application component featuring:
- **State Management**: `useState` hooks for message, loading, and error states
- **API Integration**: Fetch function to communicate with backend at `http://localhost:8000/api/hello`
- **UI Elements**: 
  - Large "Hello World" heading (48px)
  - "Get Message from Backend" button
  - Loading indicator
  - Message display area
  - Error display area

### App.css

Green-themed styling with:
- Primary green background: `#2ecc71`
- Secondary green for buttons: `#27ae60`
- Flexbox-based centering (vertical and horizontal)
- Responsive design with media queries
- Smooth animations and transitions
- Clean, minimal aesthetic

## API Integration

The frontend expects a backend API running at `http://localhost:8000/api/hello` that returns JSON in the format:

```json
{
  "message": "Your message here"
}
```

## Testing

### Test Coverage

The frontend includes comprehensive test coverage:

- **40+ tests** covering unit and integration scenarios
- **100% component coverage** for the App component
- Tests for all user interactions, state transitions, and edge cases

### Test Categories

1. **Unit Tests** (`App.test.jsx`)
   - Component rendering
   - User interactions
   - API integration
   - Loading states
   - Error handling
   - Accessibility

2. **Integration Tests** (`integration.test.jsx`)
   - Complete user workflows
   - Success/error flows
   - Error recovery
   - Sequential operations
   - State transitions

### Running Tests

```bash
# Run all tests once (for CI/CD)
npm test

# Watch mode for development
npm run test:watch

# Coverage report
npm run test:coverage
```

### Test Reports

After running `npm run test:coverage`, view the coverage report:
- Terminal: Summary statistics
- HTML Report: Open `coverage/index.html` in a browser

## Development Guidelines

### Simplicity First
- Use functional components with hooks (no class components)
- Keep components small and focused
- Use simple CSS (no Tailwind or styled-components)
- Minimal dependencies

### State Management
- Use React's built-in `useState` for local state
- Keep state as local as possible
- Avoid complex state management libraries

### Styling
- Simple CSS with clear class names
- Flexbox for layout
- Responsive design principles
- Green color theme throughout

### Testing
- Write tests for all new components
- Test user-facing behavior, not implementation details
- Use React Testing Library best practices
- Maintain high test coverage

## CI/CD Integration

Tests are designed to run in CI/CD pipelines. Example workflow:

```yaml
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

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript support required
- jsdom environment for testing

## Troubleshooting

### Tests failing
- Ensure dependencies are installed: `npm install`
- Check that Node.js version is 16 or higher
- Clear cache: `rm -rf node_modules && npm install`

### Development server issues
- Check port 3000 is not in use
- Ensure backend is running on port 8000
- Check browser console for errors

### Coverage not generating
- Ensure @vitest/coverage-v8 is installed
- Check vitest.config.js configuration
- Run with verbose flag: `npm run test:coverage -- --reporter=verbose`

## License

MIT
