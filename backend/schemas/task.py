"""
文件名：task.py
功能描述：任务相关数据模型。定义任务状态（TaskState）、进度事件（ProgressEvent）等。
         任务贯穿文档处理的全生命周期：上传 -> 解析 -> AI分析 -> 生图 -> 完成。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 核心数据模型已完成
"""

from enum import Enum
from pydantic import BaseModel, Field


class TaskPhase(str, Enum):
    """任务处理阶段"""
    UPLOADED = "uploaded"       # 已上传，等待开始
    PARSING = "parsing"        # 文档解析中
    ANALYZING = "analyzing"    # AI 内容分析中
    PREVIEW = "preview"        # 预览阶段，等待用户确认
    GENERATING = "generating"  # AI 图片生成中
    COMPLETE = "complete"      # 处理完成
    FAILED = "failed"          # 处理失败


class TaskState(BaseModel):
    """任务完整状态"""
    task_id: str = Field(description="任务 ID")
    filename: str = Field(description="原始文件名")
    source_format: str = Field(default="", description="文件格式")
    phase: TaskPhase = Field(default=TaskPhase.UPLOADED, description="当前阶段")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="总进度 0.0 ~ 1.0")
    message: str = Field(default="", description="当前状态描述")
    text_model: str = Field(default="", description="使用的文本模型")
    image_model: str = Field(default="", description="使用的图片模型")
    illustration_count: int = Field(default=0, description="计划生成的插图数")
    completed_count: int = Field(default=0, description="已完成的插图数")
    error_message: str = Field(default="", description="失败原因")


class ProgressEvent(BaseModel):
    """SSE 推送的进度事件"""
    task_id: str
    phase: TaskPhase
    progress: float
    message: str
    detail: dict = Field(default_factory=dict, description="阶段特定的详细信息")


class TaskStartRequest(BaseModel):
    """启动任务的请求体"""
    text_model: str = Field(description="用于文案理解的文本模型 ID")
    image_model: str = Field(description="用于生成插图的图片模型 ID")
    style: str = Field(default="flat", description="插图风格")
    is_ppt_mode: bool = Field(default=False, description="是否为PPT模式")
