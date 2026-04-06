/**
 * 文件名：stores/task.ts
 * 功能描述：任务进度状态管理。通过 SSE 接收实时进度并更新。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [x] 定义 state: taskId, phase, progress (0~1), message,
 *       illustrationCount, completedCount, errorMessage, isConnected
 * - [x] 实现 action: startProcessing(taskId, textModel, imageModel, style)
 *       — 调用 startTask API，然后建立 SSE 连接
 * - [x] 实现 action: connectSSE(taskId)
 *       — 使用 api/sse.connectSSE，回调中更新 state
 *       — phase === "complete" 时路由跳转到 /preview/{taskId}
 * - [x] 实现 action: disconnect() — 关闭 SSE 连接
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { startTask, getTaskStatus } from '../api/tasks'
import type { TaskState } from '../api/tasks'
import { connectSSE } from '../api/sse'

export const useTaskStore = defineStore('task', () => {
  const router = useRouter()
  
  const taskId = ref('')
  const phase = ref('')
  const progress = ref(0)
  const message = ref('')
  const illustrationCount = ref(0)
  const completedCount = ref(0)
  const errorMessage = ref('')
  const isConnected = ref(false)
  const textModel = ref('')
  const imageModel = ref('')
  const style = ref('')
  let disconnectFn: (() => void) | null = null

  function updateStateFromTaskState(data: TaskState) {
    taskId.value = data.task_id
    phase.value = data.phase
    progress.value = data.progress
    message.value = data.message
    illustrationCount.value = data.illustration_count
    completedCount.value = data.completed_count
    if (data.error_message) {
      errorMessage.value = data.error_message
    }
  }

  async function startProcessing(
    taskIdVal: string,
    textModelVal: string,
    imageModelVal: string,
    styleVal: string,
    isPPTModeVal: boolean = false
  ) {
    taskId.value = taskIdVal
    textModel.value = textModelVal
    imageModel.value = imageModelVal
    style.value = styleVal
    errorMessage.value = ''
    try {
      await startTask(taskIdVal, { 
        text_model: textModelVal, 
        image_model: imageModelVal, 
        style: styleVal,
        is_ppt_mode: isPPTModeVal
      })
      await connectToSSE(taskIdVal)
    } catch (e: any) {
      errorMessage.value = e.message || '启动任务失败'
    }
  }

  async function connectToSSE(taskIdVal: string, onPreviewCallback?: () => void) {
    isConnected.value = true
    
    disconnectFn = connectSSE(
      taskIdVal,
      (data) => {
        updateStateFromTaskState(data)
      },
      (data) => {
        updateStateFromTaskState(data)
        isConnected.value = false
        router.push(`/preview/${data.task_id}`)
      },
      (data) => {
        updateStateFromTaskState(data)
        isConnected.value = false
        errorMessage.value = data.error_message || '任务处理失败'
      },
      (data) => {
        updateStateFromTaskState(data)
        isConnected.value = false
        if (onPreviewCallback) {
          onPreviewCallback()
        }
      }
    )
  }

  async function fetchTaskStatus(taskIdVal: string) {
    try {
      const data = await getTaskStatus(taskIdVal)
      updateStateFromTaskState(data)
    } catch (e: any) {
      errorMessage.value = e.message || '获取任务状态失败'
    }
  }

  function disconnect() {
    if (disconnectFn) {
      disconnectFn()
      disconnectFn = null
    }
    isConnected.value = false
  }

  function reset() {
    disconnect()
    taskId.value = ''
    phase.value = ''
    progress.value = 0
    message.value = ''
    illustrationCount.value = 0
    completedCount.value = 0
    errorMessage.value = ''
    textModel.value = ''
    imageModel.value = ''
    style.value = ''
  }

  return {
    taskId,
    phase,
    progress,
    message,
    illustrationCount,
    completedCount,
    errorMessage,
    isConnected,
    textModel,
    imageModel,
    style,
    startProcessing,
    connectToSSE,
    fetchTaskStatus,
    disconnect,
    reset,
  }
})
