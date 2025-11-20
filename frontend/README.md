# Fullstack Hello World - Frontend

A minimal React application with a green theme that integrates with a backend API.

## Features

- 🟢 Green-themed UI (#2ecc71, #27ae60)
- ⚡ Built with Vite for fast development
- 🎯 Simple functional components with React hooks
- 🔄 Backend API integration with loading states
- 🎨 Clean, centered responsive layout
- ❌ Proper error handling

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **CSS** - Simple styling (no framework dependencies)

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
├── vite.config.js      # Vite configuration
├── .gitignore          # Git ignore rules
└── src/
    ├── main.jsx        # React entry point
    ├── App.jsx         # Main App component
    └── App.css         # Application styles
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

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript support required

## License

MIT
