# Frontend Dockerfile - nginx to serve static files
FROM nginx:alpine

# Copy frontend files to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# nginx will start automatically
CMD ["nginx", "-g", "daemon off;"]