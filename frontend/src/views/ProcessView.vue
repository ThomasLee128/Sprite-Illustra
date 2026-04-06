<!--
文件名：ProcessView.vue
功能描述：处理进度页面 + 预览界面。通过 SSE 实时显示文档处理进度，
         包括解析、AI 分析、预览阶段、图片生成各阶段。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 页面加载时从路由参数获取 taskId
- [x] 调用 taskStore.connectSSE(taskId) 建立 SSE 连接
- [x] 使用 ProgressTracker 组件展示进度
- [x] 展示当前阶段信息（解析中/分析中/预览中/生成第N张插图...）
- [x] 预览阶段：显示文档、插图位置、英文和中文提示词
- [x] 完成时自动跳转到 /preview/{taskId}
- [x] 失败时展示错误信息和重试按钮
- [x] 页面离开时断开 SSE 连接（onUnmounted）
-->

<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '../stores/task'
import { useSettingsStore } from '../stores/settings'
import { getPreview, confirmPreview, type PreviewData } from '../api/tasks'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()
const settingsStore = useSettingsStore()

const taskId = computed(() => route.params.taskId as string)
const previewData = ref<PreviewData | null>(null)
const isLoadingPreview = ref(false)

const phaseOrder = [
  'uploaded',
  'parsing',
  'analyzing',
  'preview',
  'generating',
  'complete',
]

function getPhaseIndex(phase: string) {
  const index = phaseOrder.indexOf(phase)
  return index === -1 ? 0 : index
}

function getPhaseLabel(phase: string) {
  const labels: Record<string, string> = {
    uploaded: '等待处理',
    parsing: '文档解析',
    analyzing: 'AI 分析',
    preview: '预览确认',
    generating: '生成插图',
    complete: '完成',
    failed: '失败',
  }
  return labels[phase] || phase
}

async function handleRetry() {
  if (!taskId.value) return
  taskStore.reset()
  router.push('/')
}

async function handleConfirmPreview() {
  if (!taskId.value) return
  
  // 如果 taskStore 中没有 imageModel，使用 settingsStore 中的默认值
  let imageModel = taskStore.imageModel
  if (!imageModel) {
    imageModel = settingsStore.defaultImageModel || settingsStore.imageModels[0]?.id || ''
  }
  
  if (!imageModel) {
    console.error('没有可用的图片生成模型')
    return
  }
  
  try {
    await confirmPreview(taskId.value, { image_model: imageModel })
    // 确认预览后，重新建立SSE连接来监听图片生成进度
    previewData.value = null
    await taskStore.connectToSSE(taskId.value)
  } catch (error) {
    console.error('确认预览失败:', error)
  }
}

async function fetchPreview() {
  if (!taskId.value) return
  isLoadingPreview.value = true
  try {
    previewData.value = await getPreview(taskId.value)
  } catch (error) {
    console.error('获取预览失败:', error)
  } finally {
    isLoadingPreview.value = false
  }
}

onMounted(async () => {
  if (taskId.value) {
    // 先加载设置和模型（刷新后需要）
    await settingsStore.fetchSettings()
    await settingsStore.fetchModels()
    
    await taskStore.fetchTaskStatus(taskId.value)
    
    if (taskStore.phase === 'preview') {
      await fetchPreview()
    } else if (taskStore.phase !== 'complete' && taskStore.phase !== 'failed') {
      await taskStore.connectToSSE(taskId.value, async () => {
        // 当进入 preview 阶段时，获取预览数据
        await fetchPreview()
      })
    } else if (taskStore.phase === 'complete') {
      router.push(`/preview/${taskId.value}`)
    }
  }
})

// 监听 phase 变化
watch(
  () => taskStore.phase,
  (newPhase) => {
    if (newPhase === 'preview' && !previewData.value) {
      fetchPreview()
    } else if (newPhase === 'complete') {
      router.push(`/preview/${taskId.value}`)
    }
  }
)

