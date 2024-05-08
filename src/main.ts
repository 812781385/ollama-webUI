import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'

import App from './App.vue'
import Axios from './apis/ajax'

import mountElementUI from './utils/elementUI'
import 'element-plus/theme-chalk/dark/css-vars.css'
import 'highlight.js/styles/atom-one-dark.css'

// eslint-disable-next-line import/order
import hljs from 'highlight.js'

import 'katex/dist/katex.min.css'
import '@/styles/lib/highlight.scss'
import '@/styles/lib/github-markdown.scss'

document.title = import.meta.env.VITE_APP_TITLE

const app = createApp(App)
app.use(createPinia())
app.provide('$http', Axios)
app.use(router)
app.directive('highlight', (el) => {
  const blocks = el.querySelectorAll('pre code')
  blocks.forEach((block: any) => {
    hljs.highlightBlock(block)
  })
})

// 全量引入Element UI
mountElementUI(app)
app.mount('#app')
