/**
 * 文件名：main.ts
 * 功能描述：Vue 应用入口，初始化 Pinia 状态管理和 Vue Router
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 */

import '@/styles/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
