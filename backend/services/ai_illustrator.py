"""
文件名：ai_illustrator.py
功能描述：AI 图片生成服务。调用图片生成模型为每个插图位置生成配图。
         支持并发生成，使用 Semaphore 控制并发数，防止 API 限流。
         每完成一张图即推送进度到前端。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 generate_one(self, item, model, client, style_suffix) -> IllustrationItem
- [x] TODO-2: 实现 generate_all(self, illustrations, model, task_id) -> list[IllustrationItem]

依赖：core.openai_client, schemas.document, services.task_manager, config, asyncio
"""

import asyncio
import logging
from typing import List

logger = logging.getLogger(__name__)

from schemas.document import IllustrationItem, IllustrationStatus
from schemas.task import TaskPhase
from services.task_manager import task_manager
from config import settings
from core.openai_client import OpenAICompatibleClient


class AIIllustrator:
    """AI 图片生成服务"""

    # 风格后缀映射
    STYLE_SUFFIXES = {
        "flat": "flat vector illustration, clean lines, vibrant colors, white background",
        "realistic": "photorealistic, detailed, professional photography style",
        "watercolor": "watercolor painting style, soft edges, artistic",
        "sketch": "pencil sketch, line drawing, black and white",
        "cartoon": "cartoon style, colorful, fun, expressive",
        "tech": "technical diagram, clean infographic style, minimal colors",
    }

    async def generate_all(
        self, illustrations: list[IllustrationItem], model: str, task_id: str
    ) -> list[IllustrationItem]:
        """
        并发生成所有插图。

        Args:
            illustrations: 待生成的插图列表
            model: 图片模型 ID
            task_id: 任务 ID（用于推送进度）

        Returns:
            更新状态后的插图列表
        """
        logger.info(f"[AI 生图] 开始为任务 {task_id} 生成插图")
        logger.info(f"[AI 生图] 使用模型: {model}")
        logger.info(f"[AI 生图] 待生成插图数: {len(illustrations)}")
        
        if not illustrations:
            return illustrations
        
        # 初始化 OpenAI 客户端
        client = OpenAICompatibleClient(settings.api_base_url, settings.api_key)
        
        # 创建信号量控制并发
        semaphore = asyncio.Semaphore(settings.max_concurrent_generations)
        logger.info(f"[AI 生图] 最大并发数: {settings.max_concurrent_generations}")
        
        completed_count = 0
        total_count = len(illustrations)
        
        async def _generate_with_semaphore(item: IllustrationItem) -> IllustrationItem:
            nonlocal completed_count
            
            async with semaphore:
                logger.info(f"[AI 生图] 开始生成插图: {item.id[:8]}...")
                
                # 更新状态为生成中
                item.status = IllustrationStatus.GENERATING
                
                # 获取风格后缀
                style_suffix = self.STYLE_SUFFIXES.get(item.style.value, self.STYLE_SUFFIXES["flat"])
                
                try:
                    result_item = await self.generate_one(item, model, client, style_suffix)
                    logger.info(f"[AI 生图] 插图生成成功: {item.id[:8]}")
                except Exception as e:
                    logger.error(f"[AI 生图] 插图生成失败: {item.id[:8]}, 错误: {e}")
                    item.status = IllustrationStatus.FAILED
                    item.error_message = str(e)
                    result_item = item
                
                # 更新计数并推送进度
                completed_count += 1
                progress = 0.35 + (completed_count / total_count) * 0.6
                await task_manager.update_progress(
                    task_id,
                    TaskPhase.GENERATING,
                    progress,
                    f"已生成 {completed_count}/{total_count} 张插图",
                    {"completed_count": completed_count},
                )
                
                return result_item
        
        try:
            # 并发执行
            logger.info(f"[AI 生图] 开始并发生成 {total_count} 张插图...")
            tasks = [_generate_with_semaphore(item) for item in illustrations]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理结果
            final_illustrations = []
            success_count = 0
            fail_count = 0
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    illustrations[i].status = IllustrationStatus.FAILED
                    illustrations[i].error_message = str(result)
                    final_illustrations.append(illustrations[i])
                    fail_count += 1
                else:
                    final_illustrations.append(result)
                    if result.status == IllustrationStatus.DONE:
                        success_count += 1
                    else:
                        fail_count += 1
            
            logger.info(f"[AI 生图] 所有插图生成完成! 成功: {success_count}, 失败: {fail_count}")
            return final_illustrations
        finally:
            await client.close()

    async def generate_one(
        self, item: IllustrationItem, model: str, client, style_suffix: str
    ) -> IllustrationItem:
        """生成单张插图"""
        logger.debug(f"[AI 生图] 为插图 {item.id[:8]} 生成图片")
        
        # 构建最终 prompt
        final_prompt = f"{item.prompt}, {style_suffix}"
        
        logger.debug(f"[AI 生图] 最终 prompt: {final_prompt[:100]}...")
        
        # 调用图片生成
        logger.info(f"[AI 生图] 调用图片生成 API...")
        image_paths = await client.image_generation(
            model=model,
            prompt=final_prompt,
            size="1024x1024",
            n=1,
        )
        
        if image_paths:
            logger.info(f"[AI 生图] 图片生成成功，已保存到: {image_paths[0]}")
            item.image_path = image_paths[0]
            item.status = IllustrationStatus.DONE
        else:
            logger.error(f"[AI 生图] 图片生成失败，未返回图片")
            item.status = IllustrationStatus.FAILED
            item.error_message = "图片生成失败，未返回图片"
        
        return item


# 全局单例
ai_illustrator = AIIllustrator()
