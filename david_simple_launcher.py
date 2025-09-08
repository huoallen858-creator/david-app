#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 简单启动器
"""

import os
import re
import webbrowser
from datetime import datetime

def read_file_with_encoding(file_path):
    """尝试不同编码读取文件"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except:
            continue
    return None

def process_text(text):
    """处理文本"""
    # 先去掉Markdown格式的*符号
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    # 按段落分割
    paragraphs = text.split('\n\n')
    processed_paragraphs = []
    
    # 页面行数计算（28.5cm页面，每页约47行）
    current_line_count = 0
    max_lines_per_page = 47
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        # 估算段落行数
        estimated_lines = max(1, len(paragraph) // 80 + 1)
        
        # 检查是否需要分页
        if current_line_count > 0 and (current_line_count + estimated_lines) > max_lines_per_page:
            processed_paragraphs.append('<div class="page-break"></div>')
            current_line_count = 0
        
        # 处理标题
        if paragraph == "从普通到卓越主播的技术":
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        elif paragraph.startswith("前言："):
            if current_line_count > 0:
                processed_paragraphs.append('<div class="page-break"></div>')
                current_line_count = 0
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        elif re.match(r'^第[一二三四五六七八九十\d]+章[:：]', paragraph):
            if current_line_count > 0:
                processed_paragraphs.append('<div class="page-break"></div>')
                current_line_count = 0
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        elif paragraph in ["迅速增加许多观众的直播技术、迅速增加直播业绩的方法", 
                          "直播卖货就是消费心理学的技术", 
                          "哈佛大学、沃顿商学院的商业圣经"]:
            processed_paragraphs.append(f"<h2>{paragraph}</h2>")
            current_line_count += 2
        elif '【' in paragraph and '】' in paragraph:
            quote_match = re.search(r'【([^】]+)】', paragraph)
            if quote_match:
                processed_paragraphs.append(f'<blockquote>{quote_match.group(1)}</blockquote>')
                current_line_count += 2
            else:
                processed_paragraphs.append(f'<p>{paragraph}</p>')
                current_line_count += estimated_lines
        elif paragraph.endswith('？') or paragraph == "为什么？":
            processed_paragraphs.append(f'<p class="question">{paragraph}</p>')
            current_line_count += 1
        else:
            paragraph = paragraph.replace('\n', ' ')
            processed_paragraphs.append(f'<p>{paragraph}</p>')
            current_line_count += estimated_lines
    
    processed_text = '\n'.join(processed_paragraphs)
    
    # 创建HTML模板
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>从普通到卓越主播的技术 - 大卫排版</title>
    <style>
        body { 
            font-family: "Microsoft YaHei", "SimSun", serif; 
            line-height: 1.6; 
            margin: 0;
            padding: 20px;
            background-color: #f8f8f8;
            color: #333;
        }
        
        .book-container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 40px;
            border-radius: 10px;
        }
        
        h1 { 
            font-size: 24px;
            font-weight: bold; 
            color: #2c3e50; 
            margin: 30px 0 20px 0;
            text-align: center; 
            border-bottom: 2px solid #2c3e50; 
            padding-bottom: 10px; 
        }
        
        h2 { 
            font-size: 20px;
            font-weight: bold; 
            color: #34495e; 
            margin: 25px 0 15px 0; 
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        
        p { 
            font-size: 16px;
            text-indent: 2em; 
            margin: 10px 0; 
            line-height: 1.8; 
            text-align: justify;
        }
        
        p.question {
            font-size: 18px;
            font-weight: bold;
            color: #e74c3c;
            text-align: center;
            margin: 20px 0;
            text-indent: 0;
        }
        
        blockquote { 
            background-color: #f8f9fa; 
            border-left: 4px solid #e74c3c; 
            margin: 20px 0; 
            padding: 15px 20px; 
            font-style: italic; 
            font-weight: bold;
            border-radius: 0 5px 5px 0;
        }
        
        .page-break {
            border-top: 3px dashed #e74c3c;
            margin: 40px 0;
            padding: 15px 0;
            text-align: center;
            color: #e74c3c;
            font-size: 14px;
            font-weight: bold;
            background-color: rgba(231, 76, 60, 0.1);
        }
        
        .page-break::before {
            content: "📄 分页 - 28.5cm 📄";
        }
    </style>
</head>
<body>
    <div class="book-container">
{content}
    </div>
</body>
</html>"""
    
    return html_template.replace('{content}', processed_text)

def main():
    print("=" * 60)
    print("大卫排版应用程序 - 简单启动器")
    print("=" * 60)
    
    # 创建输出目录
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # 直接处理你的32万字文档
    file_path = r"C:\Users\rudyh\Desktop\新建24文件夹(2024年公司资料）\从普通到卓越主播的技术_20250905143210 (1).txt"
    
    if os.path.exists(file_path):
        print(f"正在处理你的32万字文档...")
        print(f"文件路径: {file_path}")
        
        text = read_file_with_encoding(file_path)
        if text:
            print(f"✓ 成功读取文件，字符数: {len(text):,}")
            
            try:
                print("正在处理文本...")
                html_result = process_text(text)
                
                # 生成文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"从普通到卓越主播的技术_完整版_{timestamp}.html"
                filepath = os.path.join('output', filename)
                
                # 保存文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_result)
                
                print(f"✓ 处理完成！")
                print(f"✓ 输出文件: {filepath}")
                print(f"✓ 分页逻辑: 按28.5cm页面高度智能分页")
                
                # 打开文件
                webbrowser.open(f'file:///{os.path.abspath(filepath)}')
                print("✓ 已在浏览器中打开")
                
            except Exception as e:
                print(f"✗ 处理失败: {e}")
        else:
            print("✗ 无法读取文件")
    else:
        print("✗ 文件不存在")
        print("请检查文件路径是否正确")
    
    print("\n程序执行完成！")
    input("按任意键退出...")

if __name__ == "__main__":
    main()
