<!--
文件名：ExportView.vue
功能描述：导出选项页面。用户选择导出格式并下载文件。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 展示 4 种导出格式卡片（Word, PDF, Markdown, HTML）
      - 每种格式附说明（如 "适合编辑和打印"、"适合分享和归档" 等）
- [x] 点击格式卡片 -> 调用 POST /api/export { task_id, format }
- [x] 显示导出中 loading 状态
- [x] 导出完成后自动触发下载（window.open 或 a.download）
- [x] 支持"返回预览"按钮
-->

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { exportDocument, downloadExport, downloadFile, type ExportFormat } from '../api/export'

const route = useRoute()
const router = useRouter()

const taskId = computed(() => route.params.taskId as string)
const isExporting = ref(false)
const exportingFormat = ref<ExportFormat | null>(null)
const errorMessage = ref('')

const formatOptions: Array<{
  id: ExportFormat
  label: string
  icon: string
  description: string
  extension: string
}> = [
  { id: 'docx', label: 'Word (.docx)', icon: '📄', description: '适合继续编辑和打印', extension: '.docx' },
  { id: 'md', label: 'Markdown (.md)', icon: '📝', description: '适合技术文档和博客发布', extension: '.md' },
  { id: 'html', label: 'HTML', icon: '🌐', description: '适合网页展示，独立可用', extension: '.html' },
]

async function handleExport(format: ExportFormat) {
  isExporting.value = true
  exportingFormat.value = format
  errorMessage.value = ''
  
  try {
    const exportResponse = await exportDocument(taskId.value, format)
    const blob = await downloadExport(exportResponse.export_id)
    downloadFile(blob, exportResponse.filename)
  } catch (e: any) {
    errorMessage.value = e.response?.data?.detail || e.response?.data?.error || e.message || '导出失败，请重试'
  } finally {
    isExporting.value = false
    exportingFormat.value = null
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-8">
    <div class="text-center">
      <h1 class="text-2xl font-bold text-gray-900">导出文档</h1>
      <p class="mt-2 text-gray-500">选择您需要的文件格式进行导出</p>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-700">{{ errorMessage }}</p>
    </div>

    <!-- 格式选择 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="option in formatOptions"
        :key="option.id"
        class="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-md transition-all"
        :class="
          exportingFormat === option.id
            ? 'border-2 border-indigo-500 bg-indigo-50 opacity-75 cursor-not-allowed'
            : 'border-2 border-transparent hover:border-indigo-300'
        "
        @click="!isExporting && handleExport(option.id)"
      >
        <div class="text-3xl mb-3">{{ option.icon }}</div>
        <h3 class="font-semibold text-gray-900">{{ option.label }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ option.description }}</p>
        <div v-if="exportingFormat === option.id" class="mt-3 flex items-center text-indigo-600">
          <div class="animate-spin mr-2">⏳</div>
          <span class="text-sm">正在导出...</span>
        </div>
      </div>
    </div>

    <!-- 返回按钮 -->
    <div class="text-center">
      <button
        class="text-gray-500 hover:text-gray-700 text-sm"
        @click="router.push(`/preview/${taskId}`)"
      >
        ← 返回预览
      </button>
    </div>
  </div>
</template>
