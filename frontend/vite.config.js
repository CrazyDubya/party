import { sveltekit } from "@sveltejs/kit/vite";
import { svelteTesting } from "@testing-library/svelte/vite";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [sveltekit(), svelteTesting()],
  test: {
    include: ["tests/**/*.{test,spec}.{js,ts}"],
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      reporter: ["text", "json", "html"],
      thresholds: {
        global: {
          branches: 90,
          functions: 90,
          lines: 90,
          statements: 90,
        },
      },
    },
  },
});
