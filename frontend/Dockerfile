FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json .

# CRITICAL: Use 'npm install' NOT 'npm ci'
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]
