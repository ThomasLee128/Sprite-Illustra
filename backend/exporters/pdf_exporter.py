"""
文件名：pdf_exporter.py
功能描述：PDF 导出器。将 IllustratedDocument 导出为 PDF 文件。
         策略：先生成 HTML，再用 weasyprint 转为 PDF。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 export(self, illustrated_doc, output_path) -> str

依赖：weasyprint, schemas.document, core.exceptions, pathlib
"""

from pathlib import Path

try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

from exporters.base import BaseExporter
from exporters import register_exporter
from schemas.document import IllustratedDocument, SectionType, IllustrationStatus
from core.exceptions import ExportError


@register_exporter
class PdfExporter(BaseExporter):
    """PDF 导出器"""

    format_name = "pdf"
    content_type = "application/pdf"
    file_extension = ".pdf"

    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """导出为 PDF"""
        if not HAS_WEASYPRINT:
            raise ExportError("PDF 导出需要安装 weasyprint 库")
        
        # 创建 section.id -> section 的映射
        section_map = {s.id: s for s in illustrated_doc.document.sections}
        
        # 创建 after_section_id -> illustrations 的映射
        illustrations_map: dict[str, list] = {}
        for illu in illustrated_doc.illustrations:
            if illu.status != IllustrationStatus.DONE or not illu.image_path:
                continue
            if illu.after_section_id not in illustrations_map:
                illustrations_map[illu.after_section_id] = []
            illustrations_map[illu.after_section_id].append(illu)
        
        # 构建 HTML 内容
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{illustrated_doc.document.metadata.title or '文档'}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            font-size: 12pt;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #222;
            page-break-after: avoid;
        }}
        h1 {{ font-size: 24pt; }}
        h2 {{ font-size: 18pt; }}
        h3 {{ font-size: 15pt; }}
        p {{
            margin-bottom: 1em;
            text-align: justify;
        }}
        figure {{
            margin: 1.5em 0;
            text-align: center;
            page-break-inside: avoid;
        }}
        figure img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        figure figcaption {{
            margin-top: 0.5em;
            color: #666;
            font-size: 10pt;
        }}
        pre {{
            background: #f5f5f5;
            padding: 1em;
            overflow-x: auto;
            margin: 1em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}
        code {{
            font-family: "Courier New", Consolas, monospace;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 1em;
            color: #555;
            margin: 1em 0;
        }}
        ul, ol {{
            margin-left: 2em;
            margin-bottom: 1em;
        }}
    </style>
</head>
<body>
"""
        
        # 按顺序输出 sections 和插图
        for section in illustrated_doc.document.sections:
            # 输出 section
            if section.type == SectionType.HEADING:
                level = min(section.level, 6)
                html_content += f"<h{level}>{section.content}</h{level}>\n"
            elif section.type == SectionType.PARAGRAPH:
                html_content += f"<p>{section.content}</p>\n"
            elif section.type == SectionType.LIST:
                html_content += f"<ul><li>{section.content}</li></ul>\n"
            elif section.type == SectionType.CODE:
                html_content += f"<pre><code>{section.content}</code></pre>\n"
            elif section.type == SectionType.BLOCKQUOTE:
                html_content += f"<blockquote>{section.content}</blockquote>\n"
            
            # 输出该 section 后的插图
            if section.id in illustrations_map:
                for illu in illustrations_map[section.id]:
                    src_path = Path(illu.image_path)
                    if src_path.exists():
                        try:
                            # 使用 file:// URL
                            img_src = f"file://{src_path.absolute()}"
                            figcaption = illu.description_cn or ""
                            
                            html_content += f"""
        <figure>
            <img src="{img_src}" alt="{figcaption}">
            <figcaption>{figcaption}</figcaption>
        </figure>
"""
                        except Exception as e:
                            pass
        
        html_content += """
</body>
</html>
"""
        
        # 使用 weasyprint 转换为 PDF
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
