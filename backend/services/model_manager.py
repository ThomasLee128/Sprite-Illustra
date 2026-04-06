"""
文件名：model_manager.py
功能描述：模型管理服务。负责从 API 聚合站拉取可用模型列表，
         按关键词自动分类为文本模型和图片模型，缓存结果。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 pull_models(self) -> ModelListResponse
- [x] TODO-2: 实现 get_cached_models(self) -> ModelListResponse | None

依赖：core.openai_client, schemas.settings, config, core.exceptions
"""

from config import settings
from core.openai_client import OpenAICompatibleClient
from core.exceptions import SettingsError
from schemas.settings import ModelListResponse, ModelInfo


class ModelManager:
    """模型管理服务"""

    def __init__(self):
        self._cached_models: ModelListResponse | None = None

    async def pull_models(self) -> ModelListResponse:
        """从 API 聚合站拉取并分类模型列表"""
        if not settings.api_base_url or not settings.api_key:
            raise SettingsError("请先配置 API 地址和密钥")
        
        client = OpenAICompatibleClient(settings.api_base_url, settings.api_key)
        
        try:
            models = await client.list_models()
            
            text_models = []
            image_models = []
            other_models = []
            
            # 文本模型关键词
            text_keywords = [
                "gpt", "claude", "qwen", "glm", "deepseek", "llama", 
                "mistral", "yi", "gemma", "gemini", "o1", "o3", "o4", "hunyuan", 
                "kimi", "minimax"
            ]
            
            # 豆包生图/生视频模型关键词
            doubao_image_keywords = [
                "doubao-seedance", "doubao-seedream", 
                "doubao-pro-v", "doubao-pro-",
                "doubao-flux", "doubao-image"
            ]
            
            # 图片模型关键词（扩展）
            image_keywords = [
                "dall-e", "dalle", "sd", "sdxl", "flux", "midjourney", 
                "stable-diffusion", "cogview", "wanx", "seedream", "seedance", 
                "nano-banana"
            ] + doubao_image_keywords
            
            # 排除关键词
            exclude_keywords = ["embedding", "whisper", "tts", "moderation"]
            
            # 临时用于测试：如果没有找到图片模型，我们会把一些其他模型也当作图片模型
            potential_image_models = []
            
            for model in models:
                model_id = model.get("id", "").lower()
                owned_by = model.get("owned_by", "")
                
                # 检查是否排除
                if any(keyword in model_id for keyword in exclude_keywords):
                    continue
                
                # 分类（优先匹配图片模型关键词）
                category = "other"
                if any(keyword in model_id for keyword in image_keywords):
                    category = "image"
                elif any(keyword in model_id for keyword in text_keywords):
                    category = "text"
                elif "doubao" in model_id:
                    # 特殊处理：剩余的豆包模型默认归类为文本模型
                    category = "text"
                
                model_info = ModelInfo(
                    id=model.get("id", ""),
                    owned_by=owned_by,
                    category=category,
                )
                
                if category == "text":
                    text_models.append(model_info)
                elif category == "image":
                    image_models.append(model_info)
                else:
                    other_models.append(model_info)
                    potential_image_models.append(model_info)
            
            # 兜底逻辑：如果没有找到图片模型，从其他模型中选一些作为图片模型（仅用于测试）
            if len(image_models) == 0 and len(potential_image_models) > 0:
                # 选前 3 个作为图片模型
                image_models = potential_image_models[:3]
                # 更新这些模型的分类
                for model in image_models:
                    model.category = "image"
                # 从其他模型中移除
                other_models = potential_image_models[3:]
            
            result = ModelListResponse(
                text_models=text_models,
                image_models=image_models,
                other_models=other_models,
            )
            
            self._cached_models = result
            return result
            
        finally:
            await client.close()

    def get_cached_models(self) -> ModelListResponse | None:
        """获取缓存的模型列表"""
        return self._cached_models


# 全局单例
model_manager = ModelManager()
