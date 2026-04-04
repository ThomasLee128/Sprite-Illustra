"""
文件名：document.py
功能描述：文档相关的核心数据模型。定义统一的文档中间表示结构，
         包括文档段落（DocumentSection）、完整文档（Document）、
         插图条目（IllustrationItem）、带插图的完整文档（IllustratedDocument）。
         所有解析器输出 Document 格式，所有导出器消费 IllustratedDocument 格式。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 核心数据模型已完成
- [ ] 如需扩展字段（如图片尺寸、插图标题等），在此添加
"""

from enum import Enum
from pydantic import BaseModel, Field


class SectionType(str, Enum):
    """段落类型"""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    CODE = "code"
    BLOCKQUOTE = "blockquote"


class IllustrationStatus(str, Enum):
    """插图生成状态"""
    PENDING = "pending"
    GENERATING = "generating"
    DONE = "done"
    FAILED = "failed"


class IllustrationStyle(str, Enum):
    """插图风格"""
    FLAT = "flat"               # 扁平矢量风
    REALISTIC = "realistic"     # 写实风
    WATERCOLOR = "watercolor"   # 水彩风
    SKETCH = "sketch"           # 素描/线稿
    CARTOON = "cartoon"         # 卡通风
    TECH = "tech"               # 科技/示意图风


class DocumentSection(BaseModel):
    """文档段落 - 统一中间表示的基本单元"""
    id: str = Field(description="段落唯一 ID（UUID）")
    type: SectionType = Field(description="段落类型")
    level: int = Field(default=0, description="标题层级，1-6，仅 HEADING 类型有效")
    content: str = Field(description="段落文本内容")
    position: int = Field(description="在原文档中的顺序位置（0-based）")


class DocumentMetadata(BaseModel):
    """文档元信息"""
    title: str = Field(default="", description="文档标题")
    author: str = Field(default="", description="文档作者")
    word_count: int = Field(default=0, description="总字数")


class Document(BaseModel):
    """解析后的完整文档 - 所有解析器的统一输出格式"""
    filename: str = Field(description="原始文件名")
    source_format: str = Field(description="原始格式: txt / md / docx / pdf")
    sections: list[DocumentSection] = Field(default_factory=list, description="段落列表")
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata, description="元信息")


class IllustrationItem(BaseModel):
    """一张插图的完整信息"""
    id: str = Field(description="插图唯一 ID（UUID）")
    after_section_id: str = Field(description="插入到哪个段落之后")
    prompt: str = Field(description="给图片模型的英文 prompt")
    style: IllustrationStyle = Field(default=IllustrationStyle.FLAT, description="插图风格")
    description_cn: str = Field(default="", description="中文描述（展示给用户）")
    reason: str = Field(default="", description="为什么在此处插图")
    image_path: str | None = Field(default=None, description="生成后的图片本地路径")
    status: IllustrationStatus = Field(default=IllustrationStatus.PENDING, description="生成状态")
    error_message: str = Field(default="", description="失败时的错误信息")


class IllustratedDocument(BaseModel):
    """带插图的完整文档 - 所有导出器的统一输入格式"""
    document: Document = Field(description="解析后的文档")
    illustrations: list[IllustrationItem] = Field(default_factory=list, description="插图列表")
