import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}'],
		coverage: {
			reporter: ['text', 'json', 'html'],
			thresholds: {
				global: {
					branches: 90,
					functions: 90,
					lines: 90,
					statements: 90
				}
			}
		}
	}
});