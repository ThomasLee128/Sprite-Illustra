/**
 * 文件名：stores/settings.ts
 * 功能描述：API 设置状态管理。存储 API 配置和模型列表。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [x] 定义 state: apiBaseUrl, apiKeyMasked, defaultTextModel, defaultImageModel,
 *       textModels[], imageModels[], otherModels[], loading, error
 * - [x] 实现 action: fetchSettings() — 调用 api/settings.getSettings()
 * - [x] 实现 action: saveSettings(data) — 调用 api/settings.updateSettings()
 * - [x] 实现 action: pullModels() — 调用 api/settings.pullModels()，更新模型列表
 * - [x] 实现 action: fetchModels() — 调用 api/settings.getModels()
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSettings, updateSettings, pullModels, getModels, type ModelInfo, type APISettingsUpdate } from '../api/settings'

export const useSettingsStore = defineStore('settings', () => {
  const apiBaseUrl = ref('')
  const apiKeyMasked = ref('')
  const defaultTextModel = ref('')
  const defaultImageModel = ref('')
  const textModels = ref<ModelInfo[]>([])
  const imageModels = ref<ModelInfo[]>([])
  const otherModels = ref<ModelInfo[]>([])
  const loading = ref(false)
  const error = ref('')

  async function fetchSettings() {
    loading.value = true
    error.value = ''
    try {
      const data = await getSettings()
      apiBaseUrl.value = data.api_base_url
      apiKeyMasked.value = data.api_key_masked
      defaultTextModel.value = data.default_text_model
      defaultImageModel.value = data.default_image_model
    } catch (e: any) {
      error.value = e.message || '获取设置失败'
    } finally {
      loading.value = false
    }
  }

  async function saveSettings(data: APISettingsUpdate) {
    loading.value = true
    error.value = ''
    try {
      await updateSettings(data)
      await fetchSettings()
    } catch (e: any) {
      error.value = e.message || '保存设置失败'
    } finally {
      loading.value = false
    }
  }

  async function pullModelsFromAPI() {
    loading.value = true
    error.value = ''
    try {
      const data = await pullModels()
      textModels.value = data.text_models
      imageModels.value = data.image_models
      otherModels.value = data.other_models
    } catch (e: any) {
      error.value = e.message || '拉取模型列表失败'
    } finally {
      loading.value = false
    }
  }

  async function fetchModels() {
    loading.value = true
    error.value = ''
    try {
      const data = await getModels()
      textModels.value = data.text_models
      imageModels.value = data.image_models
      otherModels.value = data.other_models
    } catch (e: any) {
      error.value = e.message || '获取模型列表失败'
    } finally {
      loading.value = false
    }
  }

  return {
    apiBaseUrl,
    apiKeyMasked,
    defaultTextModel,
    defaultImageModel,
    textModels,
    imageModels,
    otherModels,
    loading,
    error,
    fetchSettings,
    saveSettings,
    pullModelsFromAPI,
    fetchModels,
  }
})
