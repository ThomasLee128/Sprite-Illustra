"""
文件名：md_parser.py
功能描述：Markdown 文件（.md）解析器。利用 Markdown 语法规则精准识别
         标题、段落、列表、代码块、引用块等结构，生成统一的 Document 结构。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 parse(self, file_path: str) -> Document

依赖：schemas.document, core.exceptions, uuid, pathlib
"""

import uuid
import re
from pathlib import Path

from parsers.base import BaseParser
from parsers import register_parser
from schemas.document import Document, DocumentSection, DocumentMetadata, SectionType
from core.exceptions import DocumentParseError


@register_parser
class MdParser(BaseParser):
    """Markdown 文件解析器"""

    supported_extensions = [".md", ".markdown"]

    async def parse(self, file_path: str) -> Document:
        """解析 .md 文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            lines = content.splitlines()
            sections: list[DocumentSection] = []
            position = 0
            first_heading = ""
            total_words = 0
            
            # 状态追踪
            in_code_block = False
            code_block_content = []
            current_list_content = []
            current_paragraph_content = []
            current_blockquote_content = []
            
            for line in lines:
                stripped_line = line.strip()
                
                # 代码块处理
                if stripped_line.startswith("```"):
                    if in_code_block:
                        # 结束代码块
                        if code_block_content:
                            code_text = "\n".join(code_block_content)
                            total_words += len(code_text)
                            section = DocumentSection(
                                id=str(uuid.uuid4()),
                                type=SectionType.CODE,
                                level=0,
                                content=code_text,
                                position=position,
                            )
                            sections.append(section)
                            position += 1
                        code_block_content = []
                        in_code_block = False
                    else:
                        # 开始代码块
                        self._flush_current_content(
                            sections, current_paragraph_content, current_list_content, 
                            current_blockquote_content, position, first_heading, total_words
                        )
                        in_code_block = True
                elif in_code_block:
                    code_block_content.append(line)
                else:
                    # 普通内容处理
                    if not stripped_line:
                        # 空行，刷新当前内容
                        self._flush_current_content(
                            sections, current_paragraph_content, current_list_content, 
                            current_blockquote_content, position, first_heading, total_words
                        )
                    elif stripped_line.startswith("#"):
                        # 标题
                        self._flush_current_content(
                            sections, current_paragraph_content, current_list_content, 
                            current_blockquote_content, position, first_heading, total_words
                        )
                        level = len(stripped_line) - len(stripped_line.lstrip("#"))
                        heading_text = stripped_line.lstrip("#").strip()
                        total_words += len(heading_text)
                        section = DocumentSection(
                            id=str(uuid.uuid4()),
                            type=SectionType.HEADING,
                            level=min(level, 6),
                            content=heading_text,
                            position=position,
                        )
                        sections.append(section)
                        if not first_heading:
                            first_heading = heading_text
                        position += 1
                    elif stripped_line.startswith(">"):
                        # 引用块
                        if not current_blockquote_content:
                            self._flush_current_content(
                                sections, current_paragraph_content, current_list_content, 
                                [], position, first_heading, total_words
                            )
                        quote_text = stripped_line[1:].strip()
                        current_blockquote_content.append(quote_text)
                    elif stripped_line.startswith(("- ", "* ", "+ ")) or (
                        stripped_line and stripped_line[0].isdigit() and stripped_line[1:].startswith((". ", ") "))
                    ):
                        # 列表项
                        if not current_list_content:
                            self._flush_current_content(
                                sections, current_paragraph_content, [], 
                                current_blockquote_content, position, first_heading, total_words
                            )
                        current_list_content.append(stripped_line)
                    else:
                        # 普通段落
                        if not current_paragraph_content:
                            self._flush_current_content(
                                sections, [], current_list_content, 
                                current_blockquote_content, position, first_heading, total_words
                            )
                        current_paragraph_content.append(line)
            
            # 刷新最后的内容
            self._flush_current_content(
                sections, current_paragraph_content, current_list_content, 
                current_blockquote_content, position, first_heading, total_words
            )
            
            # 构建元数据
            filename = Path(file_path).name
            metadata = DocumentMetadata(
                title=first_heading or filename,
                author="",
                word_count=total_words,
            )
            
            return Document(
                filename=filename,
                source_format="md",
                sections=sections,
                metadata=metadata,
            )
            
        except FileNotFoundError:
            raise DocumentParseError("文件不存在")
        except Exception as e:
            raise DocumentParseError(f"解析 Markdown 文件失败: {str(e)}")

    def _flush_current_content(
        self,
        sections: list[DocumentSection],
        paragraph_content: list[str],
        list_content: list[str],
        blockquote_content: list[str],
        position: int,
        first_heading: str,
        total_words: int,
    ) -> None:
        """刷新当前缓冲的内容到 sections"""
        if paragraph_content:
            text = "\n".join(paragraph_content).strip()
            if text:
                total_words += len(text)
                section = DocumentSection(
                    id=str(uuid.uuid4()),
                    type=SectionType.PARAGRAPH,
                    level=0,
                    content=text,
                    position=position,
                )
                sections.append(section)
                position += 1
            paragraph_content.clear()
        
        if list_content:
            text = "\n".join(list_content).strip()
            if text:
                total_words += len(text)
                section = DocumentSection(
                    id=str(uuid.uuid4()),
                    type=SectionType.LIST,
                    level=0,
                    content=text,
                    position=position,
                )
                sections.append(section)
                position += 1
            list_content.clear()
        
        if blockquote_content:
            text = "\n".join(blockquote_content).strip()
            if text:
                total_words += len(text)
                section = DocumentSection(
                    id=str(uuid.uuid4()),
                    type=SectionType.BLOCKQUOTE,
                    level=0,
                    content=text,
                    position=position,
                )
                sections.append(section)
                position += 1
            blockquote_content.clear()
