# Multi-stage Docker build for React + Vite frontend
# Stage 1: Build the application
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files for dependency installation
# This layer is cached unless package.json or package-lock.json changes
COPY package.json ./

# Clean npm cache to prevent integrity errors
RUN npm cache clean --force

# Install dependencies
# Use npm install (not npm ci) to generate fresh package-lock.json if missing
# Use --production=false to ensure devDependencies are installed (needed for build)
RUN npm install --production=false

# Copy all source files
COPY . .

# Build the application
# Output will be in /app/dist directory
RUN npm run build

# Stage 2: Production stage with Nginx
FROM nginx:alpine

# Copy built assets from build stage to Nginx html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration for SPA routing
# This ensures that all routes are handled by index.html (for client-side routing)
RUN echo 'server {\n\
    listen 80;\n\
    server_name localhost;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    \n\
    # Serve static files directly\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
    \n\
    # Cache static assets\n\
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {\n\
        expires 1y;\n\
        add_header Cache-Control "public, immutable";\n\
    }\n\
}' > /etc/nginx/conf.d/default.conf

# Expose port 80 (Nginx default)
# Note: You can map this to port 3000 externally using Docker run -p 3000:80
EXPOSE 80

# Start Nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]
