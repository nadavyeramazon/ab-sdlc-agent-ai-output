FROM nginx:alpine

COPY . /usr/share/nginx/html

# Custom nginx configuration for SPA
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
