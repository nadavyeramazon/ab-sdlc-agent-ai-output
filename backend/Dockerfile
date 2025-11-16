# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first for better Docker layer caching
# This allows pip install to be cached if requirements don't change
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run uvicorn with reload enabled for development
# --host 0.0.0.0 makes the server accessible from outside the container
# --reload enables auto-reload when code changes (development mode)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
