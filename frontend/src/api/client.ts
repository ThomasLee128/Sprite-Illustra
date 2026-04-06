/**
 * 文件名：api/client.ts
 * 功能描述：Axios 实例配置。统一设置 baseURL、超时、拦截器。
 * 作者：Claude Code
 * 创建时间：2026-04-04
 * 后续开发：Trea
 * TODO：
 * - [ ] 添加请求拦截器（如需要 token 认证）
 * - [ ] 添加响应拦截器（统一错误处理、toast 提示）
 */

import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 120000, // 图片生成可能较慢
  headers: {
    'Content-Type': 'application/json',
  },
})

// 添加响应拦截器，处理错误响应
client.interceptors.response.use(
  (response) => response,
  (error) => {
    // 如果后端返回了错误信息，提取并抛出
    if (error.response && error.response.data && error.response.data.error) {
      throw new Error(error.response.data.error)
    }
    throw error
  }
)

export default client
