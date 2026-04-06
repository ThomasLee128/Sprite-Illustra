/**
 * 文件名：api/export.ts
 * 功能描述：文档导出 API 调用封装。
 * 作者：Trea
 * 创建时间：2026-04-04
 */

import client from './client'

export type ExportFormat = 'md' | 'docx' | 'html' | 'pdf'

export interface ExportRequest {
  task_id: string
  format: ExportFormat
}

export interface ExportResponse {
  export_id: string
  format: ExportFormat
  filename: string
}

export async function exportDocument(
  taskId: string,
  format: ExportFormat
): Promise<ExportResponse> {
  const response = await client.post('/export/', { task_id: taskId, format })
  return response.data
}

export async function downloadExport(exportId: string): Promise<Blob> {
  const response = await client.get(`/export/${exportId}/download`, {
    responseType: 'blob',
  })
  return response.data
}

export function downloadFile(blob: Blob, filename: string) {
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}
