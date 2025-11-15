import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for React frontend
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Allow access from Docker network
    port: 3000,
    strictPort: true,
    watch: {
      usePolling: true,  // Required for Docker volume watching
    },
  },
})
