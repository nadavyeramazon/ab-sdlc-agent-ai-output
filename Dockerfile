# Use slim Python image for minimal size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY setup.py .
COPY src ./src

# Install dependencies
RUN pip install --no-cache-dir -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run as non-root user for security
RUN useradd -m appuser
USER appuser

# Command to run the application
CMD ["python", "-m", "src.main"]