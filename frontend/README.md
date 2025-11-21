# Frontend - Hello World Application

React-based frontend application built with Vite.

## Features

- ⚛️ React 18 with functional components and hooks
- ⚡ Vite for fast development and builds
- 🎨 Simple CSS styling
- 🔌 Backend API integration
- ✅ Comprehensive test coverage with Vitest

## Prerequisites

- Node.js 16+ 
- npm

## Installation

```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Testing

The frontend includes comprehensive test coverage using Vitest and React Testing Library.

### Run Tests

```bash
# Run all tests once
npm test

# Run tests in watch mode (for development)
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

### Test Coverage

The test suite includes:

- **Component Rendering Tests**: Verifies UI elements render correctly
- **User Interaction Tests**: Tests button clicks and user events
- **State Management Tests**: Validates React hooks and state updates
- **API Integration Tests**: Mocks and tests backend API calls
- **Error Handling Tests**: Ensures proper error states and messages
- **Accessibility Tests**: Validates semantic HTML and ARIA attributes
- **Loading State Tests**: Tests loading indicators and disabled states

All core functionality in `App.jsx` is covered by the test suite in `App.test.jsx`.

## Build

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx           # Main application component
│   ├── App.css           # Application styles
│   ├── App.test.jsx      # Comprehensive test suite
│   ├── setupTests.js     # Test configuration
│   └── main.jsx          # Application entry point
├── index.html
├── package.json
├── vite.config.js        # Vite configuration
└── vitest.config.js      # Test configuration
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000/api/hello`.

Make sure the backend server is running before using the application.

## Technologies Used

- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Vitest**: Testing framework
- **React Testing Library**: Component testing utilities
- **jsdom**: Browser environment for tests
