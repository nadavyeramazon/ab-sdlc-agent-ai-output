# Multi-stage build for optimized production image

# Stage 1: Build React application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build application
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy runtime configuration template
COPY public/config.js /usr/share/nginx/html/config.js

# Copy entrypoint script
COPY env-to-config.sh /docker-entrypoint.d/env-to-config.sh
RUN chmod +x /docker-entrypoint.d/env-to-config.sh

# Expose port 3000
EXPOSE 3000

# Start nginx (entrypoint script will run automatically)
CMD ["nginx", "-g", "daemon off;"]
