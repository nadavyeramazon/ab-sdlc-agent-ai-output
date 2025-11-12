# Green Hello World Frontend

A React 18 frontend application built with Vite, featuring a green theme and backend integration.

## Features

- 🌱 **Green Theme**: Beautiful green color palette (#2ecc71, #27ae60, #1e8449)
- ⚡ **React 18 + Vite**: Fast development with Hot Module Replacement (HMR)
- 📱 **Responsive Design**: Mobile-first approach with responsive layouts
- ♿ **Accessibility**: WCAG compliant with semantic HTML and proper ARIA labels
- 🔄 **API Integration**: Connects to FastAPI backend at localhost:8000
- 📦 **Component Architecture**: Modular, reusable React components
- 🧪 **Testing**: Comprehensive tests with React Testing Library and Vitest
- 🎨 **Modern CSS**: CSS custom properties, animations, and responsive utilities

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend running on http://localhost:8000

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at http://localhost:3000

## Available Scripts

- `npm run dev` - Start development server with HMR
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run test:ui` - Run tests with UI
- `npm run test:coverage` - Run tests with coverage report
- `npm run lint` - Lint code with ESLint

## Project Structure

```
src/
├── components/          # React components
│   ├── HelloWorld.jsx   # Main application component
│   ├── LoadingSpinner.jsx
│   ├── ErrorMessage.jsx
│   ├── MessageDisplay.jsx
│   └── *.css           # Component-specific styles
├── hooks/              # Custom React hooks
│   └── useApi.js       # API integration hook
├── test/               # Test configuration
│   └── setup.js        # Test setup and utilities
├── App.jsx             # Root component
├── App.css             # Global styles and CSS variables
└── main.jsx            # Application entry point
```

## Components

### HelloWorld
Main application component featuring:
- Animated "Hello World" heading with waving emoji
- Interactive "Get Message from Backend" button
- Loading states and error handling
- Responsive design

### LoadingSpinner
Reusable loading spinner with:
- Multiple size variants (xs, sm, md, lg, xl)
- Color themes (primary, secondary, white)
- Accessibility support

### ErrorMessage
Error display component with:
- Clear error messaging
- Retry functionality
- ARIA live regions for screen readers

### MessageDisplay
Success message component with:
- Animated entrance effects
- Green theme styling
- Accessible content structure

## Custom Hooks

### useApi
API integration hook providing:
- Loading state management
- Error handling with user-friendly messages
- Automatic JSON/text response parsing
- Connection error detection

## Styling

### CSS Custom Properties
The application uses CSS custom properties for:
- Color palette (green theme)
- Spacing scale
- Typography settings
- Shadow definitions
- Border radius values

### Responsive Design
- Mobile-first approach
- Breakpoints: 480px, 768px
- Fluid typography with `clamp()`
- Flexible layouts with Flexbox

### Accessibility Features
- Semantic HTML structure
- ARIA labels and live regions
- Focus management
- High contrast mode support
- Reduced motion preferences
- Screen reader optimizations

## API Integration

The frontend connects to the FastAPI backend:
- **Base URL**: `http://localhost:8000`
- **Endpoint**: `/api/hello` (GET request)
- **Error Handling**: Network errors, HTTP errors, JSON parsing errors
- **Loading States**: Visual feedback during API calls

## Testing

Testing setup includes:
- **Vitest**: Fast unit test runner
- **React Testing Library**: Component testing utilities
- **jsdom**: Browser environment simulation
- **@testing-library/jest-dom**: Extended matchers

Test files should be placed alongside components with `.test.jsx` extension.

## Docker Support

The application includes Docker configuration:
- Multi-stage build for production optimization
- Nginx serving static files
- Port 3000 exposure for development
- Health checks and container orchestration

## Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- ES2020+ features
- CSS custom properties
- CSS Grid and Flexbox

## Performance

- Vite for fast builds and HMR
- Code splitting and lazy loading ready
- Optimized CSS with custom properties
- Minimal bundle size with tree shaking
- Production build optimization

## Contributing

1. Follow the existing code style and structure
2. Add tests for new components
3. Ensure accessibility compliance
4. Test on multiple screen sizes
5. Verify color contrast ratios
6. Run linting and tests before commits

## License

MIT License - see LICENSE file for details