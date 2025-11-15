#!/bin/sh
# Script to inject environment variables into config.js at runtime
# This script is executed by nginx's docker-entrypoint system before nginx starts

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

# DO NOT exec nginx here - the nginx entrypoint system will handle starting nginx
# This script runs as part of /docker-entrypoint.d/ and should exit cleanly
