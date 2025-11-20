# Green Hello World Frontend

A React-based frontend application with a beautiful green theme that integrates with a backend API.

## Features

- ✅ React 18+ with modern hooks (useState)
- ✅ Vite 5+ for fast development and building
- ✅ Beautiful green-themed UI with gradient background
- ✅ Backend API integration (fetch from http://localhost:8000/api/hello)
- ✅ Loading states with animated spinner
- ✅ Error handling and display
- ✅ Responsive design (mobile and desktop)
- ✅ Smooth animations and transitions
- ✅ Accessible UI with semantic HTML
- ✅ Hot Module Replacement (HMR) enabled

## Tech Stack

- **React** 18.2.0 - UI library
- **Vite** 5.0.8 - Build tool and dev server
- **CSS3** - Styling with animations

## Getting Started

### Prerequisites

- Node.js (v18 or higher recommended)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application

Start the development server:
```bash
npm run dev
```

The application will be available at: **http://localhost:3000**

### Building for Production

Build the application:
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
├── index.html          # HTML entry point
├── package.json        # Dependencies and scripts
├── vite.config.js      # Vite configuration
└── src/
    ├── main.jsx        # React app entry point
    ├── App.jsx         # Main App component
    └── App.css         # Styles with green theme
```

## Usage

1. The app displays a "Hello World" heading
2. Click the "Get Message from Backend" button
3. The app fetches data from http://localhost:8000/api/hello
4. Loading state is shown during the fetch
5. Success message displays the backend response
6. Error message displays if the fetch fails

## Design Features

### Color Theme
- Primary Green: `#2ecc71`
- Dark Green: `#27ae60`
- White: `#ffffff` (on green backgrounds)

### Responsive Breakpoints
- Desktop: Default styles
- Tablet: 768px and below
- Mobile: 480px and below

### Accessibility
- Semantic HTML elements
- Focus-visible states for keyboard navigation
- Reduced motion support for accessibility preferences
- High contrast text and backgrounds

## Backend Integration

The frontend expects a backend API running on:
- **URL**: http://localhost:8000/api/hello
- **Method**: GET
- **Response**: JSON with a `message` field

Example backend response:
```json
{
  "message": "Hello from the backend!"
}
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
