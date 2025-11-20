import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite configuration with React plugin and backend proxy
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  server: {
    // Development server port
    port: 3000,
    
    // Enable host to make server accessible from outside container (for Docker)
    host: true,
    
    // Proxy API requests to backend
    // This allows frontend to make requests to /api/* which will be forwarded to the backend
    proxy: {
      '/api': {
        // In Docker Compose environment, backend service is named 'backend'
        // For local development without Docker, change to 'http://localhost:8000'
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        // Optional: rewrite path if needed (currently passes /api as-is)
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  
  // Build configuration
  build: {
    outDir: 'dist',
    sourcemap: true,
    // Optimize build output
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom']
        }
      }
    }
  },
  
  // Preview server configuration (for testing production build locally)
  preview: {
    port: 3000,
    host: true
  }
});
