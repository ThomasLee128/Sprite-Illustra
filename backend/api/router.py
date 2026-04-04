"""
文件名：router.py
功能描述：API 总路由注册器。将所有子路由模块统一注册到一个 APIRouter 下。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 路由注册已完成
"""

from fastapi import APIRouter

from api.documents import router as documents_router
from api.tasks import router as tasks_router
from api.settings import router as settings_router
from api.export import router as export_router

api_router = APIRouter()

api_router.include_router(documents_router, prefix="/documents", tags=["文档管理"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["任务管理"])
api_router.include_router(settings_router, prefix="/settings", tags=["API 设置"])
api_router.include_router(export_router, prefix="/export", tags=["文档导出"])
