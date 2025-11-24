# Use Node.js 18 Alpine for minimal size
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json
COPY package.json .

# CRITICAL: Use 'npm install' NOT 'npm ci'
RUN npm install

# Copy all frontend code
COPY . .

# Expose port 3000
EXPOSE 3000

# Start development server with explicit host and port
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
