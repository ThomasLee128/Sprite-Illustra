"""
文件名：docx_parser.py
功能描述：Word 文档（.docx）解析器。使用 python-docx 库提取文档结构，
         识别标题、段落、列表等元素，生成统一的 Document 结构。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 parse(self, file_path: str) -> Document
      - 使用 python-docx 打开文件: doc = DocxDocument(file_path)
      - 遍历 doc.paragraphs，根据 paragraph.style.name 判断类型：
        * style.name 以 "Heading" 开头 -> HEADING（level 从 style.name 提取数字）
        * style.name 以 "List" 开头 -> LIST
        * 其他 -> PARAGRAPH
      - 跳过空段落（paragraph.text.strip() == ""）
      - 为每个 section 生成 UUID，设置递增的 position
      - 提取 metadata:
        * title = doc.core_properties.title 或第一个 HEADING
        * author = doc.core_properties.author
        * word_count = 所有段落文字总数
      - 返回 Document
      - 异常处理: 文件损坏/格式错误 -> raise DocumentParseError
依赖：python-docx (from docx import Document as DocxDocument), schemas.document, core.exceptions, uuid
"""

from parsers.base import BaseParser
from parsers import register_parser
from schemas.document import Document


@register_parser
class DocxParser(BaseParser):
    """Word 文档解析器"""

    supported_extensions = [".docx"]

    async def parse(self, file_path: str) -> Document:
        """解析 .docx 文件"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
