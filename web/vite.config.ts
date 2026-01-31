import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
	plugins: [sveltekit(), tailwindcss()],
	server: {
		fs: {
			// Allow serving files from one level up (the monorepo root)
			// This lets Vite reach the hoisted node_modules
			allow: ['..']
		}
	}
});