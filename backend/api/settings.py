"""
文件名：settings.py
功能描述：API 设置管理的路由。提供配置读写和模型列表拉取功能。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 GET / 端点
- [x] TODO-2: 实现 PUT / 端点
- [x] TODO-3: 实现 POST /models/pull 端点
- [x] TODO-4: 实现 GET /models 端点

依赖：fastapi, schemas.settings, services.model_manager, config
"""

from fastapi import APIRouter

import config
from schemas.settings import APISettingsUpdate, APISettingsResponse, ModelListResponse
from services.model_manager import model_manager

router = APIRouter()


@router.get("/", response_model=APISettingsResponse)
async def get_settings():
    """获取当前 API 设置"""
    # API Key 脱敏
    api_key = config.settings.api_key
    masked_key = ""
    if api_key:
        if len(api_key) > 6:
            masked_key = f"{api_key[:3]}***{api_key[-3:]}"
        else:
            masked_key = "***"
    
    return APISettingsResponse(
        api_base_url=config.settings.api_base_url,
        api_key_masked=masked_key,
        default_text_model=config.settings.default_text_model,
        default_image_model=config.settings.default_image_model,
    )


@router.put("/")
async def update_settings(request: APISettingsUpdate):
    """保存 API 设置"""
    # 保存配置
    data_to_save = {
        "api_base_url": request.api_base_url,
        "api_key": request.api_key,
        "default_text_model": request.default_text_model,
        "default_image_model": request.default_image_model,
    }
    config.save_settings(data_to_save)
    
    # 重新加载配置
    import importlib
    importlib.reload(config)
    from config import settings as new_settings
    config.settings = new_settings
    
    return {"success": True, "message": "设置已保存"}


@router.post("/models/pull", response_model=ModelListResponse)
async def pull_models():
    """从聚合站拉取可用模型列表"""
    return await model_manager.pull_models()


@router.get("/models", response_model=ModelListResponse)
async def get_models():
    """获取已缓存的模型列表"""
    cached = model_manager.get_cached_models()
    if cached:
        return cached
    return ModelListResponse()
