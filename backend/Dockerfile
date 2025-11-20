# Use Python 3.11 slim image as base for smaller image size
FROM python:3.11-slim

# Set metadata labels for maintainability
LABEL maintainer="Hello World Team"
LABEL description="FastAPI backend for Hello World fullstack application"
LABEL version="1.0.0"

# Set working directory in container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies (if needed in future)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better Docker layer caching
# Dependencies are installed only if requirements.txt changes
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Create a non-root user for security best practices
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Health check to ensure container is healthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the application with uvicorn
# --host 0.0.0.0: Listen on all network interfaces
# --port 8000: Run on port 8000
# --reload: Auto-reload on code changes (for development)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
