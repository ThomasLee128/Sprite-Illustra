"""
文件名：html_exporter.py
功能描述：HTML 导出器。将 IllustratedDocument 导出为独立 HTML 文件，
         内嵌 CSS 样式，插图以 base64 或相对路径嵌入。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 export(self, illustrated_doc, output_path) -> str
      - 构建完整的 HTML 文档：
        * <!DOCTYPE html><html lang="zh-CN">
        * <head> 内嵌 CSS：
          - 正文字体: "Microsoft YaHei", "PingFang SC", sans-serif
          - 最大宽度 800px 居中，行距 1.8
          - 标题样式（h1~h6）
          - 图片: max-width: 100%, 居中, margin: 1em auto, display: block
          - 图注: text-align: center, color: #666, font-size: 0.9em
          - 代码块: background: #f5f5f5, padding: 1em, overflow-x: auto
          - 引用块: border-left: 4px solid #ddd, padding-left: 1em, color: #555
        * <body> 内按 sections 顺序输出 HTML 标签
        * 插图: <figure><img src="..."><figcaption>{description_cn}</figcaption></figure>
      - 图片处理策略：
        * 将图片读取为 base64，嵌入为 data:image/png;base64,...
        * 这样 HTML 文件独立可用，无需额外图片文件
      - 写入文件: output_path
      - 返回 output_path
依赖：schemas.document, core.exceptions, base64, pathlib
"""

from exporters.base import BaseExporter
from exporters import register_exporter
from schemas.document import IllustratedDocument


@register_exporter
class HtmlExporter(BaseExporter):
    """HTML 导出器"""

    format_name = "html"
    content_type = "text/html; charset=utf-8"
    file_extension = ".html"

    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """导出为 HTML"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
