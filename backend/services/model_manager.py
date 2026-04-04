"""
文件名：model_manager.py
功能描述：模型管理服务。负责从 API 聚合站拉取可用模型列表，
         按关键词自动分类为文本模型和图片模型，缓存结果。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 pull_models(self) -> ModelListResponse
      - 从 config 读取 api_base_url 和 api_key
      - 如果未配置 -> raise SettingsError
      - 实例化 OpenAICompatibleClient，调用 list_models()
      - 对每个模型按 id 关键词分类:
        * 文本模型关键词: gpt, claude, qwen, glm, deepseek, llama, mistral, yi, gemma, gemini, o1, o3, o4
        * 图片模型关键词: dall-e, dalle, sd, sdxl, flux, midjourney, stable-diffusion, cogview, wanx
        * 排除关键词（这些不是独立模型）: embedding, whisper, tts, moderation
        * 其他 -> other_models
      - 构建 ModelListResponse 并缓存到 self._cached_models
      - 关闭 client 连接
      - 返回 ModelListResponse

- [ ] TODO-2: 实现 get_cached_models(self) -> ModelListResponse | None
      - 返回缓存的模型列表（如果有），否则返回 None

依赖：core.openai_client, schemas.settings, config, core.exceptions
"""

from schemas.settings import ModelListResponse, ModelInfo
from core.exceptions import SettingsError


class ModelManager:
    """模型管理服务"""

    def __init__(self):
        self._cached_models: ModelListResponse | None = None

    async def pull_models(self) -> ModelListResponse:
        """从 API 聚合站拉取并分类模型列表"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")

    def get_cached_models(self) -> ModelListResponse | None:
        """获取缓存的模型列表"""
        # TODO-2
        return self._cached_models


# 全局单例
model_manager = ModelManager()
