"""
文件名：export.py
功能描述：文档导出的 API 路由。处理导出请求和文件下载。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 POST / 端点
      - 接收 ExportRequest 请求体 (task_id, format)
      - 验证任务已完成（phase == COMPLETE）
      - 调用 document_service.get_result(task_id) 获取 IllustratedDocument
      - 调用 get_exporter(format).export(illustrated_doc, output_path)
      - 生成 export_id（UUID）
      - 存储导出文件信息到 self._exports（或使用简单的内存字典）
      - 返回 ExportResponse

- [ ] TODO-2: 实现 GET /{export_id}/download 端点
      - 根据 export_id 查找导出文件路径
      - 使用 FileResponse 返回文件
      - 设置正确的 Content-Type 和 Content-Disposition（filename 使用原始文件名+新扩展名）
      - 文件不存在 -> 返回 404

依赖：fastapi, fastapi.responses.FileResponse, schemas.export, exporters,
      services.document_service, storage.file_manager
"""

from fastapi import APIRouter

router = APIRouter()

# 内存存储导出记录: {export_id: {"path": ..., "filename": ..., "content_type": ...}}
_exports: dict[str, dict] = {}


@router.post("/")
async def create_export():
    """请求导出文档"""
    # TODO-1
    raise NotImplementedError("待 Trea 实现")


@router.get("/{export_id}/download")
async def download_export(export_id: str):
    """下载导出的文件"""
    # TODO-2
    raise NotImplementedError("待 Trea 实现")
