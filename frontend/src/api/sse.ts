/**
 * 文件名：api/sse.ts
 * 功能描述：SSE (Server-Sent Events) 连接封装。
 *          用于实时接收任务处理进度更新。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [ ] 实现 connectSSE(taskId, onProgress, onComplete, onError)
 *       - 创建 EventSource 连接到 /api/tasks/{taskId}/sse
 *       - 监听 "progress" 事件，解析 JSON 后调用 onProgress(data)
 *       - 当 phase === "complete" 时调用 onComplete(data) 并关闭连接
 *       - 当 phase === "failed" 时调用 onError(data) 并关闭连接
 *       - 返回关闭函数 () => eventSource.close()
 *       - 建议使用 @vueuse/core 的 useEventSource 实现自动重连
 */

export {}
