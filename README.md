# Greeting User API - Full Stack Application

![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20Pipeline/badge.svg)

A full-stack application with a FastAPI backend and vanilla JavaScript frontend for greeting users in multiple languages with a beautiful green-themed UI.

## 🌟 Features

- **Multi-language Support**: Greet users in English, Spanish, French, and German
- **Beautiful Green UI**: Modern, responsive design with a green color theme
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Comprehensive Testing**: Extensive test coverage with pytest
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing
- **CORS Enabled**: Ready for frontend-backend integration
- **Type Safety**: Pydantic models for request/response validation
- **Health Checks**: Built-in health monitoring endpoint

## 📁 Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Backend dependencies
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Green-themed CSS styles
│   └── app.js              # Vanilla JavaScript logic
├── tests/
│   ├── __init__.py
│   ├── test_main.py        # Comprehensive test suite
│   └── requirements.txt    # Test dependencies
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Modern web browser

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Frontend Setup

1. **Open the frontend**:
   Simply open `frontend/index.html` in your web browser.

   Or use a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   Then visit: http://localhost:3000

2. **Update API URL** (if needed):
   Edit `frontend/app.js` and change `API_BASE_URL` if your backend runs on a different port.

## 🧪 Running Tests

1. **Install test dependencies**:
   ```bash
   pip install -r tests/requirements.txt
   ```

2. **Run all tests**:
   ```bash
   pytest tests/ -v
   ```

3. **Run tests with coverage**:
   ```bash
   pytest tests/ -v --cov=backend --cov-report=html
   ```

4. **View coverage report**:
   Open `htmlcov/index.html` in your browser

## 📡 API Endpoints

### GET `/`
Returns API information and available endpoints.

**Response**:
```json
{
  "message": "Greeting User API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

### GET `/health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "greeting-api"
}
```

### POST `/greet`
Greet a user with a personalized message.

**Request Body**:
```json
{
  "name": "Alice",
  "language": "en"
}
```

**Response**:
```json
{
  "message": "Hello, Alice! Welcome to our application!",
  "name": "Alice",
  "language": "en"
}
```

**Supported Languages**: `en` (English), `es` (Spanish), `fr` (French), `de` (German)

### GET `/greet/{name}`
Greet a user by name via GET request.

**Parameters**:
- `name` (path): User's name
- `language` (query, optional): Language code (default: "en")

**Example**: `/greet/Bob?language=es`

**Response**:
```json
{
  "message": "¡Hola, Bob! ¡Bienvenido a nuestra aplicación!",
  "name": "Bob",
  "language": "es"
}
```

## 🎨 Frontend Features

- **Green Theme**: Beautiful gradient design with green color scheme
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Real-time Validation**: Client-side input validation
- **API Status**: Live API health check indicator
- **Error Handling**: User-friendly error messages
- **Smooth Animations**: Slide-in effects and transitions
- **Language Selection**: Dropdown to choose greeting language

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to:
- Add more languages to `GREETINGS` dictionary
- Modify CORS settings
- Change logging configuration
- Customize validation rules

### Frontend Configuration

Edit `frontend/app.js` to:
- Change `API_BASE_URL` for different backend location
- Customize error messages
- Modify validation rules

## 🔐 Security

The application includes:
- Input validation and sanitization
- Pydantic models for type safety
- CORS configuration
- Length limits on inputs
- Error handling without exposing internals

**Note**: The current CORS configuration allows all origins (`*`). In production, specify exact origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    ...
)
```

## 📊 CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Testing**: Runs tests on Python 3.9, 3.10, and 3.11
2. **Linting**: Code quality checks with flake8 and black
3. **Security**: Security scanning with bandit and safety
4. **Integration**: End-to-end API testing
5. **Coverage**: Code coverage reporting

Workflow is triggered on:
- Push to `main`, `test-*`, or `feature/*` branches
- Pull requests to `main`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

See the LICENSE file for details.

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.9+ is installed: `python --version`
- Check if port 8000 is available: `lsof -i :8000`
- Verify all dependencies are installed: `pip list`

### Frontend can't connect to backend
- Ensure backend is running on http://localhost:8000
- Check browser console for CORS errors
- Verify `API_BASE_URL` in `app.js` is correct

### Tests failing
- Ensure test dependencies are installed
- Check Python version compatibility
- Review test output for specific errors

## 📧 Support

For issues and questions, please open an issue in the GitHub repository.

---

**Built with ❤️ using FastAPI and Vanilla JavaScript**
