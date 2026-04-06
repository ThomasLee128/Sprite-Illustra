/**
 * 文件名：api/sse.ts
 * 功能描述：SSE (Server-Sent Events) 连接封装。
 *          用于实时接收任务处理进度更新。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [x] 实现 connectSSE(taskId, onProgress, onComplete, onError)
 *       - 创建 EventSource 连接到 /api/tasks/{taskId}/sse
 *       - 监听 "progress" 事件，解析 JSON 后调用 onProgress(data)
 *       - 当 phase === "complete" 时调用 onComplete(data) 并关闭连接
 *       - 当 phase === "failed" 时调用 onError(data) 并关闭连接
 *       - 返回关闭函数 () => eventSource.close()
 *       - 建议使用 @vueuse/core 的 useEventSource 实现自动重连
 */

import type { TaskState } from './tasks'

export interface ProgressEvent {
  task_id: string
  phase: string
  progress: number
  message: string
  illustration_count: number
  completed_count: number
}

export function connectSSE(
  taskId: string,
  onProgress: (data: TaskState) => void,
  onComplete: (data: TaskState) => void,
  onError: (data: TaskState) => void,
  onPreview?: (data: TaskState) => void
): () => void {
  const eventSource = new EventSource(`/api/tasks/${taskId}/sse`)
  
  eventSource.addEventListener('message', (event) => {
    try {
      const data = JSON.parse(event.data) as TaskState
      onProgress(data)
      
      if (data.phase === 'complete') {
        onComplete(data)
        eventSource.close()
      } else if (data.phase === 'failed') {
        onError(data)
        eventSource.close()
      } else if (data.phase === 'preview' && onPreview) {
        // 预览阶段，关闭 SSE 连接
        onPreview(data)
        eventSource.close()
      }
    } catch (e) {
      console.error('Failed to parse SSE message:', e)
    }
  })
  
  eventSource.onerror = (error) => {
    console.error('SSE connection error:', error)
    eventSource.close()
  }
  
  return () => {
    eventSource.close()
  }
}
