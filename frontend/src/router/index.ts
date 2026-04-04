/**
 * 文件名：router/index.ts
 * 功能描述：Vue Router 路由配置。定义应用的 5 个主要页面路由。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 */

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/process/:taskId',
      name: 'process',
      component: () => import('@/views/ProcessView.vue'),
    },
    {
      path: '/preview/:taskId',
      name: 'preview',
      component: () => import('@/views/PreviewView.vue'),
    },
    {
      path: '/export/:taskId',
      name: 'export',
      component: () => import('@/views/ExportView.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
    },
  ],
})

export default router
