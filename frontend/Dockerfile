# Frontend Dockerfile for Yellow Theme Hello World application
# Base image: Node 18 Alpine for smaller image size
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port 3000 for Vite dev server
EXPOSE 3000

# Run Vite development server
# --host flag allows access from outside the container
CMD ["npm", "run", "dev", "--", "--host"]
