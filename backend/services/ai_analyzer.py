"""
文件名：ai_analyzer.py
功能描述：AI 内容分析服务。调用文本大模型分析文档内容，
         智能确定适合插入插图的位置，并生成图片描述 prompt。
         这是整个系统的核心价值所在。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 _build_analysis_prompt(self, sections) -> list[dict]
- [x] TODO-2: 实现 analyze(self, document, model, task_id) -> list[IllustrationItem]
- [x] TODO-3: 实现 _parse_model_response(self, response_text) -> list[dict]

依赖：core.openai_client, schemas.document, services.task_manager, config, json, re, uuid
"""

import uuid
import json
import re
from typing import Any
import logging

logger = logging.getLogger(__name__)

from schemas.document import Document, IllustrationItem, IllustrationStyle, IllustrationStatus
from schemas.task import TaskPhase
from services.task_manager import task_manager
from config import settings
from core.openai_client import OpenAICompatibleClient
from core.exceptions import SettingsError


class AIAnalyzer:
    """AI 内容分析服务"""

    async def analyze(
        self, document: Document, model: str, task_id: str, is_ppt_mode: bool = False
    ) -> list[IllustrationItem]:
        """
        分析文档内容，确定插图位置和描述。

        Args:
            document: 解析后的文档
            model: 文本模型 ID
            task_id: 任务 ID（用于推送进度）

        Returns:
            插图条目列表（status=PENDING）
        """
        logger.info(f"[AI 分析] 开始分析任务: {task_id}")
        
        from services.task_manager import task_manager
        from schemas.task import TaskPhase
        logger.info(f"[AI 分析] 使用模型: {model}")
        
        if not settings.api_base_url or not settings.api_key:
            raise SettingsError("请先配置 API 地址和密钥")
        
        # 按约 4000 字分段处理
        sections = document.sections
        logger.info(f"[AI 分析] 文档总段落数: {len(sections)}")
        
        chunk_size = 4000
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for section in sections:
            section_words = len(section.content)
            if current_word_count + section_words > chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_word_count = 0
            current_chunk.append(section)
            current_word_count += section_words
        
        if current_chunk:
            chunks.append(current_chunk)
        
        logger.info(f"[AI 分析] 文档分为 {len(chunks)} 个 chunk 进行分析")
        
        all_illustrations = []
        
        # 分批分析
        for i, chunk_sections in enumerate(chunks):
            logger.info(f"[AI 分析] 正在处理 chunk {i+1}/{len(chunks)}...")
            # 推送进度
            progress = 0.15 + (i / len(chunks)) * 0.15
            await task_manager.update_progress(
                task_id,
                TaskPhase.ANALYZING,
                progress,
                f"正在分析文档内容 ({i+1}/{len(chunks)})...",
            )
            
            # 构建 prompt 并调用 AI
            client = OpenAICompatibleClient(settings.api_base_url, settings.api_key)
            try:
                messages = self._build_analysis_prompt(chunk_sections, is_ppt_mode)
                logger.info(f"[AI 分析] 调用 OpenAI API...")
                
                response_text = await client.chat_completion(
                    model=model,
                    messages=messages,
                    response_format={"type": "json_object"},
                )
                
                logger.info(f"[AI 分析] API 响应已收到!")
                logger.debug(f"[AI 分析] 响应内容: {response_text[:200]}...")
                
                # 解析响应
                chunk_illustrations = self._parse_model_response(response_text)
                logger.info(f"[AI 分析] 本 chunk 找到 {len(chunk_illustrations)} 个插图")
                
                # 调整段落位置偏移（基于 chunk 在整个文档中的位置）
                chunk_start_position = chunk_sections[0].position if chunk_sections else 0
                for illu in chunk_illustrations:
                    illu["after_section"] += chunk_start_position
                
                all_illustrations.extend(chunk_illustrations)
            except Exception as e:
                logger.error(f"[AI 分析] 处理 chunk {i+1} 时出错: {e}")
                import traceback
                traceback.print_exc()
            finally:
                await client.close()
        
        # 构建 IllustrationItem 列表
        illustration_items = []
        
        # 创建 position -> section.id 的映射
        position_to_id = {s.position: s.id for s in sections}
        
        for illu_data in all_illustrations:
            after_section_pos = illu_data.get("after_section", 0)
            
            # 找到对应的 section id
            after_section_id = position_to_id.get(after_section_pos, sections[-1].id if sections else "")
            
            # 解析风格
            style_str = illu_data.get("style", "flat")
            try:
                style = IllustrationStyle(style_str)
            except ValueError:
                style = IllustrationStyle.FLAT
            
            item = IllustrationItem(
                id=str(uuid.uuid4()),
                after_section_id=after_section_id,
                prompt=illu_data.get("prompt", ""),
                style=style,
                description_cn=illu_data.get("description_cn", ""),
                reason=illu_data.get("reason", ""),
                image_path=None,
                status=IllustrationStatus.PENDING,
                error_message="",
            )
            illustration_items.append(item)
        
        return illustration_items

    def _build_analysis_prompt(self, sections: list, is_ppt_mode: bool = False) -> list[dict]:
        """构建发送给文本模型的 prompt"""
        # 构建带编号的文本
        numbered_text = ""
        for section in sections:
            prefix = f"[{section.position}]"
            numbered_text += f"{prefix} {section.content}\n"
        
        if is_ppt_mode:
            system_prompt = """你是一个专业的PPT设计师。你的任务是阅读以下编号段落，
将每一段内容都做成一张PPT页面。每张PPT要包含：
1. 完整的段落内容
2. 合适的背景和配色
3. 清晰的排版
4. 一张配图（插画或示意图）

重要要求：
- 首先检测文档内容的主要语言（中文、英文或其他）
- PPT页面中的所有文字内容必须使用该主要语言
- 避免在中文文档中出现全英文的PPT页面
- 每个段落都要做成一张独立的PPT
- prompt描述要具体，包含：完整的文字内容、配图风格、排版布局、配色方案
- 以严格 JSON 格式返回

返回格式：
{"illustrations": [
  {"after_section": 段落编号, "description_cn": "PPT页面说明",
   "prompt": "English prompt for PPT page image generation: \\
   [在此处添加完整的段落内容（使用文档主要语言）]，\\
   搭配合适的插画或示意图，\\
   采用清晰美观的排版布局，\\
   专业的商务风格，\\
   所有文字内容使用[文档主要语言，如中文/English]",
   "style": "tech",
   "reason": "作为PPT页面"}
]}"""
        else:
            system_prompt = """你是一个专业的文档插图编辑。你的任务是阅读以下编号段落，
判断哪些位置适合插入说明性插图。考虑以下场景适合插图：
1. 概念解释处（用图示帮助读者理解）
2. 流程描述处（流程图或示意图）
3. 数据对比处（图表或对比图）
4. 章节转换处（过渡性配图）
5. 复杂操作步骤处（操作示意图）

重要要求：
- 首先检测文档内容的主要语言（中文、英文或其他）
- 如果插图中有文字，必须使用该主要语言
- 避免在中文文档中出现全英文的插图
- 不要在每个段落后都插图，选择最有价值的 3~8 个位置
- 每张插图给出详细的英文描述 prompt（便于图片 AI 生成）
- prompt 描述要具体，包含画面内容、风格、色调，以及"文字使用[文档主要语言]"的要求
- 以严格 JSON 格式返回

返回格式：
{"illustrations": [
  {"after_section": 段落编号, "description_cn": "中文说明",
   "prompt": "English prompt for image generation, all text in the image should use [文档主要语言，如Chinese/English]",
   "style": "flat/tech",
   "reason": "为什么在此处插图"}
]}"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": numbered_text},
        ]

    def _parse_model_response(self, response_text: str) -> list[dict]:
        """解析模型返回的 JSON 结果"""
        # 尝试直接解析
        try:
            data = json.loads(response_text)
            illustrations = data.get("illustrations", [])
            if isinstance(illustrations, list):
                return self._filter_illustrations(illustrations)
        except json.JSONDecodeError:
            pass
        
        # 尝试提取 JSON 块
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                illustrations = data.get("illustrations", [])
                if isinstance(illustrations, list):
                    return self._filter_illustrations(illustrations)
            except json.JSONDecodeError:
                pass
        
        # 尝试直接找 { ... }
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                illustrations = data.get("illustrations", [])
                if isinstance(illustrations, list):
                    return self._filter_illustrations(illustrations)
            except json.JSONDecodeError:
                pass
        
        return []

    def _filter_illustrations(self, illustrations: list[dict]) -> list[dict]:
        """过滤无效的插图条目"""
        valid = []
        for illu in illustrations:
            if not isinstance(illu, dict):
                continue
            if "after_section" not in illu or not isinstance(illu["after_section"], int):
                continue
            if "prompt" not in illu or not isinstance(illu["prompt"], str):
                continue
            valid.append(illu)
        return valid


# 全局单例
ai_analyzer = AIAnalyzer()
