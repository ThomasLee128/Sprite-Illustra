"""
文件名：tasks.py
功能描述：任务管理的 API 路由。包括启动处理任务、查询状态、SSE 进度推送、
         获取结果、插图调整（删除/重新生成/移动）等端点。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 POST /{task_id}/start 端点
      - 接收 TaskStartRequest 请求体 (text_model, image_model, style)
      - 验证任务存在且 phase == UPLOADED
      - 获取上传文件路径
      - 使用 asyncio.create_task() 在后台启动:
        document_service.process_document(task_id, file_path, text_model, image_model, style)
      - 立即返回 {"task_id": ..., "message": "处理已开始"}

- [ ] TODO-2: 实现 GET /{task_id} 端点
      - 调用 task_manager.get_task(task_id)
      - 返回 TaskState

- [ ] TODO-3: 实现 GET /{task_id}/sse 端点
      - 调用 task_manager.subscribe(task_id) 获取事件流
      - 使用 core.sse.create_sse_response 包装为 SSE 响应
      - content_type: text/event-stream

- [ ] TODO-4: 实现 GET /{task_id}/result 端点
      - 调用 document_service.get_result(task_id)
      - 返回 IllustratedDocument（JSON 序列化）

- [ ] TODO-5: 实现 DELETE /{task_id}/illustrations/{illustration_id} 端点
      - 调用 document_service.remove_illustration

- [ ] TODO-6: 实现 POST /{task_id}/illustrations/{illustration_id}/regenerate 端点
      - 可选请求体: {"prompt": "new prompt"}
      - 调用 document_service.regenerate_illustration

- [ ] TODO-7: 实现 PUT /{task_id}/illustrations/{illustration_id}/move 端点
      - 请求体: {"after_section_id": "..."}
      - 调用 document_service.move_illustration

依赖：fastapi, asyncio, schemas.task, services.task_manager, services.document_service, core.sse
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/{task_id}/start")
async def start_task(task_id: str):
    """启动文档处理任务"""
    # TODO-1
    raise NotImplementedError("待 Trea 实现")


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """查询任务状态"""
    # TODO-2
    raise NotImplementedError("待 Trea 实现")


@router.get("/{task_id}/sse")
async def task_sse(task_id: str):
    """SSE 实时进度推送"""
    # TODO-3
    raise NotImplementedError("待 Trea 实现")


@router.get("/{task_id}/result")
async def get_task_result(task_id: str):
    """获取处理结果"""
    # TODO-4
    raise NotImplementedError("待 Trea 实现")


@router.delete("/{task_id}/illustrations/{illustration_id}")
async def remove_illustration(task_id: str, illustration_id: str):
    """删除插图"""
    # TODO-5
    raise NotImplementedError("待 Trea 实现")


@router.post("/{task_id}/illustrations/{illustration_id}/regenerate")
async def regenerate_illustration(task_id: str, illustration_id: str):
    """重新生成插图"""
    # TODO-6
    raise NotImplementedError("待 Trea 实现")


@router.put("/{task_id}/illustrations/{illustration_id}/move")
async def move_illustration(task_id: str, illustration_id: str):
    """调整插图位置"""
    # TODO-7
    raise NotImplementedError("待 Trea 实现")
