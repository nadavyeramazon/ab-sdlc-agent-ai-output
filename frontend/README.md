# Yellow Theme Hello World - Frontend

React 18 frontend for the Yellow Theme Hello World fullstack application.

## Tech Stack

- **React 18.2** - UI library
- **Vite 5** - Build tool and dev server
- **Vanilla CSS** - Styling (no frameworks)
- **Native Fetch API** - HTTP requests

## Features

- ✅ Yellow theme (#f4d03f, #f9e79f) design
- ✅ Button-triggered API calls (no auto-fetch)
- ✅ Loading, success, and error states
- ✅ Responsive design
- ✅ Clean, minimal UI
- ✅ Docker-ready with HMR support

## Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

## Installation

**IMPORTANT**: Use `npm install` (NOT `npm ci`) to avoid generating package-lock.json:

```bash
cd frontend
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The app will be available at http://localhost:3000

### Development with Docker

The Vite configuration is optimized for Docker with:
- Host binding to `0.0.0.0`
- File watching with polling enabled
- Strict port mode on 3000

## Environment Variables

Create a `.env` file in the frontend directory to override the default API URL:

```env
VITE_API_URL=http://localhost:8000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The frontend connects to the backend API:

- **Endpoint**: `GET /api/hello`
- **Response**: 
  ```json
  {
    "message": "Hello World from Backend!",
    "timestamp": "2025-11-21T11:09:03.123456Z"
  }
  ```

## Component Structure

```
src/
├── main.jsx       # App entry point
├── App.jsx        # Main component with state and API logic
├── App.css        # Component-specific styles (yellow theme)
└── index.css      # Global CSS reset and base styles
```

## Features Checklist

✅ Page displays "Hello World" as h1 heading  
✅ Background uses yellow theme (#f4d03f or #f9e79f)  
✅ Content is centered on the page  
✅ Page accessible via http://localhost:3000  
✅ Button labeled "Get Message from Backend" is visible  
✅ Clicking button triggers API call  
✅ API response displayed below button  
✅ Loading text "Loading..." appears during fetch  
✅ Error message "Failed to load message" shown if request fails  
✅ Uses React hooks (useState)

## Testing

Manual testing checklist:

- [ ] Page loads at http://localhost:3000
- [ ] Yellow theme is applied correctly
- [ ] "Hello World" heading is visible
- [ ] Button is visible and clickable
- [ ] Clicking button shows "Loading..." state
- [ ] Backend message and timestamp are displayed
- [ ] Timestamp is formatted in local time
- [ ] Error handling works when backend is down
- [ ] Button is disabled during loading
- [ ] Responsive design works on mobile

## Building for Production

Build the app:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

The build output will be in the `dist/` directory.

## Docker

The frontend includes a Dockerfile for containerized deployment. See the root docker-compose.yml for the complete setup.

## Code Style

The project uses ESLint with:
- React 18 recommended rules
- React Hooks rules
- React Refresh plugin for HMR

Run linter:

```bash
npm run lint
```

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES2020+ features
- No legacy browser support

## License

MIT
