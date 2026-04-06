"""
文件名：file_manager.py
功能描述：文件存储管理。处理上传文件的保存、生成图片的存储、导出文件的管理。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 save_upload(file, filename) -> tuple[str, str]
- [x] TODO-2: 实现 get_export_path(task_id, format_ext) -> str
- [x] TODO-3: 实现 cleanup_task(task_id)

依赖：config.DATA_DIR, uuid, pathlib, shutil
"""

import uuid
import shutil
from pathlib import Path
from typing import Tuple
from datetime import datetime

from config import DATA_DIR


def save_upload(file_content: bytes, filename: str) -> Tuple[str, str]:
    """
    保存上传文件
    
    Args:
        file_content: 文件内容字节
        filename: 原始文件名
    
    Returns:
        (task_id, 保存后的文件完整路径)
    """
    task_id = str(uuid.uuid4())
    
    uploads_dir = DATA_DIR / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    # 提取文件扩展名
    ext = Path(filename).suffix
    saved_filename = f"{task_id}{ext}"
    saved_path = uploads_dir / saved_filename
    
    # 写入文件
    with open(saved_path, "wb") as f:
        f.write(file_content)
    
    return task_id, str(saved_path)


def get_export_path(task_id: str, format_ext: str) -> str:
    """
    获取导出文件路径
    
    Args:
        task_id: 任务 ID
        format_ext: 文件扩展名（如 ".html" 或 "docx"）
    
    Returns:
        导出文件完整路径
    """
    # 导出到项目根目录（智灵智能插图）
    project_root = Path(__file__).parent.parent.parent
    project_root.mkdir(parents=True, exist_ok=True)
    
    # 确保扩展名以 . 开头
    if not format_ext.startswith("."):
        format_ext = "." + format_ext
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(project_root / f"导出文件_{timestamp}{format_ext}")


def cleanup_task(task_id: str) -> None:
    """
    清理任务相关的临时文件
    
    Args:
        task_id: 任务 ID
    """
    # 清理上传文件
    uploads_dir = DATA_DIR / "uploads"
    for file_path in uploads_dir.glob(f"{task_id}*"):
        if file_path.is_file():
            file_path.unlink()
    
    # 清理生成的图片
    images_dir = DATA_DIR / "images"
    # 注意：图片文件名是 UUID，不直接关联 task_id
    # 如果需要清理，可以在 document_service 中维护图片路径列表
    
    # 导出文件保留一段时间，暂不清理
