# Frontend Dockerfile for Green Theme Hello World Application
# Development build using Vite dev server for HMR and hot reload

FROM node:18-alpine

WORKDIR /app

# Install wget for healthcheck
RUN apk add --no-cache wget

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start Vite dev server
# --host 0.0.0.0 allows access from outside container
# --port 3000 ensures correct port
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]