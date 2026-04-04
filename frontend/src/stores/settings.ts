/**
 * 文件名：stores/settings.ts
 * 功能描述：API 设置状态管理。存储 API 配置和模型列表。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [ ] 定义 state: apiBaseUrl, apiKeyMasked, defaultTextModel, defaultImageModel,
 *       textModels[], imageModels[], otherModels[], loading, error
 * - [ ] 实现 action: fetchSettings() — 调用 api/settings.getSettings()
 * - [ ] 实现 action: saveSettings(data) — 调用 api/settings.updateSettings()
 * - [ ] 实现 action: pullModels() — 调用 api/settings.pullModels()，更新模型列表
 * - [ ] 实现 action: fetchModels() — 调用 api/settings.getModels()
 */

import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    apiBaseUrl: '',
    apiKeyMasked: '',
    defaultTextModel: '',
    defaultImageModel: '',
    textModels: [] as Array<{ id: string; owned_by: string }>,
    imageModels: [] as Array<{ id: string; owned_by: string }>,
    loading: false,
    error: '',
  }),
  actions: {
    // TODO: 实现上述 actions
  },
})
