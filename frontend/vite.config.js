import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for React application
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    // Enable Hot Module Replacement
    hmr: {
      clientPort: 3000,
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})