# Makefile for Green Hello World Backend

.PHONY: help install dev test test-cov lint format run docker-build docker-run clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  dev         Install development dependencies"
	@echo "  test        Run tests"
	@echo "  test-cov    Run tests with coverage report"
	@echo "  lint        Run code linting"
	@echo "  format      Format code"
	@echo "  run         Run the development server"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run  Run Docker container"
	@echo "  clean       Clean up generated files"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev: install
	pip install black flake8 mypy

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=. --cov-report=term-missing --cov-report=html

# Run linting
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Format code
format:
	black . --line-length 100

# Run development server
run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info

# Build Docker image
docker-build:
	docker build -t green-hello-world-backend .

# Run Docker container
docker-run:
	docker run -p 8000:8000 green-hello-world-backend

# Clean up
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete