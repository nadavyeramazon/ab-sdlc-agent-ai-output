# AB SDLC Agent AI Backend

A FastAPI-based Hello World application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn src.main:app --reload
```

## API Endpoints

- `GET /`: Hello World endpoint
- `GET /health`: Health check endpoint

## Testing

Run tests using pytest:
```bash
pytest
```