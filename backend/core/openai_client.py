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
- [x] TODO-1: 实现 __init__(self, base_url: str, api_key: str)
- [x] TODO-2: 实现 async chat_completion(self, model, messages, response_format=None) -> dict
- [x] TODO-3: 实现 async image_generation(self, model, prompt, size="1024x1024", n=1) -> list[str]
- [x] TODO-4: 实现 async list_models(self) -> list[dict]
- [x] TODO-5: 实现 async close(self)

依赖：httpx, config.settings, core.exceptions, uuid, base64, pathlib
"""

import uuid
import base64
import httpx
from pathlib import Path
from typing import Any

from config import settings, DATA_DIR
from core.exceptions import APIClientError, SettingsError


class OpenAICompatibleClient:
    """OpenAI 兼容 API 客户端"""

    def __init__(self, base_url: str, api_key: str):
        # 智能处理 URL，确保只保留基础部分
        self.base_url = self._normalize_base_url(base_url)
        self.api_key = api_key
        
        # 初始化 httpx.AsyncClient
        timeout = httpx.Timeout(connect=10.0, read=120.0, write=60.0, pool=60.0)
        transport = httpx.AsyncHTTPTransport(retries=2)
        
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
            transport=transport,
        )
    
    def _normalize_base_url(self, url: str) -> str:
        """规范化基础 URL，移除 /v1 或具体接口路径"""
        url = url.rstrip("/")
        
        # 如果包含 /v1，只保留到 /v1 之前的部分
        if "/v1" in url:
            # 找到 /v1 的位置，保留到那里
            idx = url.find("/v1")
            url = url[:idx]
        
        # 如果包含具体接口路径（如 /chat/completions 等），只保留域名部分
        # 通过计算 / 的数量来判断
        parts = url.split("/")
        # 至少有协议（https://）和域名，最多可能有路径
        # 我们只保留协议 + 域名 + 可选的 /v1（如果用户已经添加了）
        if len(parts) > 3:
            # 超过 3 个部分（协议、空、域名）说明有额外路径
            url = "/".join(parts[:3])
        
        return url

    async def chat_completion(
        self, model: str, messages: list[dict], response_format: dict | None = None
    ) -> str:
        """调用文本补全接口，返回模型回复文本"""
        try:
            payload = {
                "model": model,
                "messages": messages,
            }
            if response_format:
                payload["response_format"] = response_format
            
            response = await self._client.post("/v1/chat/completions", json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise SettingsError("API Key 无效")
            elif e.response.status_code == 429:
                raise APIClientError("API 请求频率超限，请稍后重试")
            elif e.response.status_code >= 500:
                raise APIClientError(f"API 服务端错误: {e.response.status_code}")
            raise APIClientError(f"API 请求失败: {str(e)}")
        except httpx.TimeoutException:
            raise APIClientError("API 请求超时")
        except Exception as e:
            raise APIClientError(f"API 调用异常: {str(e)}")

    async def image_generation(
        self, model: str, prompt: str, size: str = "1024x1024", n: int = 1
    ) -> list[str]:
        """调用图片生成接口，返回本地图片路径列表。
        支持两种格式：
        1. OpenAI 格式: /v1/images/generations
        2. Gemini 格式: /v1beta/models/{model}:generateContent
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            result = None
            image_paths = []
            
            # 先尝试 OpenAI 格式
            try:
                logger.info(f"[OpenAI 客户端] 尝试 OpenAI 格式图片生成，模型: {model}")
                openai_payload = {
                    "model": model,
                    "prompt": prompt,
                    "size": size,
                    "n": n,
                }
                
                response = await self._client.post("/v1/images/generations", json=openai_payload)
                response.raise_for_status()
                result = response.json()
                logger.info(f"[OpenAI 客户端] OpenAI 格式成功！")
            except (httpx.HTTPStatusError, Exception) as e:
                logger.warning(f"[OpenAI 客户端] OpenAI 格式失败: {e}，尝试 Gemini 格式")
                # OpenAI 格式失败，尝试 Gemini 格式
                gemini_payload = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }
                
                gemini_url = f"/v1beta/models/{model}:generateContent"
                logger.info(f"[OpenAI 客户端] 调用 Gemini 格式: {gemini_url}")
                logger.info(f"[OpenAI 客户端] 请求 Payload: {gemini_payload}")
                
                response = await self._client.post(gemini_url, json=gemini_payload)
                response.raise_for_status()
                result = response.json()
                logger.info(f"[OpenAI 客户端] Gemini 格式响应: {result}")
            
            images_dir = DATA_DIR / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            
            if result:
                logger.info(f"[OpenAI 客户端] 开始解析返回结果...")
                
                # 解析结果
                if "data" in result:
                    # OpenAI 格式结果
                    logger.info(f"[OpenAI 客户端] 识别为 OpenAI 格式")
                    for item in result["data"]:
                        image_id = str(uuid.uuid4())
                        image_path = images_dir / f"{image_id}.png"
                        
                        if "b64_json" in item:
                            # Base64 编码的图片
                            image_data = base64.b64decode(item["b64_json"])
                            with open(image_path, "wb") as f:
                                f.write(image_data)
                        elif "url" in item:
                            # URL 下载
                            image_response = await self._client.get(item["url"])
                            image_response.raise_for_status()
                            with open(image_path, "wb") as f:
                                f.write(image_response.content)
                        
                        # 返回完整路径，用于Word导出器等后端处理
                        image_paths.append(str(image_path))
                        logger.info(f"[OpenAI 客户端] 图片已保存: {image_path}")
                elif "candidates" in result:
                    # Gemini 格式结果
                    logger.info(f"[OpenAI 客户端] 识别为 Gemini 格式")
                    
                    for candidate in result.get("candidates", []):
                        if "content" in candidate and "parts" in candidate["content"]:
                            for part in candidate["content"]["parts"]:
                                if "inlineData" in part:
                                    # 找到 inlineData（注意是大写 D）
                                    inline_data = part["inlineData"]
                                    if "data" in inline_data:
                                        # 是 Base64 编码的图片
                                        image_id = str(uuid.uuid4())
                                        image_path = images_dir / f"{image_id}.png"
                                        
                                        # 检查 mimeType 判断扩展名
                                        mime_type = inline_data.get("mimeType", "image/png")
                                        if mime_type == "image/jpeg":
                                            image_path = images_dir / f"{image_id}.jpg"
                                        
                                        logger.info(f"[OpenAI 客户端] 解码图片，mimeType: {mime_type}")
                                        
                                        image_data = base64.b64decode(inline_data["data"])
                                        with open(image_path, "wb") as f:
                                            f.write(image_data)
                                        
                                        image_paths.append(str(image_path))
                                        logger.info(f"[OpenAI 客户端] 图片已保存: {image_path}")
                                elif "text" in part:
                                    logger.debug(f"[OpenAI 客户端] 跳过 text 部分")
                                    continue
            
            logger.info(f"[OpenAI 客户端] 返回图片路径: {image_paths}")
            return image_paths
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise SettingsError("API Key 无效")
            elif e.response.status_code == 429:
                raise APIClientError("API 请求频率超限，请稍后重试")
            elif e.response.status_code >= 500:
                raise APIClientError(f"API 服务端错误: {e.response.status_code}")
            raise APIClientError(f"API 请求失败: {str(e)}")
        except httpx.TimeoutException:
            raise APIClientError("API 请求超时")
        except Exception as e:
            raise APIClientError(f"API 调用异常: {str(e)}")

    async def list_models(self) -> list[dict]:
        """获取可用模型列表"""
        try:
            response = await self._client.get("/v1/models")
            response.raise_for_status()
            
            result = response.json()
            return result["data"]
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise SettingsError("API Key 无效")
            elif e.response.status_code == 429:
                raise APIClientError("API 请求频率超限，请稍后重试")
            elif e.response.status_code >= 500:
                raise APIClientError(f"API 服务端错误: {e.response.status_code}")
            raise APIClientError(f"API 请求失败: {str(e)}")
        except httpx.TimeoutException:
            raise APIClientError("API 请求超时")
        except Exception as e:
            raise APIClientError(f"API 调用异常: {str(e)}")

    async def close(self):
        """关闭 HTTP 客户端连接"""
        if self._client:
            await self._client.aclose()
