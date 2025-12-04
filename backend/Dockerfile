# Multi-stage Dockerfile for Python 3.13 backend

# ============================================
# Base stage - common foundation for all targets
# ============================================
FROM python:3.13-slim AS base

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Development target - includes all dev tools
# ============================================
FROM base AS development

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install all dependencies (production + development)
RUN pip install --no-cache-dir -r requirements-dev.txt

# Expose port 8000
EXPOSE 8000

# Run as root in development for easier debugging and file permissions with volume mounts
# Source code will be mounted as volume for hot-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Production target - minimal and secure
# ============================================
FROM base AS production

# Copy only production requirements
COPY requirements.txt ./

# Install only production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 8000
EXPOSE 8000

# Remove pip to minimize attack surface (optional but recommended)
# Note: This is done after all installations
USER root
RUN pip uninstall -y pip setuptools wheel && \
    rm -rf /root/.cache /tmp/*
USER appuser

# Run uvicorn without reload for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
