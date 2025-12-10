// https://nuxt.com/docs/api/configuration/nuxt-config
import path from 'path'

export default defineNuxtConfig({
  // vite: {
  //   resolve: {
  //     alias: {
  //       '@': path.resolve(__dirname, './')
  //     }
  //   }
  // },
  // dir: {
  //   pages: 'pages'
  // },
  compatibilityDate: '2025-12-09',
  devtools: { enabled: true },
  modules: [
    '@pinia/nuxt',
  ],
  // css: ['@/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1'
    }
  }
})
