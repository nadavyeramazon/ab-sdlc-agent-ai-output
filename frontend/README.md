# Simple Frontend - Item Manager

A simple, green-themed frontend interface built with vanilla JavaScript that connects to a FastAPI backend to manage items.

## Features

- 🌱 **Green-themed UI** - Clean, modern design with various shades of green
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🔄 **Real-time Connection Status** - Shows backend connectivity status
- ➕ **Add Items** - Create new items with name and description
- ✏️ **Edit Items** - Update existing items using a modal dialog
- 🗑️ **Delete Items** - Remove items with confirmation
- 📊 **Item Counter** - Shows total number of items
- 🔄 **Refresh Functionality** - Manual refresh of items list
- 🚀 **Fast & Lightweight** - Pure JavaScript, no frameworks required

## Setup

1. **Start the Backend First**:
   ```bash
   cd ../backend
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open the Frontend**:
   - Simply open `index.html` in your web browser
   - Or serve it using a local server:
   ```bash
   # Using Python
   python -m http.server 3000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:3000
   ```

## File Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # Green-themed CSS styling
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## API Integration

The frontend communicates with the FastAPI backend using these endpoints:

- `GET /health` - Check backend status
- `GET /api/items` - Retrieve all items
- `POST /api/items` - Create new item
- `PUT /api/items/{id}` - Update existing item
- `DELETE /api/items/{id}` - Delete item

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Color Scheme

The green theme uses these CSS custom properties:
- `--primary-green: #2e7d32` - Main brand color
- `--light-green: #4caf50` - Accent color
- `--dark-green: #1b5e20` - Dark accents
- `--accent-green: #81c784` - Light accents
- `--background-green: #e8f5e8` - Subtle backgrounds

## Development Notes

- No build process required - pure HTML, CSS, and JavaScript
- Uses modern JavaScript features (ES6+)
- Responsive design with CSS Grid and Flexbox
- Error handling and user feedback included
- Accessible design with proper ARIA labels

## Customization

To customize the appearance:
1. Modify CSS custom properties in `styles.css`
2. Update the color scheme in the `:root` selector
3. Adjust component styling as needed

To extend functionality:
1. Add new methods to the `ItemManager` class in `script.js`
2. Update the HTML structure in `index.html` if needed
3. Style new components in `styles.css`
