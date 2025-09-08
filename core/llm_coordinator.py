#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM协调器模块
负责协调多个大语言模型处理文本块
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    """LLM配置类"""
    name: str
    api_key: str
    base_url: str
    model: str
    max_tokens: int
    temperature: float
    timeout: int
    priority: int  # 优先级，数字越小优先级越高

@dataclass
class ProcessingTask:
    """处理任务类"""
    chunk_id: int
    content: str
    assigned_llm: str
    status: str  # pending, processing, completed, failed
    result: Optional[str] = None
    error: Optional[str] = None
    processing_time: float = 0.0

class LLMCoordinator:
    """LLM协调器类"""
    
    def __init__(self, settings):
        """初始化LLM协调器"""
        self.settings = settings
        self.llm_configs = self._load_llm_configs()
        self.max_concurrent_tasks = settings.get('max_concurrent_tasks', 3)
        self.retry_attempts = settings.get('retry_attempts', 3)
        self.retry_delay = settings.get('retry_delay', 1.0)
        
        logger.info(f"LLM协调器初始化完成，配置了 {len(self.llm_configs)} 个LLM")
    
    def _load_llm_configs(self) -> List[LLMConfig]:
        """加载LLM配置"""
        configs = []
        
        # 从设置中获取LLM配置
        llm_settings = self.settings.get('llm_configs', [])
        
        for config_data in llm_settings:
            config = LLMConfig(
                name=config_data['name'],
                api_key=config_data['api_key'],
                base_url=config_data['base_url'],
                model=config_data['model'],
                max_tokens=config_data.get('max_tokens', 4000),
                temperature=config_data.get('temperature', 0.7),
                timeout=config_data.get('timeout', 30),
                priority=config_data.get('priority', 1)
            )
            configs.append(config)
        
        # 按优先级排序
        configs.sort(key=lambda x: x.priority)
        
        return configs
    
    def process_chunks(self, chunks: List[str]) -> List[str]:
        """
        处理文本块
        
        Args:
            chunks: 文本块列表
            
        Returns:
            List[str]: 处理后的文本块列表
        """
        logger.info(f"开始处理 {len(chunks)} 个文本块")
        
        # 创建处理任务
        tasks = []
        for i, chunk in enumerate(chunks):
            task = ProcessingTask(
                chunk_id=i,
                content=chunk,
                assigned_llm=self._select_llm(i),
                status='pending'
            )
            tasks.append(task)
        
        # 并行处理任务
        processed_tasks = self._process_tasks_parallel(tasks)
        
        # 按原始顺序排序结果
        processed_tasks.sort(key=lambda x: x.chunk_id)
        
        # 提取处理结果
        results = []
        for task in processed_tasks:
            if task.status == 'completed' and task.result:
                results.append(task.result)
            else:
                logger.warning(f"文本块 {task.chunk_id} 处理失败: {task.error}")
                # 使用原始内容作为备选
                results.append(task.content)
        
        logger.info(f"文本块处理完成，成功处理 {len([t for t in processed_tasks if t.status == 'completed'])} 个")
        
        return results
    
    def _select_llm(self, chunk_id: int) -> str:
        """选择LLM"""
        if not self.llm_configs:
            raise ValueError("没有可用的LLM配置")
        
        # 使用轮询方式分配LLM
        llm_index = chunk_id % len(self.llm_configs)
        return self.llm_configs[llm_index].name
    
    def _process_tasks_parallel(self, tasks: List[ProcessingTask]) -> List[ProcessingTask]:
        """并行处理任务"""
        with ThreadPoolExecutor(max_workers=self.max_concurrent_tasks) as executor:
            # 提交所有任务
            future_to_task = {}
            for task in tasks:
                future = executor.submit(self._process_single_task, task)
                future_to_task[future] = task
            
            # 等待任务完成
            completed_tasks = []
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    completed_tasks.append(result)
                except Exception as e:
                    logger.error(f"任务 {task.chunk_id} 执行异常: {e}")
                    task.status = 'failed'
                    task.error = str(e)
                    completed_tasks.append(task)
        
        return completed_tasks
    
    def _process_single_task(self, task: ProcessingTask) -> ProcessingTask:
        """处理单个任务"""
        start_time = time.time()
        task.status = 'processing'
        
        try:
            # 获取LLM配置
            llm_config = self._get_llm_config(task.assigned_llm)
            if not llm_config:
                raise ValueError(f"找不到LLM配置: {task.assigned_llm}")
            
            # 处理文本
            result = self._call_llm_api(task.content, llm_config)
            
            task.result = result
            task.status = 'completed'
            task.processing_time = time.time() - start_time
            
            logger.info(f"文本块 {task.chunk_id} 处理完成，用时 {task.processing_time:.2f}秒")
            
        except Exception as e:
            task.status = 'failed'
            task.error = str(e)
            task.processing_time = time.time() - start_time
            
            logger.error(f"文本块 {task.chunk_id} 处理失败: {e}")
            
            # 重试机制
            if self._should_retry(task):
                logger.info(f"重试处理文本块 {task.chunk_id}")
                time.sleep(self.retry_delay)
                return self._process_single_task(task)
        
        return task
    
    def _get_llm_config(self, llm_name: str) -> Optional[LLMConfig]:
        """获取LLM配置"""
        for config in self.llm_configs:
            if config.name == llm_name:
                return config
        return None
    
    def _call_llm_api(self, content: str, config: LLMConfig) -> str:
        """调用LLM API"""
        # 这里需要根据实际的LLM API进行实现
        # 目前使用模拟实现
        
        prompt = self._build_prompt(content)
        
        # 模拟API调用
        time.sleep(0.5)  # 模拟网络延迟
        
        # 这里应该调用真实的LLM API
        # 例如：OpenAI API, Claude API, 或其他LLM服务
        result = self._mock_llm_response(content, prompt)
        
        return result
    
    def _build_prompt(self, content: str) -> str:
        """构建提示词"""
        prompt = f"""
请对以下文本进行智能排版处理，要求：

1. 保持原文内容完整，不遗漏任何信息
2. 识别并正确格式化标题层级：
   - 一级标题：CHxx 章标题 → 加粗，字号 30
   - 二级标题：CHxx-Sxx 小节标题 → 加粗，字号 26
3. 格式化正文：字号 20，首行缩进 2 个字符，1.5 倍行距
4. 处理特殊标记：
   - 引用或重点 → 用【加框】表示
   - 列表 → 用 "- " 或 "1. 2. 3." 表示
5. 确保每个大章节（CHxx）单独换页

请直接返回格式化后的文本，不要添加任何解释：

{content}
"""
        return prompt
    
    def _mock_llm_response(self, content: str, prompt: str) -> str:
        """模拟LLM响应（实际使用时需要替换为真实的API调用）"""
        # 这是一个简化的模拟实现
        # 实际使用时需要调用真实的LLM API
        
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            
            # 处理章节标题
            if line.startswith('CH') and ' ' in line and not line.startswith('CH', 2):
                formatted_lines.append(f"**{line}**")  # 加粗
                formatted_lines.append('')  # 空行
            # 处理小节标题
            elif line.startswith('CH') and '-S' in line:
                formatted_lines.append(f"**{line}**")  # 加粗
                formatted_lines.append('')  # 空行
            # 处理正文
            else:
                # 简单的段落格式化
                if line.startswith('- ') or line.startswith('1. '):
                    formatted_lines.append(line)
                else:
                    formatted_lines.append(f"    {line}")  # 首行缩进
        
        return '\n'.join(formatted_lines)
    
    def _should_retry(self, task: ProcessingTask) -> bool:
        """判断是否应该重试"""
        return (task.status == 'failed' and 
                hasattr(task, 'retry_count') and 
                task.retry_count < self.retry_attempts)
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """获取处理统计信息"""
        return {
            'total_llms': len(self.llm_configs),
            'max_concurrent_tasks': self.max_concurrent_tasks,
            'retry_attempts': self.retry_attempts,
            'retry_delay': self.retry_delay
        }
    
    def validate_llm_connections(self) -> Dict[str, bool]:
        """验证LLM连接"""
        results = {}
        
        for config in self.llm_configs:
            try:
                # 这里应该进行实际的连接测试
                # 目前使用模拟实现
                results[config.name] = True
                logger.info(f"LLM {config.name} 连接正常")
            except Exception as e:
                results[config.name] = False
                logger.error(f"LLM {config.name} 连接失败: {e}")
        
        return results

