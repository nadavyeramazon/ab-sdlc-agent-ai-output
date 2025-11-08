# FastAPI Hello World

This is a simple Hello World API using FastAPI.

## Installation

1. Clone the repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the API

To run the API, use the following command:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Endpoints

- `/`: Returns a JSON response with a "Hello, World!" message.

## Testing

Open your browser and navigate to `http://localhost:8000`. You should see a JSON response:

```json
{"message": "Hello, World!"}
```
