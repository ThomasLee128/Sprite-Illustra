/**
 * 文件名：stores/document.ts
 * 功能描述：文档处理状态管理。存储上传状态和处理结果。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [ ] 定义 state: currentTaskId, filename, sourceFormat,
 *       illustratedDocument (处理结果), uploading, error
 * - [ ] 实现 action: uploadDocument(file: File) — 上传文件，设置 taskId
 * - [ ] 实现 action: fetchResult(taskId) — 获取处理结果
 * - [ ] 实现 action: removeIllustration(illustrationId) — 删除插图
 * - [ ] 实现 action: regenerateIllustration(illustrationId, prompt?) — 重新生成
 */

import { defineStore } from 'pinia'

export const useDocumentStore = defineStore('document', {
  state: () => ({
    currentTaskId: '',
    filename: '',
    sourceFormat: '',
    illustratedDocument: null as any,
    uploading: false,
    error: '',
  }),
  actions: {
    // TODO: 实现上述 actions
  },
})
