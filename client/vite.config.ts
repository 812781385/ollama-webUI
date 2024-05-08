/// <reference types="vitest" />

import path from 'path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import ElementPlus from 'unplugin-element-plus/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import vueJsx from '@vitejs/plugin-vue-jsx'
import { configDefaults } from 'vitest/config'

export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    // Element Plus 的UI按需引入配置
    AutoImport({
      resolvers: [ElementPlusResolver()]
    }),
    Components({
      resolvers: [ElementPlusResolver()]
    }),
    ElementPlus({
      defaultLocale: 'zh-cn'
    })
  ],
  test: {
    globals: true,
    environment: 'jsdom',
    exclude: [...configDefaults.exclude, 'e2e/*'],
    root: fileURLToPath(new URL('./', import.meta.url))
  },
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'axios']
  },
  build: {
    sourcemap: true
  },
  server: {
    port: 8080,
    host: '0.0.0.0',
    proxy: {
      '/api/': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        rewrite: p => p.replace(/^\/api/, '')
      },
      '/api-prod/': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        rewrite: p => p.replace(/^\/api-prod/, '')
      },
      '/api-test/': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        rewrite: p => p.replace(/^\/api-test/, '')
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})
