<!--
文件名：App.vue
功能描述：应用根组件。包含顶部导航栏和路由视图。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 美化导航栏样式（品牌色、图标、响应式布局）
- [ ] 添加全局 loading 状态指示器
-->

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <!-- Logo -->
          <div class="flex items-center space-x-2">
            <span class="text-xl font-bold text-indigo-600">智灵智能插图</span><span class="text-sm text-gray-500 ml-2">Sprite Illustra</span>
          </div>

          <!-- 导航链接 -->
          <div class="flex space-x-8">
            <RouterLink
              to="/"
              class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium transition-colors"
              active-class="text-indigo-600 border-b-2 border-indigo-600"
            >
              首页
            </RouterLink>
            <RouterLink
              to="/settings"
              class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium transition-colors"
              active-class="text-indigo-600 border-b-2 border-indigo-600"
            >
              设置
            </RouterLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <RouterView />
    </main>
  </div>
</template>
