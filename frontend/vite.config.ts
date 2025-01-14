import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';

export default defineConfig({
    base: "/static/vue/",
    build: {
        outDir: "../api/static/vue",
        emptyOutDir: true,
    },
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            }
        }
    }
});