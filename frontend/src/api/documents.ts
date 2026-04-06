/**
 * 文件名：api/documents.ts
 * 功能描述：文档相关 API 调用封装。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [x] 实现 uploadDocument(file: File) — POST /documents/upload (FormData)
 *       返回 { task_id, filename, format }
 */

import client from './client'

export interface UploadResponse {
  task_id: string
  filename: string
  format: string
}

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await client.post<UploadResponse>('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}
