#!/bin/bash
set -e

echo "Starting Hello World FastAPI server..."

# Install dependencies if they don't exist
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --reload