<!--
文件名：ProcessView.vue
功能描述：处理进度页面。通过 SSE 实时显示文档处理进度，
         包括解析、AI 分析、图片生成各阶段。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 页面加载时从路由参数获取 taskId
- [ ] 调用 taskStore.connectSSE(taskId) 建立 SSE 连接
- [ ] 使用 ProgressTracker 组件展示进度
- [ ] 展示当前阶段信息（解析中/分析中/生成第N张插图...）
- [ ] 完成时自动跳转到 /preview/{taskId}
- [ ] 失败时展示错误信息和重试按钮
- [ ] 页面离开时断开 SSE 连接（onUnmounted）
-->

<script setup lang="ts">
// TODO: 导入 useRoute, useRouter, useTaskStore, onMounted, onUnmounted
</script>

<template>
  <div class="max-w-2xl mx-auto space-y-8">
    <div class="text-center">
      <h1 class="text-2xl font-bold text-gray-900">正在处理文档</h1>
      <p class="mt-2 text-gray-500">AI 正在分析您的文档并生成配图，请耐心等待...</p>
    </div>

    <!-- 进度条 -->
    <div class="bg-white rounded-lg shadow p-6">
      <!-- TODO: ProgressTracker 组件 -->
      <div class="space-y-4">
        <!-- 总进度条 -->
        <div>
          <div class="flex justify-between text-sm text-gray-600 mb-1">
            <span>总进度</span>
            <span>0%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div class="bg-indigo-600 h-3 rounded-full transition-all duration-500" style="width: 0%"></div>
          </div>
        </div>

        <!-- 阶段指示 -->
        <div class="flex items-center space-x-4 text-sm">
          <div class="flex items-center space-x-1 text-gray-400">
            <span class="w-2 h-2 rounded-full bg-gray-300"></span>
            <span>文档解析</span>
          </div>
          <div class="flex items-center space-x-1 text-gray-400">
            <span class="w-2 h-2 rounded-full bg-gray-300"></span>
            <span>AI 分析</span>
          </div>
          <div class="flex items-center space-x-1 text-gray-400">
            <span class="w-2 h-2 rounded-full bg-gray-300"></span>
            <span>生成插图</span>
          </div>
          <div class="flex items-center space-x-1 text-gray-400">
            <span class="w-2 h-2 rounded-full bg-gray-300"></span>
            <span>完成</span>
          </div>
        </div>

        <!-- 当前状态消息 -->
        <p class="text-center text-gray-500 text-sm">等待开始...</p>
      </div>
    </div>
  </div>
</template>
