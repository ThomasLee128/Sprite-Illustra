"""
文件名：html_exporter.py
功能描述：HTML 导出器。将 IllustratedDocument 导出为独立 HTML 文件，
         内嵌 CSS 样式，插图以 base64 或相对路径嵌入。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 export(self, illustrated_doc, output_path) -> str

依赖：schemas.document, core.exceptions, base64, pathlib
"""

import base64
from pathlib import Path

from exporters.base import BaseExporter
from exporters import register_exporter
from schemas.document import IllustratedDocument, SectionType, IllustrationStatus


@register_exporter
class HtmlExporter(BaseExporter):
    """HTML 导出器"""

    format_name = "html"
    content_type = "text/html; charset=utf-8"
    file_extension = ".html"

    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """导出为 HTML"""
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"[HTML 导出器] 开始导出，共有 {len(illustrated_doc.illustrations)} 个插图")
        
        # 创建 section.id -> section 的映射
        section_map = {s.id: s for s in illustrated_doc.document.sections}
        
        # 创建 after_section_id -> illustrations 的映射
        illustrations_map: dict[str, list] = {}
        for illu in illustrated_doc.illustrations:
            logger.info(f"[HTML 导出器] 检查插图: {illu.id}, status={illu.status}, image_path={illu.image_path}")
            if illu.status != IllustrationStatus.DONE or not illu.image_path:
                continue
            if illu.after_section_id not in illustrations_map:
                illustrations_map[illu.after_section_id] = []
            illustrations_map[illu.after_section_id].append(illu)
        
        logger.info(f"[HTML 导出器] 找到 {len(illustrations_map)} 个section有插图需要插入")
        
        # 构建 HTML 内容
        html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.8;
            color: #333;
            background-color: #f9f9f9;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #222;
        }}
        h1 {{ font-size: 2em; }}
        h2 {{ font-size: 1.5em; }}
        h3 {{ font-size: 1.25em; }}
        p {{
            margin-bottom: 1em;
        }}
        figure {{
            margin: 2em 0;
            text-align: center;
        }}
        figure img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
            border-radius: 4px;
        }}
        figure figcaption {{
            margin-top: 0.75em;
            color: #666;
            font-size: 0.9em;
        }}
        pre {{
            background: #f5f5f5;
            padding: 1em;
            overflow-x: auto;
            border-radius: 4px;
            margin: 1em 0;
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
    <div class="container">
""".format(title=illustrated_doc.document.metadata.title or "文档")
        
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
                    logger.info(f"[HTML 导出器] 尝试插入图片: {src_path}, 存在={src_path.exists()}")
                    if src_path.exists():
                        try:
                            # 读取图片并编码为 base64
                            with open(src_path, "rb") as f:
                                image_data = f.read()
                                base64_data = base64.b64encode(image_data).decode('utf-8')
                            
                            # 获取 MIME 类型
                            ext = src_path.suffix.lower()
                            mime_type = "image/png"
                            if ext in [".jpg", ".jpeg"]:
                                mime_type = "image/jpeg"
                            elif ext == ".gif":
                                mime_type = "image/gif"
                            elif ext == ".webp":
                                mime_type = "image/webp"
                            
                            img_src = f"data:{mime_type};base64,{base64_data}"
                            figcaption = illu.description_cn or ""
                            
                            html_content += f"""
        <figure>
            <img src="{img_src}" alt="{figcaption}">
            <figcaption>{figcaption}</figcaption>
        </figure>
"""
                            logger.info(f"[HTML 导出器] 图片插入成功: {src_path}")
                        except Exception as e:
                            logger.error(f"[HTML 导出器] 图片插入失败: {e}")
                            pass
                    else:
                        logger.warning(f"[HTML 导出器] 图片文件不存在: {src_path}")
        
        html_content += """
    </div>
</body>
</html>
"""
        
        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return output_path
