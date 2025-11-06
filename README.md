# Simple Full-Stack Application

A complete full-stack application with a FastAPI backend and a green-themed JavaScript frontend.

## 🌱 Features

### Backend (FastAPI)
- RESTful API with full CRUD operations
- Automatic API documentation (Swagger UI)
- CORS enabled for frontend integration
- In-memory data storage for simplicity
- Health check endpoint
- Comprehensive error handling

### Frontend (JavaScript)
- Modern, responsive green-themed UI
- Real-time backend connection status
- Complete item management (Create, Read, Update, Delete)
- Modal-based editing interface
- Toast notifications for user feedback
- Mobile-friendly responsive design
- Pure vanilla JavaScript (no frameworks)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser

### 1. Start the Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 2. Open the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Option 1: Open directly in browser
# Simply open index.html in your web browser

# Option 2: Serve with Python
python -m http.server 3000

# Option 3: Serve with Node.js
npx serve . -p 3000
```

The frontend will be available at http://localhost:3000

## 📱 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Backend documentation
│
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Green-themed CSS
│   ├── script.js           # JavaScript functionality
│   └── README.md           # Frontend documentation
│
├── README.md               # This file
└── LICENSE                 # License information
```

## 🌍 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/api/items` | Get all items |
| POST | `/api/items` | Create new item |
| GET | `/api/items/{id}` | Get item by ID |
| PUT | `/api/items/{id}` | Update item by ID |
| DELETE | `/api/items/{id}` | Delete item by ID |

## 🎨 UI Screenshots

The frontend features a modern green theme with:
- Header with gradient background
- Real-time connection status indicator
- Add item form with validation
- Items list with edit/delete actions
- Modal dialog for editing items
- Responsive design for mobile devices
- Toast notifications for user feedback

## 🗺️ Color Palette

- **Primary Green**: #2e7d32
- **Light Green**: #4caf50
- **Dark Green**: #1b5e20
- **Accent Green**: #81c784
- **Background Green**: #e8f5e8

## 🚀 Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

The frontend uses vanilla JavaScript, so no build process is required. Simply edit the files and refresh the browser.

### API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

## 📝 Features in Detail

### Backend Features
- ✅ RESTful API design
- ✅ Automatic request/response validation
- ✅ CORS middleware for cross-origin requests
- ✅ Comprehensive error handling
- ✅ Interactive API documentation
- ✅ Health check endpoint
- ✅ Pydantic models for data validation

### Frontend Features
- ✅ Modern CSS with custom properties
- ✅ Responsive grid layout
- ✅ Real-time connection monitoring
- ✅ Form validation and error handling
- ✅ Modal dialogs for editing
- ✅ Toast notifications
- ✅ Keyboard shortcuts (ESC to close modals)
- ✅ Loading states and empty state handling
- ✅ Accessibility considerations

## 🔧 Troubleshooting

### Backend Issues
1. **Port already in use**: Change the port in the uvicorn command
2. **Module not found**: Ensure you're in the backend directory and dependencies are installed
3. **CORS errors**: The backend includes CORS middleware, but ensure you're using the correct URLs

### Frontend Issues
1. **Can't connect to backend**: Ensure the backend is running on port 8000
2. **CORS errors**: Use a local server instead of opening the HTML file directly
3. **JavaScript errors**: Check the browser console for detailed error messages

## 📦 Dependencies

### Backend
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0

### Frontend
- Pure vanilla JavaScript (ES6+)
- No external dependencies
- Modern browser required

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

---

**Note**: This is a demonstration project with in-memory storage. For production use, consider adding a proper database and authentication system.
