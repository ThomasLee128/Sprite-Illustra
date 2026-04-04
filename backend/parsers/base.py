"""
文件名：base.py
功能描述：文档解析器抽象基类。定义所有解析器必须实现的接口。
         所有解析器将文档转换为统一的 Document 中间表示格式。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 抽象基类已定义，无需修改
"""

from abc import ABC, abstractmethod

from schemas.document import Document


class BaseParser(ABC):
    """文档解析器抽象基类"""

    # 子类必须声明支持的文件扩展名，如 [".txt"]
    supported_extensions: list[str] = []

    @abstractmethod
    async def parse(self, file_path: str) -> Document:
        """
        解析文件，返回统一的 Document 结构。

        Args:
            file_path: 上传文件的本地路径

        Returns:
            Document: 包含 sections 列表的统一文档结构

        Raises:
            DocumentParseError: 解析失败时抛出
        """
        ...
