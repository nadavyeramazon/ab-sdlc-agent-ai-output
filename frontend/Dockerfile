# Use Node 18 Alpine for smaller image size
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first for better caching
# Only rebuild node_modules if package files change
COPY package*.json ./

# Install dependencies
# Using --legacy-peer-deps to avoid conflicts
RUN npm install

# Copy application source code
COPY . .

# Expose port 3000 for Vite dev server
EXPOSE 3000

# Run Vite development server
# --host 0.0.0.0 makes server accessible from outside container
CMD ["npm", "run", "dev"]
