"""
文件名：document_service.py
功能描述：文档处理主编排服务。串联文档处理的完整流程：
         解析 -> AI 分析 -> AI 生图 -> 组装 IllustratedDocument。
         作为后台异步任务运行，通过 task_manager 推送进度。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [x] TODO-1: 实现 process_document(self, task_id, file_path, text_model, image_model, style)
- [x] TODO-2: 实现 get_result(self, task_id) -> IllustratedDocument
- [x] TODO-3: 实现 regenerate_illustration(self, task_id, illustration_id, new_prompt)
- [x] TODO-4: 实现 remove_illustration(self, task_id, illustration_id)
- [x] TODO-5: 实现 move_illustration(self, task_id, illustration_id, after_section_id)

依赖：parsers, services.ai_analyzer, services.ai_illustrator, services.task_manager,
      schemas.document, core.exceptions, asyncio
"""

import traceback
import json
import pickle
from pathlib import Path

from parsers import get_parser
from services.ai_analyzer import ai_analyzer
from services.ai_illustrator import ai_illustrator
from services.task_manager import task_manager
from schemas.document import Document, IllustratedDocument, IllustrationItem, IllustrationStatus
from schemas.task import TaskPhase
from core.exceptions import TaskNotFoundError

# 临时数据存储目录
DATA_DIR = Path(__file__).parent.parent / "data"
TEMP_DATA_DIR = DATA_DIR / "temp"
TEMP_DATA_DIR.mkdir(parents=True, exist_ok=True)


