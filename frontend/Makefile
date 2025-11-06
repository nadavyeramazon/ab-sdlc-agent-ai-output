# Makefile for Green Greeter Frontend

.PHONY: help install test test-coverage lint format clean serve docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install        Install dependencies"
	@echo "  test           Run tests"
	@echo "  test-coverage  Run tests with coverage report"
	@echo "  test-watch     Run tests in watch mode"
	@echo "  clean          Clean cache and build files"
	@echo "  serve          Serve files locally"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-run     Run Docker container"

# Install dependencies
install:
	npm install

# Run tests
test:
	npm test

# Run tests with coverage
test-coverage:
	npm run test:coverage

# Run tests in watch mode
test-watch:
	npm run test:watch

# Clean cache files
clean:
	rm -rf node_modules
	rm -rf coverage
	rm -f package-lock.json

# Serve files locally
serve:
	python -m http.server 3000

# Docker commands
docker-build:
	docker build -t green-greeter-frontend .

docker-run:
	docker run -p 8080:8080 green-greeter-frontend
