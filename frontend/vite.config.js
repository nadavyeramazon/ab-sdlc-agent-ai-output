import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 3000,
    watch: {
      usePolling: true,
    },
  },
  // Define environment variable prefix (default is VITE_)
  envPrefix: 'VITE_',
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
    // Make environment variables available in tests
    env: {
      VITE_API_URL: process.env.VITE_API_URL || 'http://localhost:8000/api'
    }
  },
})
