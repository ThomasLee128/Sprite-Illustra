"""
文件名：documents.py
功能描述：文档上传与管理的 API 路由。处理文件上传、格式验证等。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 POST /upload 端点
      - 接收 UploadFile 参数
      - 验证文件扩展名是否在支持列表中（调用 get_supported_extensions()）
      - 调用 file_manager.save_upload 保存文件
      - 调用 task_manager.create_task 创建任务
      - 返回 {"task_id": ..., "filename": ..., "format": ...}
      - 文件过大（>50MB）-> 返回 413
      - 格式不支持 -> 返回 400
依赖：fastapi.UploadFile, parsers.get_supported_extensions, storage.file_manager,
      services.task_manager
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/upload")
async def upload_document():
    """上传文档"""
    # TODO-1
    raise NotImplementedError("待 Trea 实现")
