# User Greeting Service

[![CI - User Greeting API Tests](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

A full-stack user greeting application with a green-themed UI, featuring a FastAPI backend and vanilla JavaScript frontend.

## 🌟 Features

- **FastAPI Backend**: RESTful API with comprehensive validation
- **Green-Themed UI**: Modern, responsive vanilla JavaScript frontend
- **Input Validation**: Client-side and server-side validation
- **Health Monitoring**: API health check endpoint with live status
- **Comprehensive Tests**: pytest test suite with 40+ test cases
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Backend dependencies
├── frontend/
│   ├── index.html          # HTML structure
│   ├── styles.css          # Green-themed styles
│   └── app.js              # JavaScript application logic
├── tests/
│   ├── test_main.py        # Comprehensive test suite
│   └── requirements.txt    # Test dependencies
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI workflow
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip
- Modern web browser

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Open `frontend/index.html` in your web browser, or
2. Serve with a local server:
```bash
cd frontend
python -m http.server 3000
```

Access the UI at `http://localhost:3000`

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt
pip install -r backend/requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

### Test Coverage

The test suite includes:
- ✅ Root endpoint tests
- ✅ Health check tests
- ✅ Greeting functionality tests
- ✅ Input validation tests
- ✅ Edge case handling
- ✅ CORS configuration tests
- ✅ Response structure validation

## 📚 API Documentation

### Endpoints

#### `GET /`
Returns API information and available endpoints.

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "greeting-api"
}
```

#### `POST /api/greet`
Greets a user with a personalized message.

**Request Body:**
```json
{
  "name": "Alice",
  "title": "Dr."  // optional
}
```

**Response:**
```json
{
  "message": "Hello, Dr. Alice! Welcome to our service. We're delighted to greet you today!",
  "name": "Alice",
  "success": true
}
```

**Validation Rules:**
- `name`: Required, 1-100 characters, letters/spaces/hyphens/apostrophes only
- `title`: Optional, max 50 characters, letters and periods only

### Interactive API Docs

Access the auto-generated API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🎨 Frontend Features

- **Green Theme**: Beautiful gradient design with green color scheme
- **Real-time Validation**: Input validation as you type
- **API Status Monitoring**: Live health check indicator
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during API calls

## 🔧 CI/CD Pipeline

The GitHub Actions workflow includes:

- **Multi-version Testing**: Python 3.9, 3.10, 3.11
- **Automated Tests**: Run on push and pull requests
- **Code Linting**: flake8, black, isort
- **Security Scanning**: bandit and safety checks
- **Coverage Reports**: Generated for Python 3.11

## 🛠️ Development

### Code Quality

```bash
# Format code
black backend/ tests/

# Sort imports
isort backend/ tests/

# Lint code
flake8 backend/ tests/

# Security scan
bandit -r backend/
```

### Adding New Features

1. Create a feature branch
2. Implement changes in `backend/` or `frontend/`
3. Add tests in `tests/`
4. Run test suite locally
5. Submit pull request

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code follows PEP 8 style guide
- New features include tests
- Documentation is updated

## 🐛 Troubleshooting

### Backend won't start
- Check Python version (3.9+)
- Verify all dependencies installed
- Ensure port 8000 is available

### Frontend can't connect to API
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Ensure API_BASE_URL in app.js is correct

### Tests failing
- Install test dependencies: `pip install -r tests/requirements.txt`
- Set PYTHONPATH: `export PYTHONPATH=$(pwd)`
- Check backend dependencies installed

## 📧 Support

For issues and questions, please open a GitHub issue.
