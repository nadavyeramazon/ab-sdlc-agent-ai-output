FROM node:18-alpine

WORKDIR /app

# Copy package.json
COPY package.json .

# CRITICAL: Use 'npm install' NOT 'npm ci'
RUN npm install

# Copy all frontend code
COPY . .

# Expose port
EXPOSE 3000

# Start development server with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
