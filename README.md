# AB SDL-C Agent AI Backend

Simple Flask API implementation for the AB SDL-C Agent AI Backend.

## Endpoints

- `GET /` - Main endpoint with service information
- `GET /health` - Health check endpoint
- `POST /echo` - Echo endpoint that returns posted data

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. The API will be available at `http://localhost:5000`

## Usage

### Health Check
```
GET /health
```

### Echo Endpoint
```
POST /echo
Content-Type: application/json

{
    "key": "value"
}
```

Expected response:
```json
{
    "received": {
        "key": "value"
    },
    "message": "Data received successfully"
}
```