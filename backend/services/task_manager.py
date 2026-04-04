"""
文件名：task_manager.py
功能描述：异步任务管理器。管理文档处理任务的生命周期状态，
         提供 SSE 订阅机制实现前端实时进度推送。
         使用内存字典 + asyncio.Queue 实现，无需外部消息队列。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 create_task(self, task_id, filename, source_format) -> TaskState
      - 创建 TaskState 实例（phase=UPLOADED, progress=0）
      - 存入 self._tasks[task_id]
      - 返回 TaskState

- [ ] TODO-2: 实现 update_progress(self, task_id, phase, progress, message, detail=None)
      - 更新 self._tasks[task_id] 的 phase, progress, message
      - 如果 detail 中包含 completed_count，同步更新 TaskState.completed_count
      - 构建 ProgressEvent 并推送到所有订阅者队列:
        for queue in self._subscribers.get(task_id, []):
            await queue.put(progress_event.model_dump())

- [ ] TODO-3: 实现 subscribe(self, task_id) -> AsyncIterator[dict]
      - 创建新的 asyncio.Queue 并添加到 self._subscribers[task_id]
      - 先 yield 当前任务状态（让新连接立即获得当前进度）
      - 循环 await queue.get()，yield 事件
      - 当 phase 为 COMPLETE 或 FAILED 时，yield 后 break
      - finally 块中从 subscribers 列表移除该 queue

- [ ] TODO-4: 实现 mark_failed(self, task_id, error_message)
      - 更新任务状态为 FAILED
      - 推送失败事件到所有订阅者

- [ ] TODO-5: 实现 get_task(self, task_id) -> TaskState
      - 返回任务状态，不存在则 raise TaskNotFoundError

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
        # TODO-1
        raise NotImplementedError("待 Trea 实现")

    async def update_progress(
        self,
        task_id: str,
        phase: TaskPhase,
        progress: float,
        message: str,
        detail: dict | None = None,
    ) -> None:
        """更新任务进度并通知所有 SSE 订阅者"""
        # TODO-2
        raise NotImplementedError("待 Trea 实现")

    async def subscribe(self, task_id: str) -> AsyncIterator[dict]:
        """订阅任务进度事件（用于 SSE 推送）"""
        # TODO-3
        raise NotImplementedError("待 Trea 实现")
        yield  # 使其成为 async generator

    async def mark_failed(self, task_id: str, error_message: str) -> None:
        """标记任务失败"""
        # TODO-4
        raise NotImplementedError("待 Trea 实现")

    async def get_task(self, task_id: str) -> TaskState:
        """获取任务状态"""
        # TODO-5
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]


# 全局单例
task_manager = TaskManager()
