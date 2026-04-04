"""
文件名：pdf_parser.py
功能描述：PDF 文件（.pdf）解析器。使用 PyMuPDF (fitz) 提取 PDF 文本内容，
         按页/块结构重组为段落，生成统一的 Document 结构。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] TODO-1: 实现 parse(self, file_path: str) -> Document
      - 使用 PyMuPDF 打开文件: doc = fitz.open(file_path)
      - 逐页提取文本块: page.get_text("blocks")
        * 每个 block 返回 (x0, y0, x1, y1, text, block_no, block_type)
        * block_type == 0 为文本块，跳过图片块（type==1）
      - 文本块处理：
        * 根据字体大小或文本长度启发式判断标题（较短且独占一块 -> HEADING）
        * 合并同页相邻的文本块为段落（当 y 坐标间距较小时）
        * 其他块 -> PARAGRAPH
      - 为每个 section 生成 UUID，设置递增的 position
      - metadata.title = 第一个 HEADING 或第一页前几行文本
      - 返回 Document
      - 注意: PDF 结构复杂，优先保证文本完整提取，结构识别可以偏保守
      - 异常处理: 加密PDF/损坏文件 -> raise DocumentParseError
依赖：PyMuPDF (import fitz), schemas.document, core.exceptions, uuid
"""

from parsers.base import BaseParser
from parsers import register_parser
from schemas.document import Document


@register_parser
class PdfParser(BaseParser):
    """PDF 文件解析器"""

    supported_extensions = [".pdf"]

    async def parse(self, file_path: str) -> Document:
        """解析 .pdf 文件"""
        # TODO-1
        raise NotImplementedError("待 Trea 实现")
