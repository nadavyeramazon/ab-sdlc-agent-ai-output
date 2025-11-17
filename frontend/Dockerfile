# Frontend Dockerfile for React application with Vite
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Run Vite dev server
CMD ["npm", "run", "dev"]
