# Frontend Dockerfile for Vite + React Application
# Base image: Node 18 Alpine variant for smaller image size
FROM node:18-alpine

# Set working directory inside the container
WORKDIR /app

# Copy package files first to leverage Docker cache
# This layer will only rebuild if package files change
COPY package.json package-lock.json* ./

# Install dependencies
# npm ci is preferred for CI/CD but we use npm install for flexibility
# with optional package-lock.json
RUN npm install

# Copy the frontend application source code
COPY . .

# Expose port 3000 for the Vite dev server
EXPOSE 3000

# Command to run Vite dev server
# --host 0.0.0.0: Listen on all network interfaces (required for Docker)
# This enables hot reload and makes the server accessible from outside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]