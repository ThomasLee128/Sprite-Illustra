"""
文件名：openai_client.py
功能描述：OpenAI 兼容 API 客户端封装。
         统一封装文本补全（chat/completions）、图片生成（images/generations）、
         模型列表（models）三个接口。运行时从 config 读取 API URL 和 Key。
         支持 New API / One API 等 OpenAI 兼容聚合服务。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 __init__(self, base_url: str, api_key: str)
      - 初始化 httpx.AsyncClient 实例
      - 设置 base_url（确保末尾无斜杠）
      - 设置默认 headers: Authorization: Bearer {api_key}, Content-Type: application/json
      - 设置超时: 连接超时 10s，读取超时 120s（图片生成耗时较长）
      - 设置重试策略: 最多重试 2 次，仅对 5xx 和超时重试

- [ ] TODO-2: 实现 async chat_completion(self, model, messages, response_format=None) -> dict
      - POST {base_url}/v1/chat/completions
      - 请求体: {"model": model, "messages": messages, "response_format": response_format}
      - response_format 为可选参数，用于要求模型返回 JSON（如 {"type": "json_object"}）
      - 返回 response["choices"][0]["message"]["content"]
      - 异常处理: HTTP 401 -> raise SettingsError("API Key 无效")
      -          HTTP 429 -> raise APIClientError("API 请求频率超限，请稍后重试")
      -          HTTP 5xx -> raise APIClientError(f"API 服务端错误: {status_code}")
      -          超时    -> raise APIClientError("API 请求超时")

- [ ] TODO-3: 实现 async image_generation(self, model, prompt, size="1024x1024", n=1) -> list[str]
      - POST {base_url}/v1/images/generations
      - 请求体: {"model": model, "prompt": prompt, "size": size, "n": n}
      - 兼容两种返回格式:
        - 如果 data[i] 含 "b64_json" 字段: base64 解码后保存为图片，返回本地路径列表
        - 如果 data[i] 含 "url" 字段: 下载图片保存到本地，返回本地路径列表
      - 图片保存路径: config.DATA_DIR / "images" / "{uuid}.png"
      - 异常处理同 TODO-2

- [ ] TODO-4: 实现 async list_models(self) -> list[dict]
      - GET {base_url}/v1/models
      - 返回 response["data"]，每个元素至少包含 {"id": "...", "owned_by": "..."}
      - 异常处理同 TODO-2

- [ ] TODO-5: 实现 async close(self)
      - 关闭 httpx.AsyncClient 连接

依赖：httpx, config.settings, core.exceptions, uuid, base64, pathlib
"""


class OpenAICompatibleClient:
    """OpenAI 兼容 API 客户端"""

    def __init__(self, base_url: str, api_key: str):
        # TODO-1: 初始化 httpx.AsyncClient
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = None  # TODO: 初始化 httpx.AsyncClient

    async def chat_completion(
        self, model: str, messages: list[dict], response_format: dict | None = None
    ) -> str:
        """调用文本补全接口，返回模型回复文本"""
        # TODO-2
        raise NotImplementedError("待 Trea 实现")

    async def image_generation(
        self, model: str, prompt: str, size: str = "1024x1024", n: int = 1
    ) -> list[str]:
        """调用图片生成接口，返回本地图片路径列表"""
        # TODO-3
        raise NotImplementedError("待 Trea 实现")

    async def list_models(self) -> list[dict]:
        """获取可用模型列表"""
        # TODO-4
        raise NotImplementedError("待 Trea 实现")

    async def close(self):
        """关闭 HTTP 客户端连接"""
        # TODO-5
        if self._client:
            await self._client.aclose()
