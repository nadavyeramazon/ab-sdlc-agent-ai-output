# Green-Themed Greeting Frontend

A beautiful green-themed web interface for greeting users based on their input.

## Features

- 🌿 **Green Theme**: Calming green color scheme throughout the UI
- 👋 **Personalized Greetings**: Get custom greetings based on your name
- ✨ **Smooth Animations**: Elegant transitions and animations
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- ⚡ **Real-time Validation**: Instant feedback on user input
- 🔄 **Error Handling**: Graceful error messages if backend is unavailable

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- The backend FastAPI service running (see backend/README.md)

### Running the Frontend

#### Option 1: Direct File Access

1. Simply open `index.html` in your web browser
2. Make sure the backend is running on `http://localhost:8000`

#### Option 2: Using a Local Server

For better CORS handling, use a local server:

```bash
# Using Python
python -m http.server 3000

# Using Node.js (if you have npx)
npx serve .

# Using PHP
php -S localhost:3000
```

Then open `http://localhost:3000` in your browser.

#### Option 3: Using Docker

If a Dockerfile is provided:

```bash
docker build -t greeting-frontend .
docker run -p 3000:80 greeting-frontend
```

## Configuration

If your backend is running on a different URL, update the `API_URL` in `app.js`:

```javascript
const API_URL = 'http://your-backend-url:port';
```

## Usage

1. Open the application in your browser
2. Enter your name in the input field
3. Click "Greet Me!" or press Enter
4. Enjoy your personalized green-themed greeting!

## File Structure

```
frontend/
├── index.html      # Main HTML structure
├── styles.css      # Green-themed styling
├── app.js          # JavaScript functionality
├── Dockerfile      # Docker configuration (optional)
├── nginx.conf      # Nginx configuration (optional)
└── README.md       # This file
```

## Color Palette

The application uses the following green color scheme:

- Primary Green: `#2d5f2e`
- Secondary Green: `#4a7c4e`
- Light Green: `#7cb87f`
- Very Light Green: `#a8d5aa`
- Pale Green: `#e8f5e9`
- Dark Green: `#1b3a1c`
- Accent Green: `#76c776`

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

## Troubleshooting

### "Unable to connect to the greeting service"

- Make sure the backend is running on the configured URL
- Check the browser console for detailed error messages
- Verify CORS is properly configured in the backend

### Styling Issues

- Clear your browser cache
- Ensure `styles.css` is in the same directory as `index.html`
- Check the browser console for CSS loading errors

## Contributing

Feel free to enhance the green theme or add new features!

## License

See the main repository LICENSE file.
