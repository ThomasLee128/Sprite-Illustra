"""
文件名：md_exporter.py
功能描述：Markdown 导出器。将 IllustratedDocument 导出为 Markdown 文件，
         插图以 Markdown 图片语法嵌入。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 export(self, illustrated_doc, output_path) -> str

依赖：schemas.document, core.exceptions, shutil, pathlib
"""

import shutil
from pathlib import Path

from exporters.base import BaseExporter
from exporters import register_exporter
from schemas.document import IllustratedDocument, SectionType, IllustrationStatus


@register_exporter
class MdExporter(BaseExporter):
    """Markdown 导出器"""

    format_name = "md"
    content_type = "text/markdown; charset=utf-8"
    file_extension = ".md"

    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """导出为 Markdown"""
        output_dir = Path(output_path).parent
        images_dir = output_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
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
        
        # 构建 Markdown 内容
        md_content = ""
        
        # 按顺序输出 sections 和插图
        for section in illustrated_doc.document.sections:
            # 输出 section
            if section.type == SectionType.HEADING:
                level = min(section.level, 6)
                md_content += f"{'#' * level} {section.content}\n\n"
            elif section.type == SectionType.PARAGRAPH:
                md_content += f"{section.content}\n\n"
            elif section.type == SectionType.LIST:
                md_content += f"{section.content}\n\n"
            elif section.type == SectionType.CODE:
                md_content += f"```\n{section.content}\n```\n\n"
            elif section.type == SectionType.BLOCKQUOTE:
                lines = section.content.split("\n")
                for line in lines:
                    md_content += f"> {line}\n"
                md_content += "\n"
            
            # 输出该 section 后的插图
            if section.id in illustrations_map:
                for illu in illustrations_map[section.id]:
                    # 复制图片到 images 目录
                    src_path = Path(illu.image_path)
                    if src_path.exists():
                        dest_filename = f"{illu.id}{src_path.suffix}"
                        dest_path = images_dir / dest_filename
                        shutil.copy2(src_path, dest_path)
                        
                        # 相对路径
                        relative_path = f"images/{dest_filename}"
                        alt_text = illu.description_cn or "插图"
                        md_content += f"![{alt_text}]({relative_path})\n\n"
        
        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        return output_path
