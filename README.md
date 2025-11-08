# 🌿 Green Greeting App

A full-stack web application with a beautiful green theme that provides personalized greetings in multiple languages.

## 🚀 Features

- **Green-themed Frontend**: Beautiful, responsive UI built with vanilla JavaScript
- **FastAPI Backend**: High-performance Python backend with RESTful API
- **Multi-language Support**: Greetings in English, Spanish, French, German, and Italian
- **Dockerized**: Full docker-compose setup for easy deployment
- **Comprehensive Tests**: Extensive test suite with pytest
- **CI/CD Pipeline**: Automated testing with GitHub Actions

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Features**:
  - RESTful API endpoints
  - CORS enabled for frontend integration
  - Health check endpoints
  - Request/response validation with Pydantic

### Frontend
- **Technology**: Vanilla JavaScript (no frameworks)
- **Styling**: Custom CSS with green theme
- **Features**:
  - Responsive design
  - Smooth animations
  - Form validation
  - Error handling

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Modern web browser

## 🛠️ Installation & Setup

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
Simply open `frontend/index.html` in your browser or serve it with a local server:
```bash
cd frontend
python -m http.server 80
```

## 🧪 Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run with coverage:
```bash
pytest tests/ --cov=backend --cov-report=term-missing
```

### Run specific test class:
```bash
pytest tests/test_main.py::TestGreetingEndpoint -v
```

## 📡 API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the API.

### Root
```
GET /
```
Returns API information and version.

### Greet User
```
POST /api/greet
Content-Type: application/json

{
  "name": "Alice",
  "language": "en"  // Optional, defaults to "en"
}
```
Returns a personalized greeting.

### Get Supported Languages
```
GET /api/languages
```
Returns list of supported language codes.

## 🌍 Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)

## 🔧 Configuration

### Backend Configuration
- Port: 8000 (configurable in docker-compose.yml)
- CORS: Enabled for all origins (configure in backend/main.py for production)

### Frontend Configuration
- Port: 80 (configurable in docker-compose.yml)
- API URL: http://localhost:8000 (configure in frontend/app.js)

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend Docker configuration
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green theme styles
│   ├── app.js              # JavaScript application logic
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend Docker configuration
├── tests/
│   ├── __init__.py
│   └── test_main.py        # Comprehensive test suite
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── docker-compose.yml      # Docker Compose configuration
├── pytest.ini              # Pytest configuration
└── README.md              # This file
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that:

1. **Tests**: Runs pytest test suite
2. **Linting**: Checks code quality with flake8, black, and isort
3. **Docker Build**: Validates Docker images build successfully
4. **Integration Tests**: Tests the full application stack
5. **Coverage**: Generates and uploads code coverage reports

## 🎨 Design Highlights

- **Green Theme**: Eco-friendly color palette with shades of green
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **Animations**: Smooth fade-in, slide-in, and hover effects
- **Accessibility**: Proper semantic HTML and ARIA labels

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

## 👥 Authors

- Initial implementation by AI Agent for SDLC automation

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Nginx for serving the frontend
- Docker for containerization
- GitHub Actions for CI/CD

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ and 🌿**