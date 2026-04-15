import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  optimizeDeps: {
    entries: ["index.html"],
    include: [
      "react",
      "react-dom",
      "react/jsx-dev-runtime",
      "react/jsx-runtime",
      "axios",
      "lucide-react",
      "@tanstack/react-query",
      "sonner",
      "class-variance-authority",
      "clsx",
      "tailwind-merge",
      "next-themes",
    ],
  },
  server: {
    host: "localhost",
    port: 5173,
    strictPort: false,
    watch: {
      ignored: [
        "**/node_modules/**",
        "**/playwright-report/**",
        "**/dist/**",
        "**/test-results/**",
      ],
    },
  },
  resolve: {
    tsconfigPaths: true,
  },
  // @ts-expect-error - Vitest config
  test: {
    globals: true,
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"],
    setupFiles: ["./src/test/setup.ts"],
  },
});
