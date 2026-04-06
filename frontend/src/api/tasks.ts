/**
 * 文件名：api/tasks.ts
 * 功能描述：任务相关 API 调用封装。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [x] 实现 startTask(taskId, { text_model, image_model, style }) — POST /tasks/{taskId}/start
 * - [x] 实现 getTaskStatus(taskId) — GET /tasks/{taskId}
 * - [x] 实现 getTaskResult(taskId) — GET /tasks/{taskId}/result
 * - [x] 实现 removeIllustration(taskId, illustrationId) — DELETE /tasks/{taskId}/illustrations/{id}
 * - [x] 实现 regenerateIllustration(taskId, illustrationId, prompt?) — POST .../regenerate
 * - [x] 实现 moveIllustration(taskId, illustrationId, afterSectionId) — PUT .../move
 */

import client from './client'

export interface TaskStartRequest {
  text_model: string
  image_model: string
  style: string
  is_ppt_mode?: boolean
}

export interface TaskState {
  task_id: string
  filename: string
  source_format: string
  phase: 'uploaded' | 'parsing' | 'analyzing' | 'preview' | 'generating' | 'complete' | 'failed'
  progress: number
  message: string
  text_model?: string
  image_model?: string
  illustration_count: number
  completed_count: number
  error_message?: string
}

export interface DocumentSection {
  id: string
  type: 'heading' | 'paragraph' | 'list' | 'code' | 'blockquote'
  level: number
  content: string
  position: number
}

export interface IllustrationItem {
  id: string
  after_section_id: string
  prompt: string
  style: string
  description_cn: string
  reason: string
  image_path?: string
  status: 'pending' | 'generating' | 'done' | 'failed'
  error_message?: string
}

export interface DocumentMetadata {
  title: string
  author: string
  word_count: number
}

export interface Document {
  filename: string
  source_format: string
  sections: DocumentSection[]
  metadata: DocumentMetadata
}

export interface IllustratedDocument {
  document: Document
  illustrations: IllustrationItem[]
}

export async function startTask(
  taskId: string,
  data: TaskStartRequest
): Promise<{ task_id: string; message: string }> {
  const response = await client.post<{ task_id: string; message: string }>(
    `/tasks/${taskId}/start`,
    data
  )
  return response.data
}

export async function getTaskStatus(taskId: string): Promise<TaskState> {
  const response = await client.get<TaskState>(`/tasks/${taskId}`)
  return response.data
}

export async function getTaskResult(taskId: string): Promise<IllustratedDocument> {
  const response = await client.get<IllustratedDocument>(`/tasks/${taskId}/result`)
  return response.data
}

export async function removeIllustration(
  taskId: string,
  illustrationId: string
): Promise<{ success: boolean; message: string }> {
  const response = await client.delete<{ success: boolean; message: string }>(
    `/tasks/${taskId}/illustrations/${illustrationId}`
  )
  return response.data
}

export interface RegenerateRequest {
  prompt?: string
}

export async function regenerateIllustration(
  taskId: string,
  illustrationId: string,
  data?: RegenerateRequest
): Promise<{ success: boolean; message: string }> {
  const response = await client.post<{ success: boolean; message: string }>(
    `/tasks/${taskId}/illustrations/${illustrationId}/regenerate`,
    data || {}
  )
  return response.data
}

export interface MoveRequest {
  after_section_id: string
}

export async function moveIllustration(
  taskId: string,
  illustrationId: string,
  data: MoveRequest
): Promise<{ success: boolean; message: string }> {
  const response = await client.put<{ success: boolean; message: string }>(
    `/tasks/${taskId}/illustrations/${illustrationId}/move`,
    data
  )
  return response.data
}

export interface PreviewData {
  document: Document
  illustrations: IllustrationItem[]
}

export async function getPreview(taskId: string): Promise<PreviewData> {
  const response = await client.get<PreviewData>(`/tasks/${taskId}/preview`)
  return response.data
}

export interface ConfirmPreviewRequest {
  image_model: string
}

export async function confirmPreview(
  taskId: string,
  data: ConfirmPreviewRequest
): Promise<{ success: boolean; message: string }> {
  const response = await client.post<{ success: boolean; message: string }>(
    `/tasks/${taskId}/preview/confirm`,
    data
  )
  return response.data
}
