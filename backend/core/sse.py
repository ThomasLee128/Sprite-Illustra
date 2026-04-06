"""
文件名：sse.py
功能描述：Server-Sent Events (SSE) 工具函数，用于向前端实时推送任务处理进度。
         封装 FastAPI 的 StreamingResponse，提供标准 SSE 事件格式化方法。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] 实现 format_sse_event(event, data) -> str
- [x] 实现 create_sse_response(event_generator) -> StreamingResponse
- [x] 实现心跳机制（每 30 秒发送 ": keepalive\n\n" 注释行，防止连接超时断开）
依赖：fastapi.responses.StreamingResponse, json, asyncio
"""

import json
import asyncio
from typing import AsyncIterator, Any
from fastapi.responses import StreamingResponse


def format_sse_event(event: str, data: dict[str, Any]) -> str:
    """
    将事件名和数据格式化为 SSE 标准格式
    
    Args:
        event: 事件名称
        data: 事件数据（字典）
    
    Returns:
        SSE 格式字符串
    """
    data_json = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {data_json}\n\n"


async def sse_event_generator(
    source_generator: AsyncIterator[dict],
    heartbeat_interval: float = 30.0
) -> AsyncIterator[str]:
    """
    包装源事件生成器，添加心跳机制
    
    Args:
        source_generator: 原始事件生成器
        heartbeat_interval: 心跳间隔（秒）
    
    Yields:
        SSE 格式的事件字符串
    """
    last_heartbeat = asyncio.get_event_loop().time()
    
    try:
        async for event_data in source_generator:
            # 发送事件
            yield format_sse_event("message", event_data)
            
            # 更新最后心跳时间
            last_heartbeat = asyncio.get_event_loop().time()
            
            # 检查是否需要发送心跳
            current_time = asyncio.get_event_loop().time()
            if current_time - last_heartbeat >= heartbeat_interval:
                yield ": keepalive\n\n"
                last_heartbeat = current_time
    except asyncio.CancelledError:
        # 客户端断开连接
        pass


def create_sse_response(event_generator: AsyncIterator[dict]) -> StreamingResponse:
    """
    创建 SSE 响应
    
    Args:
        event_generator: 事件生成器（AsyncIterator[dict]）
    
    Returns:
        FastAPI StreamingResponse
    """
    async def wrapped_generator():
        async for event in sse_event_generator(event_generator):
            yield event
    
    return StreamingResponse(
        wrapped_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
