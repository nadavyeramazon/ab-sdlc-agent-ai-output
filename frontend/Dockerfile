# Use Node.js 18 Alpine for lightweight image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json first for better caching
COPY package.json .

# Install dependencies using npm install (NOT npm ci)
RUN npm install

# Copy all frontend code
COPY . .

# Expose port 3000
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
