/**
 * 文件名：stores/task.ts
 * 功能描述：任务进度状态管理。通过 SSE 接收实时进度并更新。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [ ] 定义 state: taskId, phase, progress (0~1), message,
 *       illustrationCount, completedCount, errorMessage, isConnected
 * - [ ] 实现 action: startProcessing(taskId, textModel, imageModel, style)
 *       — 调用 startTask API，然后建立 SSE 连接
 * - [ ] 实现 action: connectSSE(taskId)
 *       — 使用 api/sse.connectSSE，回调中更新 state
 *       — phase === "complete" 时路由跳转到 /preview/{taskId}
 * - [ ] 实现 action: disconnect() — 关闭 SSE 连接
 */

import { defineStore } from 'pinia'

export const useTaskStore = defineStore('task', {
  state: () => ({
    taskId: '',
    phase: '',
    progress: 0,
    message: '',
    illustrationCount: 0,
    completedCount: 0,
    errorMessage: '',
    isConnected: false,
  }),
  actions: {
    // TODO: 实现上述 actions
  },
})
