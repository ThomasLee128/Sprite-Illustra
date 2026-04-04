"""
文件名：document_service.py
功能描述：文档处理主编排服务。串联文档处理的完整流程：
         解析 -> AI 分析 -> AI 生图 -> 组装 IllustratedDocument。
         作为后台异步任务运行，通过 task_manager 推送进度。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 process_document(self, task_id, file_path, text_model, image_model, style)
      - 这是主编排函数，由 asyncio.create_task() 在后台运行
      - 用 try/except 包裹整个流程，异常时调用 task_manager.mark_failed

      - 阶段 1: 文档解析
        * 从 file_path 提取扩展名
        * 调用 get_parser(ext).parse(file_path) 获取 Document
        * 推送进度: phase=PARSING, progress=0.1, message="文档解析完成"

      - 阶段 2: AI 内容分析
        * 推送进度: phase=ANALYZING, progress=0.15, message="AI 正在分析文档内容..."
        * 调用 ai_analyzer.analyze(document, text_model, task_id)
        * 获取 list[IllustrationItem]
        * 更新 task_state.illustration_count = len(illustrations)
        * 推送进度: phase=ANALYZING, progress=0.3, message=f"分析完成，计划生成 {n} 张插图"

      - 阶段 3: AI 图片生成
        * 推送进度: phase=GENERATING, progress=0.35, message="开始生成插图..."
        * 调用 ai_illustrator.generate_all(illustrations, image_model, task_id)
        * （generate_all 内部会逐张推送进度，从 0.35 到 0.95）

      - 阶段 4: 组装
        * 构建 IllustratedDocument(document=document, illustrations=illustrations)
        * 存储到 self._results[task_id]
        * 推送进度: phase=COMPLETE, progress=1.0, message="处理完成"

- [ ] TODO-2: 实现 get_result(self, task_id) -> IllustratedDocument
      - 从 self._results 中获取结果
      - 不存在则 raise TaskNotFoundError

- [ ] TODO-3: 实现 regenerate_illustration(self, task_id, illustration_id, new_prompt)
      - 从 _results 获取 IllustratedDocument
      - 找到对应的 IllustrationItem
      - 如有 new_prompt 则更新 prompt
      - 调用 ai_illustrator.generate_one 重新生成
      - 更新结果

- [ ] TODO-4: 实现 remove_illustration(self, task_id, illustration_id)
      - 从结果中移除指定插图

- [ ] TODO-5: 实现 move_illustration(self, task_id, illustration_id, after_section_id)
      - 修改插图的 after_section_id

依赖：parsers, services.ai_analyzer, services.ai_illustrator, services.task_manager,
      schemas.document, core.exceptions, asyncio
"""

from schemas.document import IllustratedDocument


class DocumentService:
    """文档处理主编排服务"""

    def __init__(self):
        self._results: dict[str, IllustratedDocument] = {}

    async def process_document(
        self,
        task_id: str,
        file_path: str,
        text_model: str,
        image_model: str,
        style: str = "flat",
    ) -> None:
        """主编排：解析 -> 分析 -> 生图 -> 组装（后台异步运行）"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")

    async def get_result(self, task_id: str) -> IllustratedDocument:
        """获取处理结果"""
        # TODO-2
        raise NotImplementedError("待 Trea 实现")

    async def regenerate_illustration(
        self, task_id: str, illustration_id: str, new_prompt: str | None = None
    ) -> None:
        """重新生成指定插图"""
        # TODO-3
        raise NotImplementedError("待 Trea 实现")

    async def remove_illustration(self, task_id: str, illustration_id: str) -> None:
        """删除指定插图"""
        # TODO-4
        raise NotImplementedError("待 Trea 实现")

    async def move_illustration(
        self, task_id: str, illustration_id: str, after_section_id: str
    ) -> None:
        """调整插图位置"""
        # TODO-5
        raise NotImplementedError("待 Trea 实现")


# 全局单例
document_service = DocumentService()
