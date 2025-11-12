# Green Theme Hello World - Frontend

A modern, responsive React application with a beautiful green theme and backend API integration.

## Features

- ✅ **React 18+** with functional components and hooks
- ✅ **Vite** for lightning-fast development and optimized builds
- ✅ **Green Theme** (#2ecc71, #27ae60, #1e8449) with smooth animations
- ✅ **Backend Integration** with loading and error states
- ✅ **Fully Responsive** design for all screen sizes
- ✅ **Accessibility Compliant** with ARIA labels and keyboard navigation
- ✅ **Comprehensive Testing** with React Testing Library (80%+ coverage)
- ✅ **Docker Ready** with multi-stage builds and nginx

## Tech Stack

- **React** 18.2.0
- **Vite** 5.0.8
- **React Testing Library** 14.1.2
- **Vitest** 1.0.4 for testing
- **Docker** with nginx for production

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend server running on port 8000 (or configure via VITE_API_URL)

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server (runs on http://localhost:3000)
npm run dev
```

The development server includes:
- Hot Module Replacement (HMR)
- Proxy to backend API at `/api`
- Fast refresh for instant feedback

### Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### Building for Production

```bash
# Create optimized production build
npm run build

# Preview production build locally
npm run preview
```

### Docker Deployment

```bash
# Build Docker image
docker build -t green-theme-frontend .

# Run container
docker run -p 80:80 green-theme-frontend
```

The Docker image uses:
- Multi-stage build for minimal size
- nginx for serving static files
- Automatic proxy to backend service
- Health checks for container orchestration

## Environment Variables

Create a `.env` file (see `.env.example`):

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── App.css              # Green theme styling
│   ├── main.jsx             # React entry point
│   ├── index.css            # Global styles
│   ├── setupTests.js        # Test configuration
│   └── __tests__/
│       └── App.test.jsx     # Component tests
├── index.html               # HTML entry point
├── package.json             # Dependencies and scripts
├── vite.config.js           # Vite configuration
├── Dockerfile               # Docker multi-stage build
├── nginx.conf               # nginx server configuration
└── README.md                # This file
```

## Component Details

### App Component

The main `App` component features:

1. **State Management**
   - `message`: Stores backend response
   - `loading`: Tracks API call status
   - `error`: Handles error messages

2. **API Integration**
   - Fetches data from `GET /api/hello`
   - Handles loading states
   - Displays error messages gracefully

3. **UI Elements**
   - "Hello World" heading
   - Action button with loading spinner
   - Success/error message boxes with icons
   - Feature list
   - Footer

## Styling

### Color Palette

- **Primary**: `#2ecc71` - Bright green
- **Secondary**: `#27ae60` - Medium green
- **Accent**: `#1e8449` - Dark green
- **Background**: Linear gradient of all three colors

### Responsive Breakpoints

- **Mobile**: < 480px
- **Tablet**: 480px - 768px
- **Desktop**: > 768px

### Animations

- Fade in/out transitions
- Smooth hover effects
- Loading spinner
- Reduced motion support for accessibility

## Testing Strategy

Tests cover:

1. **Initial Rendering** - All UI elements render correctly
2. **Button Interaction** - Click events and loading states
3. **Successful API Calls** - Backend integration and message display
4. **Failed API Calls** - Error handling and display
5. **Accessibility** - ARIA labels and keyboard navigation
6. **Multiple API Calls** - State management across requests

### Test Coverage Goals

- **Lines**: 80%+
- **Functions**: 80%+
- **Branches**: 80%+
- **Statements**: 80%+

## Accessibility Features

- Semantic HTML elements
- ARIA labels and live regions
- Keyboard navigation support
- Focus indicators
- Screen reader friendly
- Reduced motion support
- High contrast colors

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Optimizations

- Code splitting with React.lazy
- Vendor chunk separation
- Gzip compression
- Static asset caching
- Minimal bundle size

## API Integration

The frontend expects the backend to provide:

### GET /api/hello

**Response (200 OK)**:
```json
{
  "message": "Hello from the backend!"
}
```

**Error Handling**:
- Network errors: Display user-friendly message
- HTTP errors: Display status code
- Missing data: Display "No message received"

## Development Tips

1. **Hot Module Replacement**: Changes reflect instantly without page reload
2. **React DevTools**: Use browser extension for component inspection
3. **Vite Inspector**: Press `Option/Alt + Shift + Click` to open component source
4. **Test Watch Mode**: Keep tests running during development

## Troubleshooting

### Port Already in Use

```bash
# Change port in vite.config.js or use environment variable
PORT=3001 npm run dev
```

### API Connection Issues

1. Ensure backend is running on port 8000
2. Check VITE_API_URL environment variable
3. Verify CORS settings on backend
4. Check browser console for network errors

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Contributing

When contributing, ensure:

1. All tests pass: `npm test`
2. Code coverage meets 80% threshold
3. Linting passes (if configured)
4. Accessibility standards maintained
5. Responsive design preserved

## License

See LICENSE file in repository root.

## Support

For issues or questions, please open an issue in the GitHub repository.
