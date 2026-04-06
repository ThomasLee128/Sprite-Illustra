"""
文件名：tasks.py
功能描述：任务管理的 API 路由。包括启动处理任务、查询状态、SSE 进度推送、
         获取结果、插图调整（删除/重新生成/移动）等端点。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 POST /{task_id}/start 端点
- [x] TODO-2: 实现 GET /{task_id} 端点
- [x] TODO-3: 实现 GET /{task_id}/sse 端点
- [x] TODO-4: 实现 GET /{task_id}/result 端点
- [x] TODO-5: 实现 DELETE /{task_id}/illustrations/{illustration_id} 端点
- [x] TODO-6: 实现 POST /{task_id}/illustrations/{illustration_id}/regenerate 端点
- [x] TODO-7: 实现 PUT /{task_id}/illustrations/{illustration_id}/move 端点

依赖：fastapi, asyncio, schemas.task, services.task_manager, services.document_service, core.sse
"""

import asyncio
from pathlib import Path
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from schemas.task import TaskState, TaskStartRequest, TaskPhase
from services.task_manager import task_manager
from services.document_service import document_service
from core.sse import create_sse_response

router = APIRouter()


@router.post("/{task_id}/start")
async def start_task(task_id: str, request: TaskStartRequest):
    """启动文档处理任务"""
    try:
        # 验证任务存在且状态正确
        task = await task_manager.get_task(task_id)
        if task.phase != TaskPhase.UPLOADED:
            raise HTTPException(status_code=400, detail="任务已在处理中或已完成")
        
        # 获取上传文件路径
        from config import DATA_DIR
        ext = task.source_format
        uploads_dir = DATA_DIR / "uploads"
        file_path = str(uploads_dir / f"{task_id}.{ext}")
        
        # 在后台启动处理
        asyncio.create_task(
            document_service.process_document(
                task_id,
                file_path,
                request.text_model,
                request.image_model,
                request.style,
                request.is_ppt_mode,
            )
        )
        
        return {"task_id": task_id, "message": "处理已开始"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskState)
async def get_task_status(task_id: str):
    """查询任务状态"""
    try:
        return await task_manager.get_task(task_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{task_id}/sse")
async def task_sse(task_id: str):
    """SSE 实时进度推送"""
    try:
        event_generator = task_manager.subscribe(task_id)
        return create_sse_response(event_generator)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{task_id}/result")
async def get_task_result(task_id: str):
    """获取处理结果"""
    try:
        result = await document_service.get_result(task_id)
        # 创建一个副本用于API返回，把完整路径转换成文件名
        from copy import deepcopy
        from pathlib import Path
        result_dict = result.model_dump()
        
        for illu in result_dict["illustrations"]:
            if illu.get("image_path"):
                illu["image_path"] = Path(illu["image_path"]).name
        
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{task_id}/illustrations/{illustration_id}")
async def remove_illustration(task_id: str, illustration_id: str):
    """删除插图"""
    try:
        await document_service.remove_illustration(task_id, illustration_id)
        return {"success": True, "message": "插图已删除"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class RegenerateRequest(BaseModel):
    prompt: str | None = None


@router.post("/{task_id}/illustrations/{illustration_id}/regenerate")
async def regenerate_illustration(
    task_id: str, 
    illustration_id: str,
    request: RegenerateRequest | None = None
):
    """重新生成插图"""
    try:
        new_prompt = request.prompt if request else None
        await document_service.regenerate_illustration(task_id, illustration_id, new_prompt)
        return {"success": True, "message": "插图已重新生成"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class MoveRequest(BaseModel):
    after_section_id: str


@router.put("/{task_id}/illustrations/{illustration_id}/move")
async def move_illustration(task_id: str, illustration_id: str, request: MoveRequest):
    """调整插图位置"""
    try:
        await document_service.move_illustration(task_id, illustration_id, request.after_section_id)
        return {"success": True, "message": "插图位置已更新"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}/preview")
async def get_preview(task_id: str):
    """获取预览数据（文档和计划的插图）"""
    try:
        preview_data = await document_service.get_preview(task_id)
        return preview_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


class ConfirmPreviewRequest(BaseModel):
    """确认预览的请求"""
    image_model: str


@router.post("/{task_id}/preview/confirm")
async def confirm_preview(task_id: str, request: ConfirmPreviewRequest):
    """确认预览，开始生成图片"""
    try:
        # 在后台启动生成
        asyncio.create_task(
            document_service.confirm_preview(task_id, request.image_model)
        )
        return {"success": True, "message": "已确认，开始生成插图"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
