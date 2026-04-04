"""
文件名：pdf_exporter.py
功能描述：PDF 导出器。将 IllustratedDocument 导出为 PDF 文件。
         策略：先生成 HTML，再用 weasyprint 转为 PDF。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 export(self, illustrated_doc, output_path) -> str
      - 先调用内部方法将 IllustratedDocument 转为 HTML 字符串
        （可复用 html_exporter 的逻辑，或直接构建 HTML）
      - HTML 结构：
        * <html><head> 内嵌基础 CSS（字体、行距、图片居中、页面边距）
        * <body> 内按 sections 顺序输出 <h1>~<h6>、<p>、<ul>、<pre>、<blockquote>
        * 插图位置插入 <img src="file://{absolute_path}" style="max-width:100%">
        * 图片下方 <p class="caption">{description_cn}</p>
      - 使用 weasyprint.HTML(string=html).write_pdf(output_path)
      - 返回 output_path
      - 异常处理: weasyprint 未安装 -> raise ExportError("PDF 导出需要安装 weasyprint")
依赖：weasyprint, schemas.document, core.exceptions, pathlib
"""

from exporters.base import BaseExporter
from exporters import register_exporter
from schemas.document import IllustratedDocument


@register_exporter
class PdfExporter(BaseExporter):
    """PDF 导出器"""

    format_name = "pdf"
    content_type = "application/pdf"
    file_extension = ".pdf"

    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """导出为 PDF"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
