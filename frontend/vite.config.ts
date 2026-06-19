import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  // Serve the legacy HTML pages from the Elasticrew-main folder
  // so that /hiring-queue.html, /assessments.html, etc. resolve correctly
  // when navigating from the React SPA sidebar.
  publicDir: '../Elasticrew-main',
})
