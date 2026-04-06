<!--
文件名：SettingsView.vue
功能描述：API 聚合站设置页面。用户在此配置 API URL 和 Key，
         一键拉取模型列表，选择默认模型。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 页面加载时调用 settingsStore.fetchSettings() 填充表单
- [x] 实现表单：API 聚合站 URL 输入框、API Key 输入框（密码类型，带显示/隐藏切换）
- [x] 实现"保存设置"按钮 -> settingsStore.saveSettings()
- [x] 实现"一键拉取模型"按钮 -> settingsStore.pullModels()
      - 拉取中显示 loading 动画
      - 拉取成功后展示模型列表（分文本模型和图片模型两列）
      - 拉取失败显示错误提示
- [x] 模型列表展示：表格形式，显示模型 ID 和提供者
- [x] 默认模型选择：下拉框选择默认文本模型和图片模型
- [x] 保存默认模型选择
-->

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'

const settingsStore = useSettingsStore()

const apiBaseUrl = ref('')
const apiKey = ref('')
const showApiKey = ref(false)
const defaultTextModel = ref('')
const defaultImageModel = ref('')
const successMessage = ref('')
const errorMessage = ref('')

const isSaving = computed(() => settingsStore.loading)
const isPulling = computed(() => settingsStore.loading)

async function handleSaveSettings() {
  successMessage.value = ''
  errorMessage.value = ''
  try {
    await settingsStore.saveSettings({
      api_base_url: apiBaseUrl.value,
      api_key: apiKey.value,
      default_text_model: defaultTextModel.value,
      default_image_model: defaultImageModel.value,
    })
    successMessage.value = '设置保存成功'
  } catch (e: any) {
    errorMessage.value = e.message || '保存设置失败'
  }
}

async function handlePullModels() {
  successMessage.value = ''
  errorMessage.value = ''
  try {
    await settingsStore.pullModelsFromAPI()
    successMessage.value = '模型列表拉取成功'
  } catch (e: any) {
    errorMessage.value = e.message || '拉取模型列表失败'
  }
}

onMounted(async () => {
  await settingsStore.fetchSettings()
  await settingsStore.fetchModels()
  apiBaseUrl.value = settingsStore.apiBaseUrl
  defaultTextModel.value = settingsStore.defaultTextModel
  defaultImageModel.value = settingsStore.defaultImageModel
})
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-8">
    <h1 class="text-2xl font-bold text-gray-900">API 设置</h1>

    <!-- 提示消息 -->
    <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-4">
      <p class="text-green-700">{{ successMessage }}</p>
    </div>
    <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-700">{{ errorMessage }}</p>
    </div>

    <!-- API 配置表单 -->
    <div class="bg-white rounded-lg shadow p-6 space-y-4">
      <h2 class="text-lg font-semibold text-gray-800">聚合站配置</h2>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">API 聚合站 URL</label>
        <input
          type="url"
          v-model="apiBaseUrl"
          placeholder="https://api.spiritgpu.com"
          class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        />
        <p class="text-xs text-gray-400 mt-1">支持 New API / One API 等 OpenAI 兼容聚合服务</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">API Key</label>
        <div class="relative">
          <input
            :type="showApiKey ? 'text' : 'password'"
            v-model="apiKey"
            placeholder="sk-..."
            class="w-full border border-gray-300 rounded-md px-3 py-2 pr-10 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
          <button
            type="button"
            class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            @click="showApiKey = !showApiKey"
          >
            {{ showApiKey ? '🙈' : '👁️' }}
          </button>
        </div>
        <p v-if="settingsStore.apiKeyMasked" class="text-xs text-gray-400 mt-1">
          当前 Key：{{ settingsStore.apiKeyMasked }}
        </p>
      </div>

      <div class="flex space-x-3">
        <button
          :disabled="isSaving"
          class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm hover:bg-indigo-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          @click="handleSaveSettings"
        >
          {{ isSaving ? '保存中...' : '保存设置' }}
        </button>
        <button
          :disabled="isPulling"
          class="bg-white border border-indigo-600 text-indigo-600 px-4 py-2 rounded-md text-sm hover:bg-indigo-50 transition-colors disabled:border-gray-300 disabled:text-gray-300 disabled:cursor-not-allowed"
          @click="handlePullModels"
        >
          {{ isPulling ? '拉取中...' : '一键拉取模型' }}
        </button>
      </div>
    </div>

    <!-- 模型列表 -->
    <div class="bg-white rounded-lg shadow p-6 space-y-6">
      <h2 class="text-lg font-semibold text-gray-800">可用模型</h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 文本模型 -->
        <div>
          <h3 class="text-sm font-medium text-gray-600 mb-2">文案理解模型（文本）</h3>
          <div v-if="settingsStore.textModels.length === 0" class="bg-gray-50 rounded-md p-4 text-center text-gray-400 text-sm">
            请先拉取模型列表
          </div>
          <div v-else class="border border-gray-200 rounded-md overflow-hidden">
            <table class="w-full text-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500">模型 ID</th>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500">提供者</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="model in settingsStore.textModels" :key="model.id">
                  <td class="px-3 py-2 text-gray-900">{{ model.id }}</td>
                  <td class="px-3 py-2 text-gray-500">{{ model.owned_by }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 图片模型 -->
        <div>
          <h3 class="text-sm font-medium text-gray-600 mb-2">图片生成模型</h3>
          <div v-if="settingsStore.imageModels.length === 0" class="bg-gray-50 rounded-md p-4 text-center text-gray-400 text-sm">
            请先拉取模型列表
          </div>
          <div v-else class="border border-gray-200 rounded-md overflow-hidden">
            <table class="w-full text-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500">模型 ID</th>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500">提供者</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="model in settingsStore.imageModels" :key="model.id">
                  <td class="px-3 py-2 text-gray-900">{{ model.id }}</td>
                  <td class="px-3 py-2 text-gray-500">{{ model.owned_by }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 默认模型选择 -->
      <div class="border-t pt-4">
        <h3 class="text-sm font-medium text-gray-600 mb-3">默认模型</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-gray-500 mb-1">默认文本模型</label>
            <select
              v-model="defaultTextModel"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              :disabled="settingsStore.textModels.length === 0"
            >
              <option v-if="settingsStore.textModels.length === 0" value="">暂无可选模型</option>
              <option v-for="model in settingsStore.textModels" :key="model.id" :value="model.id">
                {{ model.id }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs text-gray-500 mb-1">默认图片模型</label>
            <select
              v-model="defaultImageModel"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              :disabled="settingsStore.imageModels.length === 0"
            >
              <option v-if="settingsStore.imageModels.length === 0" value="">暂无可选模型</option>
              <option v-for="model in settingsStore.imageModels" :key="model.id" :value="model.id">
                {{ model.id }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
