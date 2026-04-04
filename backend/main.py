"""
文件名：main.py
功能描述：FastAPI 应用入口。注册路由、中间件、全局异常处理器、生命周期事件。
         启动时初始化 OpenAI 客户端，关闭时清理资源。
         配置 CORS 允许前端跨域访问，挂载静态文件服务。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 应用初始化和路由注册已完成
- [ ] 根据实际部署需求调整 CORS 配置
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config import settings, DATA_DIR
from core.exceptions import AppException
from api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时初始化资源，关闭时清理"""
    # --- 启动 ---
    # 确保数据目录存在
    for sub in ["uploads", "images", "exports"]:
        (DATA_DIR / sub).mkdir(parents=True, exist_ok=True)
    yield
    # --- 关闭 ---
    # 清理资源（如关闭 httpx 客户端）


app = FastAPI(
    title="智灵智能插图",
    description="AI 驱动的文档智能配图工具",
    version="0.1.0",
    lifespan=lifespan,
)

# --- CORS 中间件 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite 开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 全局异常处理 ---
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


# --- 注册 API 路由 ---
app.include_router(api_router, prefix="/api")

# --- 挂载生成图片的静态文件服务 ---
app.mount("/api/images", StaticFiles(directory=str(DATA_DIR / "images")), name="images")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