onUnmounted(() => {
  taskStore.disconnect()
})
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div class="text-center">
      <h1 class="text-2xl font-bold text-gray-900">正在处理文档</h1>
      <p class="mt-2 text-gray-500">
        {{ taskStore.phase === 'preview' ? '请确认插图位置和提示词' : 'AI 正在分析您的文档并生成配图，请耐心等待...' }}
      </p>
    </div>

    <!-- 预览阶段界面 -->
    <div v-if="taskStore.phase === 'preview'" class="space-y-6">
      <!-- 确认按钮 -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-lg font-medium text-gray-900">分析完成</h3>
            <p class="text-sm text-gray-500">
              计划生成 {{ previewData?.illustrations.length || 0 }} 张插图
            </p>
          </div>
          <button
            class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isLoadingPreview"
            @click="handleConfirmPreview"
          >
            确认并开始生成
          </button>
        </div>
      </div>

      <!-- 预览内容 -->
      <div v-if="previewData" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-6">文档预览与插图计划</h3>
        
        <div class="space-y-6">
          <!-- 遍历段落 -->
          <div v-for="(section, idx) in previewData.document.sections" :key="section.id" class="space-y-2">
            <!-- 段落内容 -->
            <div 
              class="p-4 rounded-lg"
              :class="section.type === 'heading' ? 'bg-gray-50 font-medium' : 'bg-gray-50'"
            >
              <template v-if="section.type === 'heading'">
                <h3 :style="{ fontSize: `${Math.max(16, 24 - section.level * 2)}px` }">
                  {{ section.content }}
                </h3>
              </template>
              <template v-else-if="section.type === 'code'">
                <pre class="text-sm font-mono bg-gray-100 p-3 rounded">{{ section.content }}</pre>
              </template>
              <template v-else>
                <p>{{ section.content }}</p>
              </template>
            </div>

            <!-- 该段落后面的插图 -->
            <div 
              v-for="illu in previewData.illustrations.filter(i => i.after_section_id === section.id)" 
              :key="illu.id"
              class="ml-8 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-lg"
            >
              <div class="flex items-start space-x-3">
                <div class="mt-1">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <p class="text-sm font-medium text-yellow-800 mb-1">在此处插入插图</p>
                  <div class="space-y-1 text-sm">
                    <div>
                      <span class="text-yellow-700 font-medium">中文说明：</span>
                      <span class="text-yellow-600">{{ illu.description_cn }}</span>
                    </div>
                    <div>
                      <span class="text-yellow-700 font-medium">英文提示词：</span>
                      <span class="text-yellow-600 font-mono text-xs">{{ illu.prompt }}</span>
                    </div>
                    <div>
                      <span class="text-yellow-700 font-medium">风格：</span>
                      <span class="text-yellow-600">{{ illu.style }}</span>
                    </div>
                    <div v-if="illu.reason">
                      <span class="text-yellow-700 font-medium">原因：</span>
                      <span class="text-yellow-600">{{ illu.reason }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载中 -->
      <div v-else-if="isLoadingPreview" class="bg-white rounded-lg shadow p-12 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto mb-4"></div>
        <p class="text-gray-500">正在加载预览数据...</p>
      </div>
    </div>

    <!-- 进度条（非预览阶段） -->
    <div v-else class="bg-white rounded-lg shadow p-6">
      <div class="space-y-6">
        <!-- 总进度条 -->
        <div>
          <div class="flex justify-between text-sm text-gray-600 mb-1">
            <span>总进度</span>
            <span>{{ Math.round(taskStore.progress * 100) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div
              class="bg-indigo-600 h-3 rounded-full transition-all duration-500"
              :style="{ width: `${taskStore.progress * 100}%` }"
            ></div>
          </div>
        </div>

        <!-- 阶段指示 -->
        <div class="flex items-center justify-between text-sm">
          <div
            v-for="(phase, index) in ['parsing', 'analyzing', 'preview', 'generating', 'complete']"
            :key="phase"
            class="flex items-center space-x-1"
            :class="
              getPhaseIndex(taskStore.phase) > phaseOrder.indexOf(phase)
                ? 'text-green-600'
                : getPhaseIndex(taskStore.phase) === phaseOrder.indexOf(phase)
                ? 'text-indigo-600'
                : 'text-gray-400'
            "
          >
            <span
              class="w-3 h-3 rounded-full"
              :class="
                getPhaseIndex(taskStore.phase) > phaseOrder.indexOf(phase)
                  ? 'bg-green-500'
                  : getPhaseIndex(taskStore.phase) === phaseOrder.indexOf(phase)
                  ? 'bg-indigo-500 animate-pulse'
                  : 'bg-gray-300'
              "
            ></span>
            <span>{{ getPhaseLabel(phase) }}</span>
          </div>
        </div>

        <!-- 当前状态消息 -->
        <p class="text-center text-gray-600">{{ taskStore.message }}</p>

        <!-- 插图生成进度 -->
        <div v-if="taskStore.illustrationCount > 0" class="text-center">
          <p class="text-sm text-gray-500">
            插图生成进度：{{ taskStore.completedCount }} / {{ taskStore.illustrationCount }}
          </p>
        </div>
      </div>
    </div>

    <!-- 失败提示 -->
    <div v-if="taskStore.phase === 'failed'" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
      <p class="text-red-700 font-medium mb-2">处理失败</p>
      <p class="text-red-600 text-sm mb-4">{{ taskStore.errorMessage }}</p>
      <button
        class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
        @click="handleRetry"
      >
        重新上传
      </button>
    </div>
  </div>
</template>
