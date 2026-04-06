"""
文件名：task_manager.py
功能描述：异步任务管理器。管理文档处理任务的生命周期状态，
         提供 SSE 订阅机制实现前端实时进度推送。
         使用内存字典 + asyncio.Queue 实现，无需外部消息队列。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 create_task(self, task_id, filename, source_format) -> TaskState
- [x] TODO-2: 实现 update_progress(self, task_id, phase, progress, message, detail=None)
- [x] TODO-3: 实现 subscribe(self, task_id) -> AsyncIterator[dict]
- [x] TODO-4: 实现 mark_failed(self, task_id, error_message)
- [x] TODO-5: 实现 get_task(self, task_id) -> TaskState

依赖：asyncio, schemas.task, core.exceptions
"""

import asyncio
from typing import AsyncIterator

from schemas.task import TaskState, ProgressEvent, TaskPhase
from core.exceptions import TaskNotFoundError


class TaskManager:
    """异步任务管理器（单例模式，在 main.py 中初始化）"""

    def __init__(self):
        self._tasks: dict[str, TaskState] = {}
        self._subscribers: dict[str, list[asyncio.Queue]] = {}

    async def create_task(self, task_id: str, filename: str, source_format: str) -> TaskState:
        """创建新任务"""
        task = TaskState(
            task_id=task_id,
            filename=filename,
            source_format=source_format,
            phase=TaskPhase.UPLOADED,
            progress=0.0,
            message="文件已上传，等待处理",
        )
        self._tasks[task_id] = task
        return task

    async def update_progress(
        self,
        task_id: str,
        phase: TaskPhase,
        progress: float,
        message: str,
        detail: dict | None = None,
    ) -> None:
        """更新任务进度并通知所有 SSE 订阅者"""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        
        task = self._tasks[task_id]
        task.phase = phase
        task.progress = progress
        task.message = message
        
        # 更新完成计数
        if detail and "completed_count" in detail:
            task.completed_count = detail["completed_count"]
        
        # 构建进度事件
        progress_event = ProgressEvent(
            task_id=task_id,
            phase=phase,
            progress=progress,
            message=message,
            detail=detail or {},
        )
        
        # 推送给所有订阅者
        if task_id in self._subscribers:
            event_dict = progress_event.model_dump()
            for queue in self._subscribers[task_id]:
                try:
                    queue.put_nowait(event_dict)
                except asyncio.QueueFull:
                    pass

    async def subscribe(self, task_id: str) -> AsyncIterator[dict]:
        """订阅任务进度事件（用于 SSE 推送）"""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        
        # 创建队列
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        
        # 注册订阅者
        if task_id not in self._subscribers:
            self._subscribers[task_id] = []
        self._subscribers[task_id].append(queue)
        
        try:
            # 先推送当前状态
            task = self._tasks[task_id]
            yield ProgressEvent(
                task_id=task_id,
                phase=task.phase,
                progress=task.progress,
                message=task.message,
                detail={},
            ).model_dump()
            
            # 循环等待事件
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=1.0)
                    yield event
                    
                    # 检查是否完成或失败
                    if event["phase"] in [TaskPhase.COMPLETE, TaskPhase.FAILED]:
                        break
                except asyncio.TimeoutError:
                    # 超时继续等待
                    continue
        finally:
            # 清理订阅者
            if task_id in self._subscribers:
                try:
                    self._subscribers[task_id].remove(queue)
                    if not self._subscribers[task_id]:
                        del self._subscribers[task_id]
                except ValueError:
                    pass

    async def mark_failed(self, task_id: str, error_message: str) -> None:
        """标记任务失败"""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        
        task = self._tasks[task_id]
        task.phase = TaskPhase.FAILED
        task.progress = 1.0
        task.message = "处理失败"
        task.error_message = error_message
        
        # 推送失败事件
        progress_event = ProgressEvent(
            task_id=task_id,
            phase=TaskPhase.FAILED,
            progress=1.0,
            message="处理失败",
            detail={"error": error_message},
        )
        
        if task_id in self._subscribers:
            event_dict = progress_event.model_dump()
            for queue in self._subscribers[task_id]:
                try:
                    queue.put_nowait(event_dict)
                except asyncio.QueueFull:
                    pass

    async def get_task(self, task_id: str) -> TaskState:
        """获取任务状态"""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]


# 全局单例
task_manager = TaskManager()
