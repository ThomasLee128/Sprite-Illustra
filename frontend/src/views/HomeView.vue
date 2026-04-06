<!--
文件名：HomeView.vue
功能描述：首页 - 文档上传页面。用户在此上传文档、选择模型和风格，启动处理。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 实现文件上传区域（拖拽上传 + 点击上传）
      - 使用 FileUploader 组件
      - 支持 .txt, .md, .docx, .pdf
      - 显示文件大小限制提示（50MB）
- [x] 实现模型选择区域
      - 使用 ModelSelector 组件选择文本模型和图片模型
      - 如果模型列表为空，提示用户先去设置页面配置
- [x] 实现风格选择（flat/realistic/watercolor/sketch/cartoon/tech）
      - 卡片式 UI，每种风格配示意图标
- [x] 实现"开始处理"按钮
      - 验证：已选文件 + 已选模型
      - 调用 uploadDocument -> startProcessing
      - 跳转到 /process/{taskId}
-->

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSettingsStore } from '../stores/settings'
import { useTaskStore } from '../stores/task'
import { uploadDocument } from '../api/documents'

const router = useRouter()
const settingsStore = useSettingsStore()
const taskStore = useTaskStore()

const selectedFile = ref<File | null>(null)
const selectedTextModel = ref('')
const selectedImageModel = ref('')
const selectedStyle = ref('flat')
const isLoading = ref(false)
const errorMessage = ref('')
const fileInputRef = ref<HTMLInputElement | null>(null)

const styleOptions = [
  { id: 'flat', label: '扁平矢量', icon: '🎨' },
  { id: 'realistic', label: '写实风格', icon: '📸' },
  { id: 'watercolor', label: '水彩风格', icon: '🎭' },
  { id: 'sketch', label: '素描风格', icon: '✏️' },
  { id: 'cartoon', label: '卡通风格', icon: '🎪' },
  { id: 'tech', label: '科技示意', icon: '⚙️' },
  { id: 'ppt', label: 'PPT模式', icon: '📊' },
]

onMounted(async () => {
  await settingsStore.fetchSettings()
  await settingsStore.fetchModels()
  if (settingsStore.textModels.length > 0) {
    selectedTextModel.value = settingsStore.defaultTextModel || settingsStore.textModels[0].id
  }
  if (settingsStore.imageModels.length > 0) {
    selectedImageModel.value = settingsStore.defaultImageModel || settingsStore.imageModels[0].id
  }
})

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    const allowedTypes = ['.txt', '.md', '.docx', '.pdf']
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
    
    if (!allowedTypes.includes(fileExt)) {
      errorMessage.value = '不支持的文件格式，请上传 .txt, .md, .docx 或 .pdf 文件'
      return
    }
    
    if (file.size > 50 * 1024 * 1024) {
      errorMessage.value = '文件大小不能超过 50MB'
      return
    }
    
    selectedFile.value = file
    errorMessage.value = ''
  }
}

function handleDrop(event: DragEvent) {
  event.preventDefault()
  if (event.dataTransfer && event.dataTransfer.files.length > 0) {
    const file = event.dataTransfer.files[0]
    const fakeEvent = { target: { files: [file] } } as unknown as Event
    handleFileChange(fakeEvent)
  }
}

function handleDragOver(event: DragEvent) {
  event.preventDefault()
}

async function startProcessing() {
  if (!selectedFile.value) {
    errorMessage.value = '请先选择要上传的文件'
    return
  }
  if (!selectedTextModel.value) {
    errorMessage.value = '请选择文案理解模型'
    return
  }
  if (!selectedImageModel.value) {
    errorMessage.value = '请选择图片生成模型'
    return
  }
  
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const uploadResp = await uploadDocument(selectedFile.value)
    taskStore.reset()
    const isPPTMode = selectedStyle.value === 'ppt'
    await taskStore.startProcessing(
      uploadResp.task_id,
      selectedTextModel.value,
      selectedImageModel.value,
      isPPTMode ? 'tech' : selectedStyle.value,
      isPPTMode
    )
    router.push(`/process/${uploadResp.task_id}`)
  } catch (e: any) {
    errorMessage.value = e.message || '上传文件失败，请重试'
  } finally {
    isLoading.value = false
  }
}

