<!--
文件名：PreviewView.vue
功能描述：插图预览与调整页面。展示处理结果，允许用户：
         - 查看文档内容和插入的插图
         - 删除不需要的插图
         - 重新生成不满意的插图（可修改 prompt）
         - 调整插图位置
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 页面加载时获取 taskId，调用 documentStore.fetchResult(taskId)
- [x] 渲染文档内容：按 sections 顺序展示标题、段落等
- [x] 在对应位置插入 IllustrationCard 组件展示插图
- [x] IllustrationCard 操作按钮：删除、重新生成、编辑 prompt
- [x] 拖拽调整插图位置（可选，MVP 阶段可用上下箭头）
- [x] 底部"导出文档"按钮 -> 跳转到 /export/{taskId}
- [x] 使用 DocumentPreview 组件整合文档和插图的混排展示
-->

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTaskResult, removeIllustration, regenerateIllustration, moveIllustration } from '../api/tasks'
import type { IllustratedDocument, IllustrationItem, DocumentSection } from '../api/tasks'

const route = useRoute()
const router = useRouter()

const taskId = computed(() => route.params.taskId as string)
const document = ref<IllustratedDocument | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')
const editingIllustrationId = ref<string | null>(null)
const editingPrompt = ref('')

async function fetchResult() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    document.value = await getTaskResult(taskId.value)
  } catch (e: any) {
    errorMessage.value = e.message || '获取文档结果失败'
  } finally {
    isLoading.value = false
  }
}

async function handleRemoveIllustration(illustrationId: string) {
  if (!confirm('确定要删除这张插图吗？')) return
  try {
    await removeIllustration(taskId.value, illustrationId)
    await fetchResult()
  } catch (e: any) {
    alert('删除失败：' + (e.message || '未知错误'))
  }
}

function startRegenerate(illustration: IllustrationItem) {
  editingIllustrationId.value = illustration.id
  editingPrompt.value = illustration.prompt
}

let pollInterval: number | null = null

async function confirmRegenerate() {
  if (!editingIllustrationId.value) return
  try {
    await regenerateIllustration(taskId.value, editingIllustrationId.value, {
      prompt: editingPrompt.value,
    })
    editingIllustrationId.value = null
    await fetchResult()
    
    // 开始轮询，检查生成状态
    startPolling()
  } catch (e: any) {
    alert('重新生成失败：' + (e.message || '未知错误'))
  }
}

function startPolling() {
  if (pollInterval) return
  
  pollInterval = window.setInterval(async () => {
    await fetchResult()
    
    // 检查是否还有正在生成的插图
    const hasGenerating = document.value?.illustrations.some(
      illu => illu.status === 'generating'
    )
    
    if (!hasGenerating) {
      // 没有正在生成的了，停止轮询
      stopPolling()
    }
  }, 2000)
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

async function handleMove(illustrationId: string, direction: 'up' | 'down') {
  if (!document.value) return
  const illustrations = [...document.value.illustrations]
  const index = illustrations.findIndex(i => i.id === illustrationId)
  if (index === -1) return

  let newIndex: number
  if (direction === 'up' && index > 0) {
    newIndex = index - 1
  } else if (direction === 'down' && index < illustrations.length - 1) {
    newIndex = index + 1
  } else {
    return
  }

  const targetIllustration = illustrations[newIndex]
  try {
    await moveIllustration(taskId.value, illustrationId, {
      after_section_id: targetIllustration.after_section_id,
    })
    await fetchResult()
  } catch (e: any) {
    alert('移动失败：' + (e.message || '未知错误'))
  }
}

function getSectionContent(section: DocumentSection) {
  if (section.type === 'heading') {
    const level = Math.max(1, Math.min(6, section.level))
    const tag = `h${level}`
    return `<${tag} class="font-bold text-gray-900">${section.content}</${tag}>`
  } else if (section.type === 'code') {
    return `<pre class="bg-gray-100 p-4 rounded-lg text-sm overflow-x-auto"><code>${section.content}</code></pre>`
  } else if (section.type === 'list') {
    return `<ul class="list-disc list-inside space-y-1"><li>${section.content}</li></ul>`
  } else if (section.type === 'blockquote') {
    return `<blockquote class="border-l-4 border-gray-300 pl-4 text-gray-600 italic">${section.content}</blockquote>`
  }
  return `<p class="text-gray-700">${section.content}</p>`
}

function getIllustrationsForSection(sectionId: string) {
  if (!document.value) return []
  return document.value.illustrations.filter(i => i.after_section_id === sectionId)
}

onMounted(() => {
  fetchResult()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">预览与调整</h1>
      <button
        class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
        @click="router.push(`/export/${taskId}`)"
      >
        导出文档
      </button>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-700">{{ errorMessage }}</p>
    </div>

    <div v-if="isLoading" class="text-center py-12">
      <p class="text-gray-500">加载中...</p>
    </div>

    <!-- 文档预览区 -->
    <div v-if="document && !isLoading" class="bg-white rounded-lg shadow p-8">
      <div class="space-y-6">
        <template v-for="section in document.document.sections" :key="section.id">
          <div v-html="getSectionContent(section)" class="space-y-2"></div>

          <div
            v-for="illustration in getIllustrationsForSection(section.id)"
            :key="illustration.id"
            class="my-6 border border-gray-200 rounded-lg overflow-hidden"
          >
            <div class="relative">
              <img
                v-if="illustration.image_path"
                :src="`/api/images/${illustration.image_path}`"
                :alt="illustration.description_cn"
                class="w-full h-auto"
              />
              <div v-else class="bg-gray-100 h-64 flex items-center justify-center">
                <p class="text-gray-400">
                  {{ illustration.status === 'pending' ? '等待生成' : illustration.status === 'generating' ? '正在生成...' : '生成失败' }}
                </p>
              </div>
            </div>
            <div class="p-4 bg-gray-50 border-t border-gray-200">
              <p class="text-sm text-gray-600 mb-2">{{ illustration.description_cn }}</p>
              <p class="text-xs text-gray-400 mb-3">Prompt: {{ illustration.prompt }}</p>
              <div class="flex items-center justify-between">
                <div class="flex space-x-2">
                  <button
                    class="text-sm text-indigo-600 hover:text-indigo-800"
                    @click="startRegenerate(illustration)"
                  >
                    重新生成
                  </button>
                  <button
                    class="text-sm text-red-600 hover:text-red-800"
                    @click="handleRemoveIllustration(illustration.id)"
                  >
                    删除
                  </button>
                </div>
                <div class="flex space-x-1">
                  <button
                    class="text-sm text-gray-500 hover:text-gray-700 px-2"
                    @click="handleMove(illustration.id, 'up')"
                  >
                    ↑
                  </button>
                  <button
                    class="text-sm text-gray-500 hover:text-gray-700 px-2"
                    @click="handleMove(illustration.id, 'down')"
                  >
                    ↓
                  </button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- 重新生成对话框 -->
    <div v-if="editingIllustrationId" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">重新生成插图</h3>
        <label class="block text-sm font-medium text-gray-700 mb-1">修改 Prompt</label>
        <textarea
          v-model="editingPrompt"
          class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
          rows="4"
        ></textarea>
        <div class="mt-4 flex justify-end space-x-3">
          <button
            class="text-gray-600 hover:text-gray-800 px-4 py-2"
            @click="editingIllustrationId = null"
          >
            取消
          </button>
          <button
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="confirmRegenerate"
          >
            确认生成
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
