import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// Served at https://<user>.github.io/gridlet/ in production, root in dev.
export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/gridlet/' : '/',
  plugins: [svelte()],
  server: {
    port: 5173,
    fs: {
      // Allow importing the wasm-pack output that lives under src/engine/pkg.
      allow: ['..'],
    },
  },
}))
