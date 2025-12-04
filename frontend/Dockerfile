# ============================================
# Base Stage - Common foundation
# ============================================
FROM node:24-alpine AS base

# Set working directory
WORKDIR /app

# Copy package files for dependency installation
COPY package.json package-lock.json ./

# ============================================
# Build Stage - Create production bundle
# ============================================
FROM base AS build

# Install all dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Run production build
RUN npm run build

# ============================================
# Development Target - Hot-reload dev server
# ============================================
FROM base AS development

# Install all dependencies (including devDependencies)
RUN npm install

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 3000

# Start Vite dev server with hot-reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]

# ============================================
# Production Target - Nginx serving static files
# ============================================
FROM nginx:alpine AS production

# Copy built static files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
