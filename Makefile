# Makefile for Green Greeting Application

.PHONY: help build up down restart logs clean backend-logs frontend-logs test

# Default target
help:
	@echo "Green Greeting Application - Available Commands:"
	@echo ""
	@echo "  make build          - Build Docker containers"
	@echo "  make up             - Start the application"
	@echo "  make down           - Stop the application"
	@echo "  make restart        - Restart the application"
	@echo "  make logs           - View logs from all containers"
	@echo "  make backend-logs   - View backend logs only"
	@echo "  make frontend-logs  - View frontend logs only"
	@echo "  make clean          - Remove containers, volumes, and images"
	@echo "  make test           - Test backend health"
	@echo ""

# Build Docker containers
build:
	@echo "Building Docker containers..."
	docker-compose build

# Start the application
up:
	@echo "Starting the application..."
	docker-compose up -d
	@echo "Application started!"
	@echo "Frontend: http://localhost"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

# Start with logs
up-logs:
	@echo "Starting the application with logs..."
	docker-compose up

# Stop the application
down:
	@echo "Stopping the application..."
	docker-compose down

# Restart the application
restart: down up

# View logs
logs:
	docker-compose logs -f

# View backend logs only
backend-logs:
	docker-compose logs -f backend

# View frontend logs only
frontend-logs:
	docker-compose logs -f frontend

# Clean up everything
clean:
	@echo "Cleaning up containers, volumes, and images..."
	docker-compose down -v --rmi all
	@echo "Cleanup complete!"

# Test backend health
test:
	@echo "Testing backend health..."
	@curl -s http://localhost:8000/health | jq || echo "Backend is not responding"

# Development mode - rebuild and start
dev: build up-logs
