#!/bin/sh
# Script to inject environment variables into config.js at runtime

# Get API_URL from environment or use default
API_URL=${API_URL:-http://localhost:8000}

# Create config.js with the actual API URL
cat > /usr/share/nginx/html/config.js << EOF
// Runtime configuration for frontend
// Generated at container startup
window.API_CONFIG = {
  apiUrl: '${API_URL}'
};
EOF

echo "Generated config.js with API_URL: ${API_URL}"

# Start nginx
exec nginx -g 'daemon off;'
