import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Bind to all network interfaces (required for Docker)
    port: 3000,
    strictPort: true, // Fail if port is already in use
    watch: {
      usePolling: true, // Required for hot reload in Docker on some systems
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
  },
})
