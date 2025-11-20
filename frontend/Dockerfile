FROM node:18-alpine

WORKDIR /app

# Copy package.json first for layer caching
COPY package.json .

# CRITICAL: Use 'npm install' NOT 'npm ci'
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Start development server with host binding
CMD ["npm", "run", "dev", "--", "--host"]
