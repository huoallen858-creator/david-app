#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版大卫排版应用程序
Simple David Text Formatting Application
"""

import os
import sys
import re
import json
from pathlib import Path

def create_directories():
    """创建必要目录"""
    directories = ['logs', 'output', 'temp', 'config', 'examples']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def create_config():
    """创建配置文件"""
    config = {
        "chunk_size": 4000,
        "overlap_size": 200,
        "max_concurrent_tasks": 3,
        "min_similarity_threshold": 0.95,
        "output_format": "html"
    }
    
    with open('config/settings.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print("✓ 创建配置文件")

def create_sample_text():
    """创建示例文本"""
    sample_text = """CH1 人工智能的发展历程

人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

CH1-S1 早期发展（1940-1950年代）

在1940年代，随着电子计算机的发明，科学家们开始思考机器是否能够模拟人类思维。

【重要观点】图灵在1950年发表的论文《计算机器与智能》中提出了著名的"图灵测试"。

CH1-S2 黄金时代（1950-1970年代）

1956年，达特茅斯会议标志着人工智能作为一门学科的正式诞生。

1. 逻辑理论机（1956年）
2. 通用问题求解器（1957年）
3. 感知机（1958年）

CH2 现代人工智能的崛起

CH2-S1 机器学习的发展

1980年代后期，机器学习开始兴起。这种方法让计算机能够从数据中学习。

- 监督学习：使用标记数据训练模型
- 无监督学习：从无标记数据中发现模式
- 强化学习：通过与环境交互学习最优策略

【技术突破】2012年，AlexNet在ImageNet图像识别竞赛中取得了突破性成果。

CH3 人工智能的应用领域

CH3-S1 自然语言处理

自然语言处理（NLP）是人工智能的重要应用领域。

【应用实例】现代聊天机器人、翻译软件、语音助手等都依赖于自然语言处理技术。

CH3-S2 计算机视觉

计算机视觉让机器能够"看见"和理解图像和视频内容。

- 医疗影像诊断
- 自动驾驶汽车
- 安防监控系统
- 工业质量检测

结论

人工智能作为21世纪最重要的技术之一，正在深刻改变我们的世界。

【最终思考】人工智能不是要替代人类，而是要增强人类的能力。"""
    
    with open('examples/sample_text.txt', 'w', encoding='utf-8') as f:
        f.write(sample_text)
    print("✓ 创建示例文本")

class SimpleTextProcessor:
    """简化的文本处理器"""
    
    def __init__(self):
        self.chapter_pattern = re.compile(r'^CH\d+\s+(.+)$', re.MULTILINE)
        self.section_pattern = re.compile(r'^CH\d+-S\d+\s+(.+)$', re.MULTILINE)
        self.quote_pattern = re.compile(r'【([^】]+)】')
        self.list_pattern = re.compile(r'^[\s]*[-•]\s+(.+)$', re.MULTILINE)
        self.numbered_list_pattern = re.compile(r'^[\s]*(\d+)\.\s+(.+)$', re.MULTILINE)
    
    def process_text(self, text):
        """处理文本"""
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                processed_lines.append('')
                continue
            
            # 处理章节标题
            if self.chapter_pattern.match(line):
                processed_lines.append(f"<h1>{line}</h1>")
                processed_lines.append('')
            # 处理小节标题
            elif self.section_pattern.match(line):
                processed_lines.append(f"<h2>{line}</h2>")
                processed_lines.append('')
            # 处理引用
            elif '【' in line and '】' in line:
                quote_text = self.quote_pattern.search(line)
                if quote_text:
                    processed_lines.append(f'<blockquote>{quote_text.group(1)}</blockquote>')
                else:
                    processed_lines.append(f'<p>{line}</p>')
            # 处理列表
            elif line.startswith('- ') or line.startswith('• '):
                processed_lines.append(f'<li>{line[2:]}</li>')
            elif re.match(r'^\d+\.\s+', line):
                processed_lines.append(f'<li>{line}</li>')
            # 处理普通段落
            else:
                processed_lines.append(f'<p>{line}</p>')
        
        return '\n'.join(processed_lines)
    
    def format_for_html(self, processed_text):
        """格式化为HTML"""
        html_template = """<!DOCTYPE html>
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
    </style>
</head>
<body>
{content}
</body>
</html>"""
        
        return html_template.format(content=processed_text)

def main():
    """主函数"""
    print("=" * 60)
    print("大卫排版应用程序 - 简化版")
    print("David Text Formatting Application - Simple Version")
    print("=" * 60)
    
    # 创建必要目录和文件
    create_directories()
    create_config()
    create_sample_text()
    
    print("\n✓ 安装完成！")
    print("\n使用方法：")
    print("1. 运行示例: python simple_install.py")
    print("2. 处理文件: python simple_install.py your_file.txt")
    
    # 处理示例文本
    print("\n" + "=" * 40)
    print("处理示例文本...")
    
    try:
        with open('examples/sample_text.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        processor = SimpleTextProcessor()
        processed_text = processor.process_text(text)
        html_output = processor.format_for_html(processed_text)
        
        # 保存结果
        with open('output/formatted_sample.html', 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print("✓ 示例文本处理完成！")
        print("✓ 输出文件: output/formatted_sample.html")
        print("✓ 可以在浏览器中打开查看结果")
        
    except Exception as e:
        print(f"✗ 处理失败: {e}")

if __name__ == "__main__":
    main()
