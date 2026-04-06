"""
文件名：export.py
功能描述：文档导出的 API 路由。处理导出请求和文件下载。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 POST / 端点
- [x] TODO-2: 实现 GET /{export_id}/download 端点

依赖：fastapi, fastapi.responses.FileResponse, schemas.export, exporters,
      services.document_service, storage.file_manager
"""

import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from schemas.export import ExportRequest, ExportResponse, ExportFormat
from exporters import get_exporter, get_supported_formats
from services.document_service import document_service
from services.task_manager import task_manager
from schemas.task import TaskPhase
from storage.file_manager import get_export_path

router = APIRouter()

# 内存存储导出记录: {export_id: {"path": ..., "filename": ..., "content_type": ...}}
_exports: dict[str, dict] = {}


@router.post("/", response_model=ExportResponse)
async def create_export(request: ExportRequest):
    """请求导出文档"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"[导出API] 收到导出请求，任务: {request.task_id}, 格式: {request.format}")
    
    # 验证任务已完成
    try:
        task = await task_manager.get_task(request.task_id)
        if task.phase != TaskPhase.COMPLETE:
            raise HTTPException(status_code=400, detail="任务未完成，无法导出")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    # 获取处理结果
    illustrated_doc = await document_service.get_result(request.task_id)
    
    logger.info(f"[导出API] 获取到结果，共有 {len(illustrated_doc.illustrations)} 个插图")
    for illu in illustrated_doc.illustrations:
        logger.info(f"  - {illu.id}: status={illu.status}, image_path={illu.image_path}")
    
    # 获取导出器
    exporter = get_exporter(request.format.value)
    
    # 生成导出 ID
    export_id = str(uuid.uuid4())
    
    # 导出文件
    output_path = get_export_path(export_id, exporter.file_extension)
    logger.info(f"[导出API] 开始导出到: {output_path}")
    await exporter.export(illustrated_doc, output_path)
    
    # 生成下载文件名
    original_filename = Path(illustrated_doc.document.filename).stem
    download_filename = f"{original_filename}_with_illustrations{exporter.file_extension}"
    
    # 存储导出记录
    _exports[export_id] = {
        "path": output_path,
        "filename": download_filename,
        "content_type": exporter.content_type,
    }
    
    return ExportResponse(
        export_id=export_id,
        format=request.format,
        filename=download_filename,
    )


@router.get("/{export_id}/download")
async def download_export(export_id: str):
    """下载导出的文件"""
    if export_id not in _exports:
        raise HTTPException(status_code=404, detail="导出记录不存在")
    
    export_info = _exports[export_id]
    file_path = export_info["path"]
    
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="导出文件不存在")
    
    return FileResponse(
        path=file_path,
        media_type=export_info["content_type"],
        filename=export_info["filename"],
    )
