/**
 * 文件名：api/settings.ts
 * 功能描述：API 设置相关接口封装。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [x] 实现 getSettings() — GET /settings
 * - [x] 实现 updateSettings(data) — PUT /settings
 * - [x] 实现 pullModels() — POST /settings/models/pull
 * - [x] 实现 getModels() — GET /settings/models
 */

import client from './client'

export interface ModelInfo {
  id: string
  owned_by: string
  category: 'text' | 'image' | 'other'
}

export interface ModelListResponse {
  text_models: ModelInfo[]
  image_models: ModelInfo[]
  other_models: ModelInfo[]
}

export interface APISettingsResponse {
  api_base_url: string
  api_key_masked: string
  default_text_model: string
  default_image_model: string
}

export interface APISettingsUpdate {
  api_base_url: string
  api_key: string
  default_text_model: string
  default_image_model: string
}

export async function getSettings(): Promise<APISettingsResponse> {
  const response = await client.get<APISettingsResponse>('/settings/')
  return response.data
}

export async function updateSettings(
  data: APISettingsUpdate
): Promise<{ success: boolean; message: string }> {
  const response = await client.put<{ success: boolean; message: string }>(
    '/settings/',
    data
  )
  return response.data
}

export async function pullModels(): Promise<ModelListResponse> {
  const response = await client.post<ModelListResponse>('/settings/models/pull')
  return response.data
}

export async function getModels(): Promise<ModelListResponse> {
  const response = await client.get<ModelListResponse>('/settings/models')
  return response.data
}
