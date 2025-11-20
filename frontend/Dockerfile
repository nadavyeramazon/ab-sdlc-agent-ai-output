# Use Node.js 18 Alpine for smaller image size
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files for dependency installation
# This layer is cached unless package files change
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
# Separate from dependency installation for better layer caching
COPY . .

# Expose port 3000 for Vite dev server
EXPOSE 3000

# Start Vite development server with host flag
# --host flag allows external connections (required for Docker)
CMD ["npm", "run", "dev", "--", "--host"]

# Docker build and run instructions:
# Build: docker build -t hello-world-frontend .
# Run: docker run -p 3000:3000 -v $(pwd):/app -v /app/node_modules hello-world-frontend
#
# Volume mounts explanation:
# -v $(pwd):/app - Mounts current directory for hot reloading
# -v /app/node_modules - Prevents overwriting node_modules in container
#
# Recommended .dockerignore entries:
# node_modules
# dist
# .git
# .env
# npm-debug.log
