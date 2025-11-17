import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for React frontend
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Listen on all addresses (needed for Docker)
    port: 3000,
    strictPort: true, // Fail if port is already in use
    watch: {
      usePolling: true, // Enable polling for Docker volume mounts
    },
    // Proxy API requests to backend during development
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://backend:8000',
        changeOrigin: true,
      },
      '/health': {
        target: process.env.VITE_API_URL || 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})
