# Makefile for Green Greeter Backend

.PHONY: help install test test-coverage lint format clean run dev docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install        Install dependencies"
	@echo "  test           Run tests"
	@echo "  test-coverage  Run tests with coverage report"
	@echo "  lint           Run linting (flake8)"
	@echo "  format         Format code (black)"
	@echo "  clean          Clean cache and build files"
	@echo "  run            Run the application"
	@echo "  dev            Run in development mode"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-run     Run Docker container"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install black flake8 mypy

# Run tests
test:
	pytest

# Run tests with coverage
test-coverage:
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Lint code
lint:
	flake8 app.py test_app.py
	mypy app.py

# Format code
format:
	black app.py test_app.py

# Clean cache files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Run application
run:
	uvicorn app:app --host 0.0.0.0 --port 8000

# Run in development mode
dev:
	uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Docker commands
docker-build:
	docker build -t green-greeter-backend .

docker-run:
	docker run -p 8000:8000 green-greeter-backend
