# FastAPI Backend Dockerfile
# Uses Python 3.11 slim image for optimal size and performance

# Base image - Python 3.11 slim variant (smaller footprint)
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="Backend Team"
LABEL description="FastAPI Backend Service"

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B)
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (equivalent to python -u)
ENV PYTHONUNBUFFERED=1

# Copy requirements file first for better Docker layer caching
# This layer will only rebuild if requirements.txt changes
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: Don't cache pip packages, reduces image size
# --upgrade: Upgrade pip to latest version for better dependency resolution
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
# This layer rebuilds whenever main.py changes
COPY main.py .

# Expose port 8000 for the FastAPI application
# This is the port uvicorn will listen on
EXPOSE 8000

# Health check to ensure container is running properly
# Checks the /health endpoint every 30 seconds
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application with uvicorn
# --host 0.0.0.0: Listen on all network interfaces
# --port 8000: Listen on port 8000
# --reload: Enable auto-reload during development (disable in production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
