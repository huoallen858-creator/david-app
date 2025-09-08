#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
排版引擎模块
负责应用排版规则和格式化文本
"""

import re
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class FormattingRule:
    """排版规则类"""
    name: str
    pattern: str
    replacement: str
    flags: int = 0
    priority: int = 0

class FormattingEngine:
    """排版引擎类"""
    
    def __init__(self, settings):
        """初始化排版引擎"""
        self.settings = settings
        self.rules = self._load_formatting_rules()
        
        logger.info(f"排版引擎初始化完成，加载了 {len(self.rules)} 个规则")
    
    def _load_formatting_rules(self) -> List[FormattingRule]:
        """加载排版规则"""
        rules = []
        
        # 标题格式化规则
        rules.append(FormattingRule(
            name="chapter_title",
            pattern=r'^\*\*(CH\d+\s+.+?)\*\*$',
            replacement=r'<h1>\1</h1>',
            flags=re.MULTILINE,
            priority=1
        ))
        
        rules.append(FormattingRule(
            name="section_title",
            pattern=r'^\*\*(CH\d+-S\d+\s+.+?)\*\*$',
            replacement=r'<h2>\1</h2>',
            flags=re.MULTILINE,
            priority=2
        ))
        
        # 引用格式化规则
        rules.append(FormattingRule(
            name="quote_format",
            pattern=r'【([^】]+)】',
            replacement=r'<blockquote>\1</blockquote>',
            priority=3
        ))
        
        # 列表格式化规则
        rules.append(FormattingRule(
            name="bullet_list",
            pattern=r'^[\s]*- (.+)$',
            replacement=r'<li>\1</li>',
            flags=re.MULTILINE,
            priority=4
        ))
        
        rules.append(FormattingRule(
            name="numbered_list",
            pattern=r'^[\s]*(\d+)\. (.+)$',
            replacement=r'<li>\1. \2</li>',
            flags=re.MULTILINE,
            priority=5
        ))
        
        # 段落格式化规则
        rules.append(FormattingRule(
            name="paragraph_indent",
            pattern=r'^[\s]{4}(.+)$',
            replacement=r'<p>\1</p>',
            flags=re.MULTILINE,
            priority=6
        ))
        
        # 分页规则
        rules.append(FormattingRule(
            name="chapter_page_break",
            pattern=r'<h1>CH\d+',
            replacement=r'<div class="page-break"></div><h1>CH',
            priority=7
        ))
        
        # 按优先级排序
        rules.sort(key=lambda x: x.priority)
        
        return rules
    
    def format_text(self, chunks: List[str]) -> str:
        """
        格式化文本
        
        Args:
            chunks: 处理后的文本块列表
            
        Returns:
            str: 格式化后的文本
        """
        logger.info(f"开始格式化 {len(chunks)} 个文本块")
        
        # 合并文本块
        combined_text = self._combine_chunks(chunks)
        
        # 应用格式化规则
        formatted_text = self._apply_formatting_rules(combined_text)
        
        # 后处理
        final_text = self._post_process(formatted_text)
        
        logger.info("文本格式化完成")
        
        return final_text
    
    def _combine_chunks(self, chunks: List[str]) -> str:
        """合并文本块"""
        combined = []
        
        for i, chunk in enumerate(chunks):
            # 清理块内容
            cleaned_chunk = self._clean_chunk(chunk)
            
            if cleaned_chunk:
                combined.append(cleaned_chunk)
                
                # 在块之间添加适当的分隔
                if i < len(chunks) - 1:
                    combined.append('\n\n')
        
        return ''.join(combined)
    
    def _clean_chunk(self, chunk: str) -> str:
        """清理文本块"""
        # 移除多余的空行
        chunk = re.sub(r'\n\s*\n\s*\n', '\n\n', chunk)
        
        # 移除行首行尾空白
        lines = chunk.split('\n')
        cleaned_lines = [line.strip() for line in lines]
        
        # 移除空行
        non_empty_lines = [line for line in cleaned_lines if line]
        
        return '\n'.join(non_empty_lines)
    
    def _apply_formatting_rules(self, text: str) -> str:
        """应用格式化规则"""
        formatted_text = text
        
        for rule in self.rules:
            try:
                formatted_text = re.sub(
                    rule.pattern, 
                    rule.replacement, 
                    formatted_text, 
                    flags=rule.flags
                )
                logger.debug(f"应用规则 {rule.name}")
            except Exception as e:
                logger.warning(f"应用规则 {rule.name} 失败: {e}")
        
        return formatted_text
    
    def _post_process(self, text: str) -> str:
        """后处理"""
        # 添加文档头部
        header = self._generate_header()
        
        # 添加文档尾部
        footer = self._generate_footer()
        
        # 组合最终文档
        final_text = header + '\n\n' + text + '\n\n' + footer
        
        # 清理多余的空行
        final_text = re.sub(r'\n\s*\n\s*\n', '\n\n', final_text)
        
        return final_text
    
    def _generate_header(self) -> str:
        """生成文档头部"""
        header = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>格式化文档</title>
    <style>
        body {
            font-family: "Microsoft YaHei", "SimSun", sans-serif;
            line-height: 1.5;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
        }
        
        h1 {
            font-size: 30px;
            font-weight: bold;
            color: #333;
            margin: 20px 0;
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }
        
        h2 {
            font-size: 26px;
            font-weight: bold;
            color: #555;
            margin: 15px 0;
            text-align: left;
        }
        
        p {
            font-size: 20px;
            text-indent: 2em;
            margin: 10px 0;
            line-height: 1.5;
        }
        
        blockquote {
            background-color: #f5f5f5;
            border-left: 4px solid #333;
            margin: 15px 0;
            padding: 10px 20px;
            font-style: italic;
        }
        
        li {
            font-size: 20px;
            margin: 5px 0;
            line-height: 1.5;
        }
        
        ul, ol {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        @media print {
            .page-break {
                page-break-before: always;
            }
        }
    </style>
</head>
<body>"""
        return header
    
    def _generate_footer(self) -> str:
        """生成文档尾部"""
        footer = """</body>
</html>"""
        return footer
    
    def format_for_word(self, text: str) -> str:
        """
        格式化为Word文档格式
        
        Args:
            text: 原始文本
            
        Returns:
            str: Word格式文本
        """
        logger.info("开始格式化为Word格式")
        
        # 应用Word特定的格式化规则
        word_rules = self._get_word_formatting_rules()
        
        formatted_text = text
        for rule in word_rules:
            try:
                formatted_text = re.sub(
                    rule.pattern,
                    rule.replacement,
                    formatted_text,
                    flags=rule.flags
                )
            except Exception as e:
                logger.warning(f"应用Word规则 {rule.name} 失败: {e}")
        
        return formatted_text
    
    def _get_word_formatting_rules(self) -> List[FormattingRule]:
        """获取Word格式化规则"""
        rules = []
        
        # 章节标题 - Word格式
        rules.append(FormattingRule(
            name="word_chapter_title",
            pattern=r'^\*\*(CH\d+\s+.+?)\*\*$',
            replacement=r'CH\1',
            flags=re.MULTILINE,
            priority=1
        ))
        
        # 小节标题 - Word格式
        rules.append(FormattingRule(
            name="word_section_title",
            pattern=r'^\*\*(CH\d+-S\d+\s+.+?)\*\*$',
            replacement=r'CH\1',
            flags=re.MULTILINE,
            priority=2
        ))
        
        # 引用 - Word格式
        rules.append(FormattingRule(
            name="word_quote",
            pattern=r'【([^】]+)】',
            replacement=r'【\1】',
            priority=3
        ))
        
        # 列表 - Word格式
        rules.append(FormattingRule(
            name="word_bullet_list",
            pattern=r'^[\s]*- (.+)$',
            replacement=r'- \1',
            flags=re.MULTILINE,
            priority=4
        ))
        
        rules.append(FormattingRule(
            name="word_numbered_list",
            pattern=r'^[\s]*(\d+)\. (.+)$',
            replacement=r'\1. \2',
            flags=re.MULTILINE,
            priority=5
        ))
        
        # 段落缩进 - Word格式
        rules.append(FormattingRule(
            name="word_paragraph",
            pattern=r'^[\s]{4}(.+)$',
            replacement=r'    \1',
            flags=re.MULTILINE,
            priority=6
        ))
        
        # 分页 - Word格式
        rules.append(FormattingRule(
            name="word_page_break",
            pattern=r'<div class="page-break"></div>',
            replacement=r'\f',
            priority=7
        ))
        
        return rules
    
    def get_formatting_stats(self) -> Dict[str, Any]:
        """获取格式化统计信息"""
        return {
            'total_rules': len(self.rules),
            'rule_names': [rule.name for rule in self.rules],
            'supported_formats': ['HTML', 'Word', 'Plain Text']
        }
    
    def validate_formatting(self, text: str) -> Dict[str, Any]:
        """验证格式化结果"""
        validation = {
            'has_chapter_headers': bool(re.search(r'CH\d+\s+', text)),
            'has_section_headers': bool(re.search(r'CH\d+-S\d+\s+', text)),
            'has_quotes': bool(re.search(r'【[^】]+】', text)),
            'has_lists': bool(re.search(r'^[\s]*[-•]\s+', text, re.MULTILINE) or 
                            re.search(r'^[\s]*\d+\.\s+', text, re.MULTILINE)),
            'has_paragraphs': bool(re.search(r'^[\s]{4}', text, re.MULTILINE)),
            'total_length': len(text),
            'line_count': len(text.split('\n'))
        }
        
        return validation

