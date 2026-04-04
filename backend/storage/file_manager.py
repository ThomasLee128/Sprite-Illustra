"""
文件名：file_manager.py
功能描述：文件存储管理。处理上传文件的保存、生成图片的存储、导出文件的管理。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 save_upload(file, filename) -> tuple[str, str]
      - 生成 UUID 作为 task_id
      - 保存文件到 DATA_DIR/uploads/{task_id}_{filename}
      - 返回 (task_id, 保存后的文件完整路径)

- [ ] TODO-2: 实现 get_export_path(task_id, format_ext) -> str
      - 返回导出文件路径: DATA_DIR/exports/{task_id}.{format_ext}

- [ ] TODO-3: 实现 cleanup_task(task_id)
      - 清理任务相关的临时文件（上传文件、生成的图片）
      - 可选：保留导出文件一段时间

依赖：config.DATA_DIR, uuid, pathlib, shutil
"""

pass
