#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫 - 智能长文本排版应用程序
David - Intelligent Long Text Formatting Application

一个专门用于处理长文本文件排版的智能应用程序，
能够协调多个大语言模型完成排版任务，确保内容完整性和格式规范。
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# 导入自定义模块
from core.text_processor import TextProcessor
from core.llm_coordinator import LLMCoordinator
from core.formatting_engine import FormattingEngine
from core.content_validator import ContentValidator
from ui.main_interface import MainInterface
from config.settings import Settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/david.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """处理结果数据类"""
    success: bool
    output_file: str
    original_word_count: int
    processed_word_count: int
    processing_time: float
    errors: List[str]
    warnings: List[str]

class DavidApp:
    """大卫应用程序主类"""
    
    def __init__(self, config_file: str = "config/settings.json"):
        """初始化应用程序"""
        self.settings = Settings(config_file)
        self.text_processor = TextProcessor(self.settings)
        self.llm_coordinator = LLMCoordinator(self.settings)
        self.formatting_engine = FormattingEngine(self.settings)
        self.content_validator = ContentValidator(self.settings)
        self.ui = MainInterface()
        
        # 确保日志目录存在
        os.makedirs("logs", exist_ok=True)
        
        logger.info("大卫应用程序初始化完成")
    
    def process_text_file(self, input_file: str, output_file: Optional[str] = None) -> ProcessingResult:
        """
        处理文本文件的主要方法
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径（可选）
            
        Returns:
            ProcessingResult: 处理结果
        """
        start_time = datetime.now()
        errors = []
        warnings = []
        
        try:
            logger.info(f"开始处理文件: {input_file}")
            
            # 1. 读取和预处理文本
            logger.info("步骤1: 读取和预处理文本")
            text_chunks = self.text_processor.load_and_chunk_text(input_file)
            original_word_count = sum(len(chunk.split()) for chunk in text_chunks)
            
            # 2. 使用多个LLM协调处理
            logger.info("步骤2: 使用多个LLM协调处理")
            processed_chunks = self.llm_coordinator.process_chunks(text_chunks)
            
            # 3. 应用排版规则
            logger.info("步骤3: 应用排版规则")
            formatted_text = self.formatting_engine.format_text(processed_chunks)
            
            # 4. 验证内容完整性
            logger.info("步骤4: 验证内容完整性")
            validation_result = self.content_validator.validate_content(
                original_chunks=text_chunks,
                processed_chunks=processed_chunks,
                formatted_text=formatted_text
            )
            
            if not validation_result.is_valid:
                errors.extend(validation_result.errors)
                warnings.extend(validation_result.warnings)
            
            # 5. 保存结果
            if not output_file:
                output_file = self._generate_output_filename(input_file)
            
            logger.info("步骤5: 保存结果")
            self._save_formatted_text(formatted_text, output_file)
            
            # 计算处理时间
            processing_time = (datetime.now() - start_time).total_seconds()
            processed_word_count = len(formatted_text.split())
            
            logger.info(f"文件处理完成: {output_file}")
            logger.info(f"处理时间: {processing_time:.2f}秒")
            logger.info(f"字数统计: {original_word_count} -> {processed_word_count}")
            
            return ProcessingResult(
                success=len(errors) == 0,
                output_file=output_file,
                original_word_count=original_word_count,
                processed_word_count=processed_word_count,
                processing_time=processing_time,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            error_msg = f"处理文件时发生错误: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            
            return ProcessingResult(
                success=False,
                output_file="",
                original_word_count=0,
                processed_word_count=0,
                processing_time=(datetime.now() - start_time).total_seconds(),
                errors=errors,
                warnings=warnings
            )
    
    def _generate_output_filename(self, input_file: str) -> str:
        """生成输出文件名"""
        input_path = Path(input_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{input_path.stem}_formatted_{timestamp}.txt"
    
    def _save_formatted_text(self, text: str, output_file: str):
        """保存格式化后的文本"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def run_interactive_mode(self):
        """运行交互模式"""
        self.ui.run(self)
    
    def run_batch_mode(self, input_files: List[str], output_dir: str = "output"):
        """运行批处理模式"""
        logger.info(f"开始批处理模式，处理 {len(input_files)} 个文件")
        
        results = []
        for i, input_file in enumerate(input_files, 1):
            logger.info(f"处理文件 {i}/{len(input_files)}: {input_file}")
            
            output_file = os.path.join(output_dir, f"formatted_{os.path.basename(input_file)}")
            result = self.process_text_file(input_file, output_file)
            results.append(result)
            
            if result.success:
                logger.info(f"✓ 文件处理成功: {result.output_file}")
            else:
                logger.error(f"✗ 文件处理失败: {result.errors}")
        
        # 生成批处理报告
        self._generate_batch_report(results, output_dir)
    
    def _generate_batch_report(self, results: List[ProcessingResult], output_dir: str):
        """生成批处理报告"""
        report_file = os.path.join(output_dir, "batch_report.json")
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(results),
            "successful_files": sum(1 for r in results if r.success),
            "failed_files": sum(1 for r in results if not r.success),
            "total_processing_time": sum(r.processing_time for r in results),
            "results": [
                {
                    "input_file": getattr(r, 'input_file', ''),
                    "output_file": r.output_file,
                    "success": r.success,
                    "word_count": r.processed_word_count,
                    "processing_time": r.processing_time,
                    "errors": r.errors,
                    "warnings": r.warnings
                }
                for r in results
            ]
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"批处理报告已保存: {report_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("大卫 - 智能长文本排版应用程序")
    print("David - Intelligent Long Text Formatting Application")
    print("=" * 60)
    
    try:
        # 创建应用程序实例
        app = DavidApp()
        
        # 检查命令行参数
        if len(sys.argv) > 1:
            # 批处理模式
            input_files = sys.argv[1:]
            app.run_batch_mode(input_files)
        else:
            # 交互模式
            app.run_interactive_mode()
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        logger.info("程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        logger.error(f"程序运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

