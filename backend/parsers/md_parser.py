"""
文件名：md_parser.py
功能描述：Markdown 文件（.md）解析器。利用 Markdown 语法规则精准识别
         标题、段落、列表、代码块、引用块等结构，生成统一的 Document 结构。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 parse(self, file_path: str) -> Document
      - 读取文件（UTF-8 编码）
      - 逐行扫描，识别 Markdown 结构：
        * "# " ~ "###### " 开头 -> HEADING（level 对应 # 的数量）
        * "- " / "* " / "1. " 开头 -> LIST（相邻列表项合并为一个 section）
        * "```" 包裹的块 -> CODE（将整个代码块合并为一个 section）
        * "> " 开头 -> BLOCKQUOTE
        * 其他非空行 -> PARAGRAPH（相邻的普通文本行合并为一个段落）
        * 空行作为段落分隔符
      - 为每个 section 生成 UUID，设置递增的 position
      - metadata.title = 第一个 HEADING 的内容
      - 返回 Document
      - 异常处理: 文件不存在 -> raise DocumentParseError
依赖：schemas.document, core.exceptions, uuid, pathlib
"""

from parsers.base import BaseParser
from parsers import register_parser
from schemas.document import Document


@register_parser
class MdParser(BaseParser):
    """Markdown 文件解析器"""

    supported_extensions = [".md", ".markdown"]

    async def parse(self, file_path: str) -> Document:
        """解析 .md 文件"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
