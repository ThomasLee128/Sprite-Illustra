"""
文件名：pdf_parser.py
功能描述：PDF 文件（.pdf）解析器。使用 PyMuPDF (fitz) 提取 PDF 文本内容，
         按页/块结构重组为段落，生成统一的 Document 结构。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 parse(self, file_path: str) -> Document

依赖：PyMuPDF (import fitz), schemas.document, core.exceptions, uuid
"""

import uuid
from pathlib import Path

try:
    import fitz
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

from parsers.base import BaseParser
from parsers import register_parser
from schemas.document import Document, DocumentSection, DocumentMetadata, SectionType
from core.exceptions import DocumentParseError


@register_parser
class PdfParser(BaseParser):
    """PDF 文件解析器"""

    supported_extensions = [".pdf"]

    async def parse(self, file_path: str) -> Document:
        """解析 .pdf 文件"""
        if not HAS_PDF:
            raise DocumentParseError("需要安装 PyMuPDF (fitz) 库才能解析 PDF 文档")
        
        try:
            doc = fitz.open(file_path)
            sections: list[DocumentSection] = []
            position = 0
            first_heading = ""
            total_words = 0
            
            for page_num, page in enumerate(doc):
                # 获取文本块
                blocks = page.get_text("blocks")
                
                # 处理文本块
                text_blocks = []
                for block in blocks:
                    # block 格式: (x0, y0, x1, y1, text, block_no, block_type)
                    if block[6] == 0:  # 文本块
                        text = block[4].strip()
                        if text:
                            text_blocks.append((block[1], text))  # (y坐标, 文本)
                
                # 按 y 坐标排序（从上到下）
                text_blocks.sort(key=lambda x: x[0])
                
                # 合并相邻文本块为段落
                current_paragraph = []
                last_y = None
                
                for y, text in text_blocks:
                    # 判断是否为新段落（y 坐标变化较大）
                    if last_y is not None and (y - last_y) > 20:
                        if current_paragraph:
                            para_text = " ".join(current_paragraph).strip()
                            if para_text:
                                total_words += len(para_text)
                                section = self._create_section(para_text, position, sections)
                                sections.append(section)
                                if not first_heading and section.type == SectionType.HEADING:
                                    first_heading = section.content
                                position += 1
                            current_paragraph = []
                    
                    current_paragraph.append(text)
                    last_y = y
                
                # 处理最后一个段落
                if current_paragraph:
                    para_text = " ".join(current_paragraph).strip()
                    if para_text:
                        total_words += len(para_text)
                        section = self._create_section(para_text, position, sections)
                        sections.append(section)
                        if not first_heading and section.type == SectionType.HEADING:
                            first_heading = section.content
                        position += 1
            
            # 构建元数据
            filename = Path(file_path).name
            metadata = DocumentMetadata(
                title=first_heading or filename,
                author="",
                word_count=total_words,
            )
            
            return Document(
                filename=filename,
                source_format="pdf",
                sections=sections,
                metadata=metadata,
            )
            
        except Exception as e:
            raise DocumentParseError(f"解析 PDF 文档失败: {str(e)}")

    def _create_section(self, text: str, position: int, existing_sections: list) -> DocumentSection:
        """创建文档段落"""
        section_type = SectionType.PARAGRAPH
        level = 0
        
        # 启发式判断标题（PDF中较短的、独占一行的文本可能是标题
        if len(text) < 50 and "\n" not in text:
            section_type = SectionType.HEADING
            has_heading = any(s.type == SectionType.HEADING for s in existing_sections)
            level = 1 if not has_heading else 2
        
        return DocumentSection(
            id=str(uuid.uuid4()),
            type=section_type,
            level=level,
            content=text,
            position=position,
        )
