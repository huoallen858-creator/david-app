#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本处理模块
负责文本的读取、分块和预处理
"""

import re
import os
import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class TextProcessor:
    """文本处理器类"""
    
    def __init__(self, settings):
        """初始化文本处理器"""
        self.settings = settings
        self.chunk_size = settings.get('chunk_size', 4000)  # 每个块的最大字符数
        self.overlap_size = settings.get('overlap_size', 200)  # 块之间的重叠字符数
        
        # 标题模式
        self.chapter_pattern = re.compile(r'^CH\d+\s+(.+)$', re.MULTILINE)
        self.section_pattern = re.compile(r'^CH\d+-S\d+\s+(.+)$', re.MULTILINE)
        
        # 特殊标记模式
        self.quote_pattern = re.compile(r'【([^】]+)】')
        self.list_pattern = re.compile(r'^[\s]*[-•]\s+(.+)$', re.MULTILINE)
        self.numbered_list_pattern = re.compile(r'^[\s]*\d+\.\s+(.+)$', re.MULTILINE)
    
    def load_and_chunk_text(self, file_path: str) -> List[str]:
        """
        加载文本文件并分块
        
        Args:
            file_path: 文件路径
            
        Returns:
            List[str]: 文本块列表
        """
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"成功读取文件: {file_path}, 字符数: {len(content)}")
            
            # 预处理文本
            processed_content = self._preprocess_text(content)
            
            # 分块处理
            chunks = self._chunk_text(processed_content)
            
            logger.info(f"文本分块完成，共 {len(chunks)} 个块")
            
            return chunks
            
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            raise
    
    def _preprocess_text(self, content: str) -> str:
        """
        预处理文本
        
        Args:
            content: 原始文本内容
            
        Returns:
            str: 预处理后的文本
        """
        # 统一换行符
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 确保章节标题格式正确
        content = self._normalize_chapter_headers(content)
        
        # 确保小节标题格式正确
        content = self._normalize_section_headers(content)
        
        # 清理特殊字符
        content = self._clean_special_characters(content)
        
        return content
    
    def _normalize_chapter_headers(self, content: str) -> str:
        """标准化章节标题格式"""
        def replace_chapter(match):
            chapter_num = match.group(1)
            title = match.group(2).strip()
            return f"CH{chapter_num} {title}"
        
        # 匹配各种可能的章节标题格式
        patterns = [
            r'第\s*(\d+)\s*章\s*(.+)',
            r'Chapter\s*(\d+)\s*(.+)',
            r'CHAPTER\s*(\d+)\s*(.+)',
            r'第\s*(\d+)\s*节\s*(.+)',
            r'(\d+)\s*[、．]\s*(.+)',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, replace_chapter, content, flags=re.MULTILINE)
        
        return content
    
    def _normalize_section_headers(self, content: str) -> str:
        """标准化小节标题格式"""
        def replace_section(match):
            chapter_num = match.group(1)
            section_num = match.group(2)
            title = match.group(3).strip()
            return f"CH{chapter_num}-S{section_num} {title}"
        
        # 匹配各种可能的小节标题格式
        patterns = [
            r'第\s*(\d+)\s*章\s*第\s*(\d+)\s*节\s*(.+)',
            r'(\d+)\.(\d+)\s+(.+)',
            r'(\d+)-(\d+)\s+(.+)',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, replace_section, content, flags=re.MULTILINE)
        
        return content
    
    def _clean_special_characters(self, content: str) -> str:
        """清理特殊字符"""
        # 替换全角字符为半角
        content = content.replace('（', '(').replace('）', ')')
        content = content.replace('，', ',').replace('。', '.')
        content = content.replace('；', ';').replace('：', ':')
        content = content.replace('"', '"').replace('"', '"')
        content = content.replace(''', "'").replace(''', "'")
        
        # 清理多余的空格
        content = re.sub(r' +', ' ', content)
        
        return content
    
    def _chunk_text(self, content: str) -> List[str]:
        """
        将文本分块
        
        Args:
            content: 文本内容
            
        Returns:
            List[str]: 文本块列表
        """
        chunks = []
        
        # 首先按章节分割
        chapter_splits = self._split_by_chapters(content)
        
        for chapter in chapter_splits:
            if len(chapter) <= self.chunk_size:
                chunks.append(chapter)
            else:
                # 章节太长，需要进一步分割
                sub_chunks = self._split_by_sections(chapter)
                for sub_chunk in sub_chunks:
                    if len(sub_chunk) <= self.chunk_size:
                        chunks.append(sub_chunk)
                    else:
                        # 按段落分割
                        paragraph_chunks = self._split_by_paragraphs(sub_chunk)
                        chunks.extend(paragraph_chunks)
        
        # 添加重叠内容以确保连续性
        chunks = self._add_overlap(chunks)
        
        return chunks
    
    def _split_by_chapters(self, content: str) -> List[str]:
        """按章节分割文本"""
        chapters = []
        current_chapter = ""
        
        lines = content.split('\n')
        for line in lines:
            if self.chapter_pattern.match(line.strip()):
                if current_chapter:
                    chapters.append(current_chapter.strip())
                current_chapter = line + '\n'
            else:
                current_chapter += line + '\n'
        
        if current_chapter:
            chapters.append(current_chapter.strip())
        
        return chapters
    
    def _split_by_sections(self, content: str) -> List[str]:
        """按小节分割文本"""
        sections = []
        current_section = ""
        
        lines = content.split('\n')
        for line in lines:
            if self.section_pattern.match(line.strip()):
                if current_section:
                    sections.append(current_section.strip())
                current_section = line + '\n'
            else:
                current_section += line + '\n'
        
        if current_section:
            sections.append(current_section.strip())
        
        return sections
    
    def _split_by_paragraphs(self, content: str) -> List[str]:
        """按段落分割文本"""
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= self.chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _add_overlap(self, chunks: List[str]) -> List[str]:
        """为文本块添加重叠内容"""
        if len(chunks) <= 1:
            return chunks
        
        overlapped_chunks = [chunks[0]]
        
        for i in range(1, len(chunks)):
            current_chunk = chunks[i]
            previous_chunk = chunks[i-1]
            
            # 从前一个块的末尾提取重叠内容
            overlap_text = previous_chunk[-self.overlap_size:] if len(previous_chunk) > self.overlap_size else ""
            
            # 将重叠内容添加到当前块的开头
            if overlap_text:
                overlapped_chunk = overlap_text + current_chunk
            else:
                overlapped_chunk = current_chunk
            
            overlapped_chunks.append(overlapped_chunk)
        
        return overlapped_chunks
    
    def analyze_text_structure(self, content: str) -> Dict[str, Any]:
        """
        分析文本结构
        
        Args:
            content: 文本内容
            
        Returns:
            Dict[str, Any]: 结构分析结果
        """
        analysis = {
            'total_characters': len(content),
            'total_words': len(content.split()),
            'total_lines': len(content.split('\n')),
            'chapters': [],
            'sections': [],
            'paragraphs': 0,
            'quotes': 0,
            'lists': 0
        }
        
        # 分析章节
        chapter_matches = self.chapter_pattern.findall(content)
        for i, title in enumerate(chapter_matches, 1):
            analysis['chapters'].append({
                'number': i,
                'title': title.strip()
            })
        
        # 分析小节
        section_matches = self.section_pattern.findall(content)
        for title in section_matches:
            analysis['sections'].append({
                'title': title.strip()
            })
        
        # 分析段落
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        analysis['paragraphs'] = len(paragraphs)
        
        # 分析引用
        quote_matches = self.quote_pattern.findall(content)
        analysis['quotes'] = len(quote_matches)
        
        # 分析列表
        list_matches = self.list_pattern.findall(content)
        numbered_list_matches = self.numbered_list_pattern.findall(content)
        analysis['lists'] = len(list_matches) + len(numbered_list_matches)
        
        return analysis

