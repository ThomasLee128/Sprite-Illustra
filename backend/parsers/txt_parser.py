"""
文件名：txt_parser.py
功能描述：纯文本文件（.txt）解析器。将纯文本按段落分割，
         识别空行分隔的段落，生成统一的 Document 结构。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 parse(self, file_path: str) -> Document

依赖：schemas.document, core.exceptions, uuid, pathlib
"""

import uuid
from pathlib import Path

from parsers.base import BaseParser
from parsers import register_parser
from schemas.document import Document, DocumentSection, DocumentMetadata, SectionType
from core.exceptions import DocumentParseError


@register_parser
class TxtParser(BaseParser):
    """纯文本文件解析器"""

    supported_extensions = [".txt"]

    async def parse(self, file_path: str) -> Document:
        """解析 .txt 文件"""
        try:
            # 尝试读取文件（优先 UTF-8，回退 GBK）
            content = ""
            for encoding in ["utf-8", "gbk", "gb2312", "latin-1"]:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if not content:
                raise DocumentParseError("无法读取文件内容或文件为空")
            
            # 按行分割
            lines = content.splitlines()
            sections: list[DocumentSection] = []
            current_paragraph = []
            position = 0
            first_heading = ""
            total_words = 0
            
            for line in lines:
                stripped_line = line.strip()
                
                if not stripped_line:
                    # 空行，结束当前段落
                    if current_paragraph:
                        # 处理当前段落
                        section_text = "\n".join(current_paragraph).strip()
                        if section_text:
                            total_words += len(section_text)
                            section = self._create_section(section_text, position, sections)
                            sections.append(section)
                            if not first_heading and section.type == SectionType.HEADING:
                                first_heading = section.content
                            position += 1
                        current_paragraph = []
                else:
                    current_paragraph.append(line)
            
            # 处理最后一个段落
            if current_paragraph:
                section_text = "\n".join(current_paragraph).strip()
                if section_text:
                    total_words += len(section_text)
                    section = self._create_section(section_text, position, sections)
                    sections.append(section)
                    if not first_heading and section.type == SectionType.HEADING:
                        first_heading = section.content
            
            # 构建元数据
            filename = Path(file_path).name
            metadata = DocumentMetadata(
                title=first_heading or filename,
                author="",
                word_count=total_words,
            )
            
            return Document(
                filename=filename,
                source_format="txt",
                sections=sections,
                metadata=metadata,
            )
            
        except FileNotFoundError:
            raise DocumentParseError("文件不存在")
        except Exception as e:
            raise DocumentParseError(f"解析 TXT 文件失败: {str(e)}")

    def _create_section(self, text: str, position: int, existing_sections: list) -> DocumentSection:
        """创建文档段落"""
        # 判断段落类型
        section_type = SectionType.PARAGRAPH
        level = 0
        
        # 检查是否为列表
        stripped = text.lstrip()
        if stripped.startswith(("- ", "* ", "• ")) or (stripped and stripped[0].isdigit() and stripped[1:].startswith((". ", ") "))):
            section_type = SectionType.LIST
        # 检查是否为标题（较短的单行）
        elif "\n" not in text and len(text) < 30:
            section_type = SectionType.HEADING
            # 第一个标题是 level 1，其他 level 2
            has_heading = any(s.type == SectionType.HEADING for s in existing_sections)
            level = 1 if not has_heading else 2
        
        return DocumentSection(
            id=str(uuid.uuid4()),
            type=section_type,
            level=level,
            content=text,
            position=position,
        )
