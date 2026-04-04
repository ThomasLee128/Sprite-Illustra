"""
文件名：txt_parser.py
功能描述：纯文本文件（.txt）解析器。将纯文本按段落分割，
         识别空行分隔的段落，生成统一的 Document 结构。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 parse(self, file_path: str) -> Document
      - 读取文件（自动检测编码，优先 UTF-8，回退 GBK/GB2312）
      - 按空行分割为段落（连续的非空行为一个段落）
      - 判断段落类型：
        * 单行且字数较少（<30字）-> HEADING（level=1 如果是第一段，否则 level=2）
        * 以 "- " 或 "* " 或 "1. " 开头 -> LIST
        * 其他 -> PARAGRAPH
      - 为每个段落生成 UUID 作为 id
      - 计算 metadata（title=第一个 HEADING 的内容，word_count=总字数）
      - 返回 Document 实例
      - 异常处理: 文件不存在/编码错误 -> raise DocumentParseError
依赖：schemas.document, core.exceptions, uuid, pathlib
"""

from parsers.base import BaseParser
from parsers import register_parser
from schemas.document import Document


@register_parser
class TxtParser(BaseParser):
    """纯文本文件解析器"""

    supported_extensions = [".txt"]

    async def parse(self, file_path: str) -> Document:
        """解析 .txt 文件"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
