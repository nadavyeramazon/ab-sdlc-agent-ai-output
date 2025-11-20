# Backend Dockerfile for FastAPI Application
# Base image: Python 3.11 slim variant for smaller image size
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
# This layer will only rebuild if requirements.txt changes
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: Don't cache pip packages to reduce image size
# --upgrade: Ensure pip is up to date
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the application with hot reload for development
# --host 0.0.0.0: Listen on all network interfaces (required for Docker)
# --port 8000: Run on port 8000
# --reload: Enable auto-reload on code changes (development mode)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]