#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置管理模块
负责应用程序配置管理
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class Settings:
    """设置管理类"""
    
    def __init__(self, config_file: str = "config/settings.json"):
        """初始化设置管理器"""
        self.config_file = config_file
        self.settings = self._load_default_settings()
        self._load_settings()
        
        logger.info(f"设置管理器初始化完成，配置文件: {config_file}")
    
    def _load_default_settings(self) -> Dict[str, Any]:
        """加载默认设置"""
        return {
            # 文本处理设置
            'chunk_size': 4000,
            'overlap_size': 200,
            
            # LLM协调设置
            'max_concurrent_tasks': 3,
            'retry_attempts': 3,
            'retry_delay': 1.0,
            
            # 内容验证设置
            'min_similarity_threshold': 0.95,
            'max_content_loss_threshold': 0.05,
            
            # LLM配置
            'llm_configs': [
                {
                    'name': 'openai_gpt4',
                    'api_key': 'your-openai-api-key',
                    'base_url': 'https://api.openai.com/v1',
                    'model': 'gpt-4',
                    'max_tokens': 4000,
                    'temperature': 0.7,
                    'timeout': 30,
                    'priority': 1
                },
                {
                    'name': 'claude_3',
                    'api_key': 'your-claude-api-key',
                    'base_url': 'https://api.anthropic.com/v1',
                    'model': 'claude-3-sonnet-20240229',
                    'max_tokens': 4000,
                    'temperature': 0.7,
                    'timeout': 30,
                    'priority': 2
                }
            ],
            
            # 输出设置
            'output_format': 'html',  # html, word, plain
            'output_directory': 'output',
            'backup_original': True,
            
            # 日志设置
            'log_level': 'INFO',
            'log_file': 'logs/david.log',
            'log_max_size': 10 * 1024 * 1024,  # 10MB
            'log_backup_count': 5,
            
            # 性能设置
            'max_memory_usage': 1024 * 1024 * 1024,  # 1GB
            'temp_directory': 'temp',
            'cleanup_temp_files': True,
            
            # 安全设置
            'max_file_size': 100 * 1024 * 1024,  # 100MB
            'allowed_file_extensions': ['.txt', '.md', '.docx'],
            'enable_content_validation': True,
            
            # 用户界面设置
            'show_progress_bar': True,
            'auto_save_settings': True,
            'theme': 'default'
        }
    
    def _load_settings(self):
        """加载设置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                
                # 合并用户设置和默认设置
                self._merge_settings(user_settings)
                logger.info(f"成功加载设置文件: {self.config_file}")
            else:
                # 创建默认设置文件
                self._save_settings()
                logger.info(f"创建默认设置文件: {self.config_file}")
                
        except Exception as e:
            logger.error(f"加载设置文件失败: {e}")
            logger.info("使用默认设置")
    
    def _merge_settings(self, user_settings: Dict[str, Any]):
        """合并用户设置和默认设置"""
        def merge_dict(default: Dict, user: Dict) -> Dict:
            result = default.copy()
            for key, value in user.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dict(result[key], value)
                else:
                    result[key] = value
            return result
        
        self.settings = merge_dict(self.settings, user_settings)
    
    def _save_settings(self):
        """保存设置到文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            
            logger.info(f"设置已保存到: {self.config_file}")
            
        except Exception as e:
            logger.error(f"保存设置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取设置值"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置值"""
        self.settings[key] = value
        
        if self.get('auto_save_settings', True):
            self._save_settings()
    
    def get_all_settings(self) -> Dict[str, Any]:
        """获取所有设置"""
        return self.settings.copy()
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """更新设置"""
        self._merge_settings(new_settings)
        self._save_settings()
    
    def reset_to_default(self):
        """重置为默认设置"""
        self.settings = self._load_default_settings()
        self._save_settings()
        logger.info("设置已重置为默认值")
    
    def validate_settings(self) -> List[str]:
        """验证设置有效性"""
        errors = []
        
        # 验证数值设置
        if not isinstance(self.get('chunk_size'), int) or self.get('chunk_size') <= 0:
            errors.append("chunk_size 必须是正整数")
        
        if not isinstance(self.get('overlap_size'), int) or self.get('overlap_size') < 0:
            errors.append("overlap_size 必须是非负整数")
        
        if not isinstance(self.get('max_concurrent_tasks'), int) or self.get('max_concurrent_tasks') <= 0:
            errors.append("max_concurrent_tasks 必须是正整数")
        
        # 验证阈值设置
        similarity_threshold = self.get('min_similarity_threshold')
        if not isinstance(similarity_threshold, (int, float)) or not 0 <= similarity_threshold <= 1:
            errors.append("min_similarity_threshold 必须是0到1之间的数值")
        
        content_loss_threshold = self.get('max_content_loss_threshold')
        if not isinstance(content_loss_threshold, (int, float)) or not 0 <= content_loss_threshold <= 1:
            errors.append("max_content_loss_threshold 必须是0到1之间的数值")
        
        # 验证LLM配置
        llm_configs = self.get('llm_configs', [])
        if not isinstance(llm_configs, list):
            errors.append("llm_configs 必须是列表")
        else:
            for i, config in enumerate(llm_configs):
                if not isinstance(config, dict):
                    errors.append(f"LLM配置 {i} 必须是字典")
                    continue
                
                required_fields = ['name', 'api_key', 'base_url', 'model']
                for field in required_fields:
                    if field not in config:
                        errors.append(f"LLM配置 {i} 缺少必需字段: {field}")
        
        # 验证文件路径
        output_dir = self.get('output_directory')
        if not isinstance(output_dir, str) or not output_dir:
            errors.append("output_directory 必须是有效的字符串")
        
        log_file = self.get('log_file')
        if not isinstance(log_file, str) or not log_file:
            errors.append("log_file 必须是有效的字符串")
        
        return errors
    
    def get_llm_config(self, name: str) -> Optional[Dict[str, Any]]:
        """获取指定名称的LLM配置"""
        llm_configs = self.get('llm_configs', [])
        for config in llm_configs:
            if config.get('name') == name:
                return config
        return None
    
    def add_llm_config(self, config: Dict[str, Any]):
        """添加LLM配置"""
        llm_configs = self.get('llm_configs', [])
        llm_configs.append(config)
        self.set('llm_configs', llm_configs)
    
    def remove_llm_config(self, name: str):
        """移除LLM配置"""
        llm_configs = self.get('llm_configs', [])
        llm_configs = [config for config in llm_configs if config.get('name') != name]
        self.set('llm_configs', llm_configs)
    
    def update_llm_config(self, name: str, new_config: Dict[str, Any]):
        """更新LLM配置"""
        llm_configs = self.get('llm_configs', [])
        for i, config in enumerate(llm_configs):
            if config.get('name') == name:
                llm_configs[i] = new_config
                break
        self.set('llm_configs', llm_configs)
    
    def export_settings(self, file_path: str):
        """导出设置到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            logger.info(f"设置已导出到: {file_path}")
        except Exception as e:
            logger.error(f"导出设置失败: {e}")
            raise
    
    def import_settings(self, file_path: str):
        """从文件导入设置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            self._merge_settings(imported_settings)
            self._save_settings()
            logger.info(f"设置已从文件导入: {file_path}")
        except Exception as e:
            logger.error(f"导入设置失败: {e}")
            raise
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        import platform
        import psutil
        
        return {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
        }

