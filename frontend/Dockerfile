# Use Node 18 Alpine for smaller image size
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
# Note: package-lock.json is generated during npm install if it doesn't exist
RUN npm install

# Copy application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Run Vite dev server with explicit host binding for Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
