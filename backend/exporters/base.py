"""
文件名：exporters/base.py
功能描述：文档导出器抽象基类。定义所有导出器必须实现的接口。
         所有导出器消费 IllustratedDocument 格式，输出指定格式的文件。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 抽象基类已定义，无需修改
"""

from abc import ABC, abstractmethod

from schemas.document import IllustratedDocument


class BaseExporter(ABC):
    """文档导出器抽象基类"""

    # 子类声明支持的导出格式，如 "docx"
    format_name: str = ""
    # 导出文件的 MIME 类型
    content_type: str = "application/octet-stream"
    # 文件扩展名
    file_extension: str = ""

    @abstractmethod
    async def export(self, illustrated_doc: IllustratedDocument, output_path: str) -> str:
        """
        将带插图的文档导出为指定格式。

        Args:
            illustrated_doc: 包含文档内容和插图的完整数据
            output_path: 导出文件保存路径

        Returns:
            实际导出文件的完整路径

        Raises:
            ExportError: 导出失败时抛出
        """
        ...
