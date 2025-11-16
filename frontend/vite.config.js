import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for React development
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Listen on all network interfaces (required for Docker)
    port: 3000,
    watch: {
      usePolling: true, // Enable polling for file changes (needed for Docker on some systems)
    },
    hmr: {
      host: 'localhost', // Hot Module Replacement host
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})
