"""
文件名：documents.py
功能描述：文档上传与管理的 API 路由。处理文件上传、格式验证等。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 POST /upload 端点

依赖：fastapi.UploadFile, parsers.get_supported_extensions, storage.file_manager,
      services.task_manager
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from parsers import get_supported_extensions
from storage.file_manager import save_upload
from services.task_manager import task_manager

router = APIRouter()

# 最大文件大小 50MB
MAX_FILE_SIZE = 50 * 1024 * 1024


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传文档"""
    # 检查文件大小
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="文件过大，最大支持 50MB")
    
    # 检查文件格式
    filename = file.filename or "unknown"
    ext = Path(filename).suffix.lower()
    
    supported_exts = get_supported_extensions()
    if ext not in supported_exts:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {ext}（支持: {', '.join(supported_exts)}）"
        )
    
    # 保存文件
    task_id, saved_path = save_upload(file_content, filename)
    
    # 创建任务
    source_format = ext.lstrip(".")
    await task_manager.create_task(task_id, filename, source_format)
    
    return {
        "task_id": task_id,
        "filename": filename,
        "format": source_format,
    }
