"""
文件名：exporters/__init__.py
功能描述：导出器注册表。通过 @register_exporter 装饰器自动注册导出器，
         通过 get_exporter(format_name) 获取对应导出器实例。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 注册机制已完成，无需修改
"""

from exporters.base import BaseExporter
from core.exceptions import ExportError

# 导出器注册表: {"docx": WordExporter, "pdf": PdfExporter, ...}
EXPORTER_REGISTRY: dict[str, type[BaseExporter]] = {}


def register_exporter(cls: type[BaseExporter]) -> type[BaseExporter]:
    """
    装饰器：自动将导出器注册到全局注册表。
    用法：
        @register_exporter
        class WordExporter(BaseExporter):
            format_name = "docx"
    """
    EXPORTER_REGISTRY[cls.format_name] = cls
    return cls


def get_exporter(format_name: str) -> BaseExporter:
    """
    根据格式名获取导出器实例。

    Args:
        format_name: 格式名，如 "docx"、"pdf"、"md"、"html"

    Raises:
        ExportError: 不支持的导出格式
    """
    fmt = format_name.lower()
    if fmt not in EXPORTER_REGISTRY:
        supported = ", ".join(EXPORTER_REGISTRY.keys())
        raise ExportError(f"不支持的导出格式: {fmt}（支持: {supported}）")
    return EXPORTER_REGISTRY[fmt]()


def get_supported_formats() -> list[str]:
    """返回所有支持的导出格式列表"""
    return list(EXPORTER_REGISTRY.keys())


# --- 导入所有导出器以触发注册 ---
from exporters.word_exporter import WordExporter    # noqa: E402, F401
from exporters.md_exporter import MdExporter        # noqa: E402, F401
from exporters.html_exporter import HtmlExporter    # noqa: E402, F401

# PDF 导出器 - 已启用
try:
    from exporters.pdf_exporter import PdfExporter  # noqa: E402, F401
except Exception as e:
    print(f"警告：PDF 导出器加载失败: {e}，将不支持 PDF 导出")
