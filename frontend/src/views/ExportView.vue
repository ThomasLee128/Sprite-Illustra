<!--
文件名：ExportView.vue
功能描述：导出选项页面。用户选择导出格式并下载文件。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 展示 4 种导出格式卡片（Word, PDF, Markdown, HTML）
      - 每种格式附说明（如 "适合编辑和打印"、"适合分享和归档" 等）
- [ ] 点击格式卡片 -> 调用 POST /api/export { task_id, format }
- [ ] 显示导出中 loading 状态
- [ ] 导出完成后自动触发下载（window.open 或 a.download）
- [ ] 支持"返回预览"按钮
-->

<script setup lang="ts">
// TODO: 导入 stores 和 router
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-8">
    <div class="text-center">
      <h1 class="text-2xl font-bold text-gray-900">导出文档</h1>
      <p class="mt-2 text-gray-500">选择您需要的文件格式进行导出</p>
    </div>

    <!-- 格式选择 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Word -->
      <div class="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-md hover:border-indigo-300 border-2 border-transparent transition-all">
        <div class="text-3xl mb-3">📄</div>
        <h3 class="font-semibold text-gray-900">Word (.docx)</h3>
        <p class="text-sm text-gray-500 mt-1">适合继续编辑和打印</p>
      </div>
      <!-- PDF -->
      <div class="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-md hover:border-indigo-300 border-2 border-transparent transition-all">
        <div class="text-3xl mb-3">📕</div>
        <h3 class="font-semibold text-gray-900">PDF</h3>
        <p class="text-sm text-gray-500 mt-1">适合分享和归档</p>
      </div>
      <!-- Markdown -->
      <div class="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-md hover:border-indigo-300 border-2 border-transparent transition-all">
        <div class="text-3xl mb-3">📝</div>
        <h3 class="font-semibold text-gray-900">Markdown (.md)</h3>
        <p class="text-sm text-gray-500 mt-1">适合技术文档和博客发布</p>
      </div>
      <!-- HTML -->
      <div class="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-md hover:border-indigo-300 border-2 border-transparent transition-all">
        <div class="text-3xl mb-3">🌐</div>
        <h3 class="font-semibold text-gray-900">HTML</h3>
        <p class="text-sm text-gray-500 mt-1">适合网页展示，独立可用</p>
      </div>
    </div>

    <!-- 返回按钮 -->
    <div class="text-center">
      <button class="text-gray-500 hover:text-gray-700 text-sm">← 返回预览</button>
    </div>
  </div>
</template>
