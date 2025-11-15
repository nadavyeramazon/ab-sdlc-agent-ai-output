# Development Dockerfile for React frontend with Vite
# Provides hot module reload (HMR) for development

FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy application source
COPY . .

# Expose port 3000
EXPOSE 3000

# Start Vite dev server with HMR
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
