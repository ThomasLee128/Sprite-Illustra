"""
文件名：settings.py
功能描述：API 设置管理的路由。提供配置读写和模型列表拉取功能。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 GET / 端点
      - 从 config 读取当前设置
      - API Key 脱敏: 如 "sk-abc123def456" -> "sk-***456"（保留前3位和后3位）
      - 返回 APISettingsResponse

- [ ] TODO-2: 实现 PUT / 端点
      - 接收 APISettingsUpdate 请求体
      - 调用 config.save_settings() 持久化到 settings.json
      - 重新加载全局 config（更新 settings 单例）
      - 返回 {"success": true, "message": "设置已保存"}

- [ ] TODO-3: 实现 POST /models/pull 端点
      - 调用 model_manager.pull_models()
      - 返回 ModelListResponse

- [ ] TODO-4: 实现 GET /models 端点
      - 调用 model_manager.get_cached_models()
      - 如果无缓存，返回空的 ModelListResponse
      - 如果有缓存，返回缓存的 ModelListResponse

依赖：fastapi, schemas.settings, services.model_manager, config
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_settings():
    """获取当前 API 设置"""
    # TODO-1
    raise NotImplementedError("待 Trea 实现")


@router.put("/")
async def update_settings():
    """保存 API 设置"""
    # TODO-2
    raise NotImplementedError("待 Trea 实现")


@router.post("/models/pull")
async def pull_models():
    """从聚合站拉取可用模型列表"""
    # TODO-3
    raise NotImplementedError("待 Trea 实现")


@router.get("/models")
async def get_models():
    """获取已缓存的模型列表"""
    # TODO-4
    raise NotImplementedError("待 Trea 实现")
