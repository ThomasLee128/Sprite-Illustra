"""
文件名：exceptions.py
功能描述：自定义异常类，统一全局错误处理。
         包括 API 调用异常、文档解析异常、导出异常等。
         在 main.py 中注册全局异常处理器，将这些异常转为标准 HTTP 响应。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 基础异常类已定义
- [ ] 如需更细粒度的错误码，可在此扩展
"""


class AppException(Exception):
    """应用基础异常"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class APIClientError(AppException):
    """AI API 调用失败（网络错误、认证失败、限流等）"""

    def __init__(self, message: str = "AI API 调用失败"):
        super().__init__(message, status_code=502)


class DocumentParseError(AppException):
    """文档解析失败（格式不支持、文件损坏等）"""

    def __init__(self, message: str = "文档解析失败"):
        super().__init__(message, status_code=400)


class ExportError(AppException):
    """文档导出失败"""

    def __init__(self, message: str = "文档导出失败"):
        super().__init__(message, status_code=500)


class TaskNotFoundError(AppException):
    """任务不存在"""

    def __init__(self, task_id: str):
        super().__init__(f"任务不存在: {task_id}", status_code=404)


class SettingsError(AppException):
    """配置错误（如未设置 API Key）"""

    def __init__(self, message: str = "请先在设置页面配置 API 地址和密钥"):
        super().__init__(message, status_code=400)
