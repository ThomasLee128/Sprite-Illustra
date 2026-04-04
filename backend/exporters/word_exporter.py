"""
文件名：word_exporter.py
功能描述：Word (.docx) 导出器。将 IllustratedDocument 导出为 Word 文档，
         在对应段落后插入 AI 生成的配图。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 export(self, illustrated_doc, output_path) -> str
      - 使用 python-docx 创建新文档: doc = DocxDocument()
      - 遍历 illustrated_doc.document.sections：
        * HEADING -> doc.add_heading(content, level=section.level)
        * PARAGRAPH -> doc.add_paragraph(content)
        * LIST -> doc.add_paragraph(content, style='List Bullet')
        * CODE -> doc.add_paragraph(content)，设置等宽字体
        * BLOCKQUOTE -> doc.add_paragraph(content)，设置缩进样式
      - 每个 section 输出后，检查 illustrations 中是否有 after_section_id 匹配的插图
        * 如有且 status==DONE: doc.add_picture(image_path, width=Inches(5))
        * 图片下方可加居中标题: doc.add_paragraph(description_cn, style='Caption')
      - doc.save(output_path)
      - 返回 output_path
      - 异常处理: 图片文件不存在时跳过该插图并记录警告
依赖：python-docx (from docx import Document as DocxDocument, from docx.shared import Inches)
      schemas.document, core.exceptions
"""

from exporters.base import BaseExporter
from exporters import register_exporter
from schemas.document import IllustratedDocument


@register_exporter
class WordExporter(BaseExporter):
    """Word 文档导出器"""

    format_name = "docx"
    content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    file_extension = ".docx"

    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """导出为 Word 文档"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