function isFormValid() {
  return selectedFile.value && selectedTextModel.value && selectedImageModel.value && !isLoading.value
}
</script>

<template>
  <div class="space-y-8">
    <!-- 页面标题 -->
    <div class="text-center">
      <h1 class="text-3xl font-bold text-gray-900">智灵智能插图 <span class="text-xl text-gray-500">Sprite Illustra</span></h1>
      <p class="mt-2 text-gray-500">上传文档，AI 自动在合适的位置插入精美配图</p>
    </div>

    <!-- 文件上传区 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">1. 上传文档</h2>
      <div
        class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-indigo-400 transition-colors cursor-pointer"
        @click="fileInputRef?.click()"
        @drop="handleDrop"
        @dragover="handleDragOver"
      >
        <input
          ref="fileInputRef"
          type="file"
          class="hidden"
          accept=".txt,.md,.docx,.pdf"
          @change="handleFileChange"
        />
        <div v-if="selectedFile" class="space-y-2">
          <div class="text-xl text-green-600">✓</div>
          <p class="text-gray-700 font-medium">{{ selectedFile.name }}</p>
          <p class="text-sm text-gray-400">{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB</p>
          <button
            type="button"
            class="text-indigo-600 hover:text-indigo-800 text-sm"
            @click.stop="selectedFile = null"
          >
            重新选择
          </button>
        </div>
        <div v-else>
          <p class="text-gray-400">拖拽文件到此处，或点击选择文件</p>
          <p class="text-sm text-gray-300 mt-2">支持 .txt .md .docx .pdf（最大 50MB）</p>
        </div>
      </div>
    </div>

    <!-- 模型选择区 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">2. 选择 AI 模型</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">文案理解模型</label>
          <select
            v-model="selectedTextModel"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            :disabled="settingsStore.textModels.length === 0"
          >
            <option v-if="settingsStore.textModels.length === 0" value="">
              请先在设置页面拉取模型列表
            </option>
            <option
              v-for="model in settingsStore.textModels"
              :key="model.id"
              :value="model.id"
            >
              {{ model.id }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">图片生成模型</label>
          <select
            v-model="selectedImageModel"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            :disabled="settingsStore.imageModels.length === 0"
          >
            <option v-if="settingsStore.imageModels.length === 0" value="">
              请先在设置页面拉取模型列表
            </option>
            <option
              v-for="model in settingsStore.imageModels"
              :key="model.id"
              :value="model.id"
            >
              {{ model.id }}
            </option>
          </select>
        </div>
      </div>
      <p v-if="settingsStore.textModels.length === 0" class="mt-2 text-sm text-yellow-600">
        提示：请先去
        <router-link to="/settings" class="text-indigo-600 hover:underline">设置页面</router-link>
        配置 API 并拉取模型列表
      </p>
    </div>

    <!-- 风格选择区 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">3. 选择插图风格</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        <div
          v-for="style in styleOptions"
          :key="style.id"
          class="rounded-lg p-3 text-center cursor-pointer transition-all"
          :class="
            selectedStyle === style.id
              ? 'border-2 border-indigo-500 bg-indigo-50'
              : 'border border-gray-200 hover:border-indigo-300'
          "
          @click="selectedStyle = style.id"
        >
          <div class="text-2xl mb-1">{{ style.icon }}</div>
          <div class="text-sm font-medium">{{ style.label }}</div>
        </div>
      </div>
      <p v-if="selectedStyle === 'ppt'" class="mt-3 text-sm text-gray-500">
        PPT模式：将每一段内容都做成一张PPT页面图片，可直接插入PPT使用
      </p>
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-700">{{ errorMessage }}</p>
    </div>

    <!-- 开始按钮 -->
    <div class="text-center">
      <button
        class="bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-indigo-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        :disabled="!isFormValid()"
        @click="startProcessing"
      >
        {{ isLoading ? '处理中...' : '开始智能配图' }}
      </button>
    </div>
  </div>
</template>
