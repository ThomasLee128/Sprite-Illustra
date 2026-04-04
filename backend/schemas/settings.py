"""
文件名：settings.py
功能描述：API 设置相关数据模型。定义配置请求/响应格式、模型信息等。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 核心数据模型已完成
"""

from pydantic import BaseModel, Field


class APISettingsUpdate(BaseModel):
    """更新 API 设置的请求体"""
    api_base_url: str = Field(description="API 聚合站 URL，如 https://api.spiritgpu.com")
    api_key: str = Field(description="API 聚合站密钥")
    default_text_model: str = Field(default="", description="默认文本模型 ID")
    default_image_model: str = Field(default="", description="默认图片模型 ID")


class APISettingsResponse(BaseModel):
    """返回给前端的配置信息（Key 脱敏）"""
    api_base_url: str = Field(default="")
    api_key_masked: str = Field(default="", description="脱敏后的 Key，如 sk-***abc")
    default_text_model: str = Field(default="")
    default_image_model: str = Field(default="")


class ModelInfo(BaseModel):
    """单个模型信息"""
    id: str = Field(description="模型 ID")
    owned_by: str = Field(default="", description="模型提供者")
    category: str = Field(default="other", description="分类: text / image / other")


class ModelListResponse(BaseModel):
    """模型列表响应"""
    text_models: list[ModelInfo] = Field(default_factory=list, description="文本理解模型列表")
    image_models: list[ModelInfo] = Field(default_factory=list, description="图片生成模型列表")
    other_models: list[ModelInfo] = Field(default_factory=list, description="未分类模型列表")