class DocumentService:
    """文档处理主编排服务"""

    def __init__(self):
        self._results: dict[str, IllustratedDocument] = {}
        self._temp_illustrations: dict[str, list] = {}
        self._temp_document: dict[str, Document] = {}
        # 启动时从文件加载临时数据
        self._load_temp_data()

    def _get_temp_files(self, task_id: str) -> tuple[Path, Path]:
        """获取临时数据文件路径"""
        doc_file = TEMP_DATA_DIR / f"{task_id}_document.pkl"
        illu_file = TEMP_DATA_DIR / f"{task_id}_illustrations.pkl"
        return doc_file, illu_file
    
    def _get_result_file(self, task_id: str) -> Path:
        """获取最终结果文件路径"""
        return TEMP_DATA_DIR / f"{task_id}_result.pkl"

    def _save_temp_data(self, task_id: str) -> None:
        """保存临时数据到文件"""
        doc_file, illu_file = self._get_temp_files(task_id)
        if task_id in self._temp_document:
            with open(doc_file, "wb") as f:
                pickle.dump(self._temp_document[task_id], f)
        if task_id in self._temp_illustrations:
            with open(illu_file, "wb") as f:
                pickle.dump(self._temp_illustrations[task_id], f)

    def _load_temp_data(self) -> None:
        """从文件加载所有临时数据"""
        for pkl_file in TEMP_DATA_DIR.glob("*.pkl"):
            try:
                task_id = pkl_file.stem.replace("_document", "").replace("_illustrations", "")
                if "document" in pkl_file.stem and task_id not in self._temp_document:
                    with open(pkl_file, "rb") as f:
                        self._temp_document[task_id] = pickle.load(f)
                elif "illustrations" in pkl_file.stem and task_id not in self._temp_illustrations:
                    with open(pkl_file, "rb") as f:
                        self._temp_illustrations[task_id] = pickle.load(f)
            except Exception as e:
                print(f"[警告] 加载临时数据失败 {pkl_file}: {e}")

    def _save_result(self, task_id: str) -> None:
        """保存最终结果到文件"""
        import logging
        logger = logging.getLogger(__name__)
        
        result_file = self._get_result_file(task_id)
        print(f"[文档服务] 尝试保存结果到文件: {result_file}")
        logger.info(f"[文档服务] 尝试保存结果到文件: {result_file}")
        
        # 确保目录存在
        result_file.parent.mkdir(parents=True, exist_ok=True)
        
        if task_id in self._results:
            try:
                print(f"[文档服务] 任务 {task_id} 在 _results 中，开始保存...")
                with open(result_file, "wb") as f:
                    pickle.dump(self._results[task_id], f)
                print(f"[文档服务] 结果保存成功: {result_file}")
                logger.info(f"[文档服务] 结果保存成功: {result_file}")
            except Exception as e:
                print(f"[文档服务] 结果保存失败: {e}")
                logger.error(f"[文档服务] 结果保存失败: {e}")
        else:
            print(f"[文档服务] 任务 {task_id} 不在 _results 中，无法保存")
            logger.warning(f"[文档服务] 任务 {task_id} 不在 _results 中，无法保存")
    
    def _load_temp_data(self) -> None:
        """从文件加载所有临时数据（包括临时数据和最终结果）"""
        for pkl_file in TEMP_DATA_DIR.glob("*.pkl"):
            try:
                task_id = pkl_file.stem.replace("_document", "").replace("_illustrations", "").replace("_result", "")
                if "document" in pkl_file.stem and task_id not in self._temp_document:
                    with open(pkl_file, "rb") as f:
                        self._temp_document[task_id] = pickle.load(f)
                elif "illustrations" in pkl_file.stem and task_id not in self._temp_illustrations:
                    with open(pkl_file, "rb") as f:
                        self._temp_illustrations[task_id] = pickle.load(f)
                elif "result" in pkl_file.stem and task_id not in self._results:
                    with open(pkl_file, "rb") as f:
                        self._results[task_id] = pickle.load(f)
            except Exception as e:
                print(f"[警告] 加载临时数据失败 {pkl_file}: {e}")
    
    def _delete_temp_data(self, task_id: str) -> None:
        """删除临时数据文件"""
        doc_file, illu_file = self._get_temp_files(task_id)
        for f in [doc_file, illu_file]:
            if f.exists():
                f.unlink()

    async def process_document(
        self,
        task_id: str,
        file_path: str,
        text_model: str,
        image_model: str,
        style: str = "flat",
        is_ppt_mode: bool = False,
    ) -> None:
        """主编排：解析 -> 分析 -> 生图 -> 组装（后台异步运行）"""
        try:
            # 阶段 1: 文档解析
            await task_manager.update_progress(
                task_id,
                TaskPhase.PARSING,
                0.05,
                "正在解析文档...",
            )
            
            ext = Path(file_path).suffix.lower()
            parser = get_parser(ext)
            document = await parser.parse(file_path)
            
            await task_manager.update_progress(
                task_id,
                TaskPhase.PARSING,
                0.1,
                "文档解析完成",
            )
            
            # 阶段 2: AI 内容分析
            await task_manager.update_progress(
                task_id,
                TaskPhase.ANALYZING,
                0.15,
                "AI 正在分析文档内容...",
            )
            
            illustrations = await ai_analyzer.analyze(document, text_model, task_id, is_ppt_mode)
            
            # 更新插图数量
            task_state = await task_manager.get_task(task_id)
            task_state.illustration_count = len(illustrations)
            task_state.text_model = text_model
            task_state.image_model = image_model
            
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info(f"[文档服务] AI 分析完成，找到 {len(illustrations)} 个插图")
            
            # 保存分析结果用于预览
            self._temp_illustrations[task_id] = illustrations
            self._temp_document[task_id] = document
            
            # 持久化临时数据到文件
            self._save_temp_data(task_id)
            
            logger.info(f"[文档服务] 已保存临时数据，准备进入预览阶段")
            
            # 进入预览阶段，等待用户确认
            await task_manager.update_progress(
                task_id,
                TaskPhase.PREVIEW,
                0.3,
                f"分析完成，计划生成 {len(illustrations)} 张插图，请确认预览",
            )
            
            logger.info(f"[文档服务] 已进入预览阶段")
            
        except Exception as e:
            error_msg = str(e)
            traceback.print_exc()
            await task_manager.mark_failed(task_id, error_msg)

    async def get_result(self, task_id: str) -> IllustratedDocument:
        """获取处理结果（包含完整图片路径，用于导出）"""
        import logging
        logger = logging.getLogger(__name__)
        
        # 如果内存中没有，尝试从文件加载
        if task_id not in self._results:
            result_file = self._get_result_file(task_id)
            if result_file.exists():
                try:
                    logger.info(f"[文档服务] 从文件加载结果: {task_id}")
                    with open(result_file, "rb") as f:
                        self._results[task_id] = pickle.load(f)
                    logger.info(f"[文档服务] 结果加载成功")
                except Exception as e:
                    logger.error(f"[文档服务] 加载结果失败: {e}")
        
        if task_id not in self._results:
            raise TaskNotFoundError(task_id)
        
        result = self._results[task_id]
        logger.info(f"[文档服务] 返回结果，共有 {len(result.illustrations)} 个插图")
        for illu in result.illustrations:
            logger.info(f"  - {illu.id}: status={illu.status}, image_path={illu.image_path}")
        
        return result

    async def regenerate_illustration(
        self, task_id: str, illustration_id: str, new_prompt: str | None = None
    ) -> None:
        """重新生成指定插图（异步执行）"""
        if task_id not in self._results:
            raise TaskNotFoundError(task_id)
        
        illustrated_doc = self._results[task_id]
        
        # 找到对应的插图
        target_item = None
        for item in illustrated_doc.illustrations:
            if item.id == illustration_id:
                target_item = item
                break
        
        if not target_item:
            raise ValueError("插图不存在")
        
        # 更新 prompt（如果提供）
        if new_prompt:
            target_item.prompt = new_prompt
        
        # 设置为生成中状态
        target_item.status = IllustrationStatus.GENERATING
        target_item.image_path = None
        
        # 立即保存当前状态（显示正在生成）
        self._save_result(task_id)
        
        # 在后台执行实际的图片生成
        import asyncio
        asyncio.create_task(self._do_regenerate(task_id, illustration_id))
    
    async def _do_regenerate(self, task_id: str, illustration_id: str) -> None:
        """后台执行重新生成"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            illustrated_doc = self._results[task_id]
            
            # 找到对应的插图
            target_item = None
            for item in illustrated_doc.illustrations:
                if item.id == illustration_id:
                    target_item = item
                    break
            
            if not target_item:
                logger.error(f"插图不存在: {illustration_id}")
                return
            
            # 重新生成
            from config import settings
            from core.openai_client import OpenAICompatibleClient
            
            client = OpenAICompatibleClient(settings.api_base_url, settings.api_key)
            try:
                style_suffix = ai_illustrator.STYLE_SUFFIXES.get(
                    target_item.style.value, 
                    ai_illustrator.STYLE_SUFFIXES["flat"]
                )
                
                task_state = await task_manager.get_task(task_id)
                target_item = await ai_illustrator.generate_one(
                    target_item, 
                    task_state.image_model, 
                    client, 
                    style_suffix
                )
                
                logger.info(f"重新生成完成: {illustration_id}")
            finally:
                await client.close()
            
            # 保存最终结果
            self._save_result(task_id)
            
        except Exception as e:
            logger.error(f"重新生成失败: {e}")
            # 如果失败，设置为失败状态
            if task_id in self._results:
                illustrated_doc = self._results[task_id]
                for item in illustrated_doc.illustrations:
                    if item.id == illustration_id:
                        item.status = IllustrationStatus.FAILED
                self._save_result(task_id)

    async def remove_illustration(self, task_id: str, illustration_id: str) -> None:
        """删除指定插图"""
        if task_id not in self._results:
            raise TaskNotFoundError(task_id)
        
        illustrated_doc = self._results[task_id]
        illustrated_doc.illustrations = [
            item for item in illustrated_doc.illustrations 
            if item.id != illustration_id
        ]
        
        # 保存结果
        self._save_result(task_id)

    async def move_illustration(
        self, task_id: str, illustration_id: str, after_section_id: str
    ) -> None:
        """调整插图位置"""
        if task_id not in self._results:
            raise TaskNotFoundError(task_id)
        
        illustrated_doc = self._results[task_id]
        
        # 找到对应的插图
        target_item = None
        for item in illustrated_doc.illustrations:
            if item.id == illustration_id:
                target_item = item
                break
        
        if not target_item:
            raise ValueError("插图不存在")
        
        # 更新位置
        target_item.after_section_id = after_section_id
        
        # 保存结果
        self._save_result(task_id)

    async def get_preview(self, task_id: str) -> dict:
        """获取预览数据（文档和计划的插图）"""
        if task_id not in self._temp_illustrations or task_id not in self._temp_document:
            raise TaskNotFoundError(task_id)
        
        document = self._temp_document[task_id]
        illustrations = self._temp_illustrations[task_id]
        
        # 预览阶段不需要处理图片路径（图片还没生成）
        # 直接返回即可
        return {
            "document": document,
            "illustrations": illustrations
        }

    async def confirm_preview(self, task_id: str, image_model: str) -> None:
        """确认预览，开始生成图片"""
        import logging
        logger = logging.getLogger(__name__)
        
        if task_id not in self._temp_illustrations or task_id not in self._temp_document:
            raise TaskNotFoundError(task_id)
        
        document = self._temp_document[task_id]
        illustrations = self._temp_illustrations[task_id]
        
        logger.info(f"[文档服务] 开始生成插图，任务: {task_id}")
        
        # 阶段 3: AI 图片生成
        await task_manager.update_progress(
            task_id,
            TaskPhase.GENERATING,
            0.35,
            "开始生成插图...",
        )
        
        illustrations = await ai_illustrator.generate_all(illustrations, image_model, task_id)
        
        # 阶段 4: 组装
        logger.info(f"[文档服务] 插图生成完成，检查图片路径:")
        for illu in illustrations:
            logger.info(f"  - {illu.id}: status={illu.status}, image_path={illu.image_path}")
        
        illustrated_doc = IllustratedDocument(
            document=document,
            illustrations=illustrations,
        )
        self._results[task_id] = illustrated_doc
        print(f"[文档服务] 结果已保存到 _results[{task_id}]")
        logger.info(f"[文档服务] 结果已保存到 _results[{task_id}]")
        
        # 持久化最终结果到文件
        print(f"[文档服务] 调用 _save_result({task_id})")
        self._save_result(task_id)
        logger.info(f"[文档服务] 结果已持久化到文件")
        
        await task_manager.update_progress(
            task_id,
            TaskPhase.COMPLETE,
            1.0,
            "处理完成",
        )
        
        # 清理临时数据
        if task_id in self._temp_illustrations:
            del self._temp_illustrations[task_id]
        if task_id in self._temp_document:
            del self._temp_document[task_id]
        
        # 删除临时数据文件
        self._delete_temp_data(task_id)


# 全局单例
document_service = DocumentService()
