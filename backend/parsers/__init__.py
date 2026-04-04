"""
文件名：parsers/__init__.py
功能描述：解析器注册表。通过 @register_parser 装饰器自动注册解析器，
         通过 get_parser(extension) 获取对应解析器实例。
         新增文件格式支持只需新建一个解析器文件并使用装饰器即可。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 注册机制已完成，无需修改
"""

from parsers.base import BaseParser
from core.exceptions import DocumentParseError

# 解析器注册表: {".txt": TxtParser, ".md": MdParser, ...}
PARSER_REGISTRY: dict[str, type[BaseParser]] = {}


def register_parser(cls: type[BaseParser]) -> type[BaseParser]:
    """
    装饰器：自动将解析器注册到全局注册表。
    用法：
        @register_parser
        class TxtParser(BaseParser):
            supported_extensions = [".txt"]
    """
    for ext in cls.supported_extensions:
        PARSER_REGISTRY[ext.lower()] = cls
    return cls


def get_parser(extension: str) -> BaseParser:
    """
    根据文件扩展名获取解析器实例。

    Args:
        extension: 文件扩展名，如 ".txt"、".docx"

    Returns:
        对应的解析器实例

    Raises:
        DocumentParseError: 不支持的文件格式
    """
    ext = extension.lower()
    if ext not in PARSER_REGISTRY:
        supported = ", ".join(PARSER_REGISTRY.keys())
        raise DocumentParseError(f"不支持的文件格式: {ext}（支持: {supported}）")
    return PARSER_REGISTRY[ext]()


def get_supported_extensions() -> list[str]:
    """返回所有支持的文件扩展名列表"""
    return list(PARSER_REGISTRY.keys())


# --- 导入所有解析器以触发注册 ---
from parsers.txt_parser import TxtParser      # noqa: E402, F401
from parsers.md_parser import MdParser        # noqa: E402, F401
from parsers.docx_parser import DocxParser    # noqa: E402, F401
from parsers.pdf_parser import PdfParser      # noqa: E402, F401
