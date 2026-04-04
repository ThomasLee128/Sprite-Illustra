"""
文件名：export.py
功能描述：导出相关数据模型。定义导出请求和响应格式。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 核心数据模型已完成
"""

from enum import Enum
from pydantic import BaseModel, Field


class ExportFormat(str, Enum):
    """支持的导出格式"""
    WORD = "docx"
    PDF = "pdf"
    MARKDOWN = "md"
    HTML = "html"


class ExportRequest(BaseModel):
    """导出请求"""
    task_id: str = Field(description="任务 ID")
    format: ExportFormat = Field(description="导出格式")


class ExportResponse(BaseModel):
    """导出响应"""
    export_id: str = Field(description="导出任务 ID，用于下载")
    format: ExportFormat
    filename: str = Field(description="导出文件名")
