"""
文件名：config.py
功能描述：全局配置管理，使用 Pydantic Settings 从环境变量和 JSON 文件加载配置。
         提供 API 聚合站 URL/Key、默认模型、服务器参数、文件存储路径等配置项。
         支持运行时通过 Web 设置页面修改配置并持久化到 settings.json。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 基础配置类已完成
- [ ] 如需加密存储 API Key，可在此扩展加密/解密逻辑
"""

import json
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


# 项目根目录（backend/ 的父目录）
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SETTINGS_FILE = BASE_DIR / "settings.json"


class Settings(BaseSettings):
    """应用全局配置"""

    # --- 服务器配置 ---
    host: str = Field(default="0.0.0.0", description="服务器监听地址")
    port: int = Field(default=8000, description="服务器监听端口")
    debug: bool = Field(default=True, description="调试模式")

    # --- API 聚合站配置 ---
    api_base_url: str = Field(default="", description="API 聚合站 URL，如 https://api.spiritgpu.com")
    api_key: str = Field(default="", description="API 聚合站密钥")

    # --- 默认模型 ---
    default_text_model: str = Field(default="", description="默认文本理解模型 ID")
    default_image_model: str = Field(default="", description="默认图片生成模型 ID")

    # --- 文件存储 ---
    data_dir: Path = Field(default=DATA_DIR, description="数据存储根目录")

    # --- 并发控制 ---
    max_concurrent_generations: int = Field(default=3, description="图片生成最大并发数")

    model_config = {
        "env_file": str(BASE_DIR.parent / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def load_settings() -> Settings:
    """
    加载配置：优先从 settings.json 读取（运行时用户修改的配置），
    缺失字段回退到环境变量和默认值。
    """
    overrides = {}
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            overrides = json.load(f)
    return Settings(**overrides)


def save_settings(data: dict) -> None:
    """
    将用户通过 Web 页面修改的配置持久化到 settings.json。
    仅保存用户主动设置的字段（api_base_url, api_key, default_text_model, default_image_model）。
    """
    existing = {}
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing.update(data)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)


# 全局单例
settings = load_settings()
