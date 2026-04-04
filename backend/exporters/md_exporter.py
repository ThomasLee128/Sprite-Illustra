"""
文件名：md_exporter.py
功能描述：Markdown 导出器。将 IllustratedDocument 导出为 Markdown 文件，
         插图以 Markdown 图片语法嵌入。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 export(self, illustrated_doc, output_path) -> str
      - 构建 Markdown 文本：
        * HEADING -> "# " * level + content + "\n\n"
        * PARAGRAPH -> content + "\n\n"
        * LIST -> "- " + content + "\n"（列表结束后加空行）
        * CODE -> "```\n" + content + "\n```\n\n"
        * BLOCKQUOTE -> "> " + content + "\n\n"
      - 每个 section 输出后，检查是否有对应插图：
        * 如有且 status==DONE: "![{description_cn}]({image_relative_path})\n\n"
        * image_relative_path: 相对于导出文件的路径
      - 将图片复制到导出目录的 images/ 子目录下
      - 写入文件: output_path
      - 返回 output_path
依赖：schemas.document, core.exceptions, shutil, pathlib
"""

from exporters.base import BaseExporter
from exporters import register_exporter
from schemas.document import IllustratedDocument


@register_exporter
class MdExporter(BaseExporter):
    """Markdown 导出器"""

    format_name = "md"
    content_type = "text/markdown; charset=utf-8"
    file_extension = ".md"

    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """导出为 Markdown"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
