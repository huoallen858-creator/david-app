#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序启动器
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
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>从普通到卓越主播的技术 - 大卫排版</title>
    <style>
        @page {{
            size: 184mm 285mm;
            margin: 25mm 25mm 20mm 25mm;
        }}
        
        body {{ 
            font-family: "Microsoft YaHei", "SimSun", serif; 
            line-height: 1.6; 
            margin: 0;
            padding: 0;
            background-color: #f8f8f8;
            color: #333;
        }}
        
        .book-container {{
            width: 18.4cm;
            min-height: 28.5cm;
            margin: 1cm auto;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 25mm 25mm 20mm 25mm;
            box-sizing: border-box;
        }}
        
        h1 {{ 
            font-size: 20pt;
            font-weight: bold; 
            color: #2c3e50; 
            margin: 30pt 0 15pt 0;
            text-align: center; 
            border-bottom: 2pt solid #2c3e50; 
            padding-bottom: 8pt; 
            line-height: 1.3;
        }}
        
        h2 {{ 
            font-size: 16pt;
            font-weight: bold; 
            color: #34495e; 
            margin: 20pt 0 12pt 0; 
            border-left: 3pt solid #3498db;
            padding-left: 10pt;
            line-height: 1.4;
        }}
        
        p {{ 
            font-size: 12pt;
            text-indent: 2em; 
            margin: 6pt 0; 
            line-height: 1.6; 
            text-align: justify;
        }}
        
        p.question {{
            font-size: 14pt;
            font-weight: bold;
            color: #e74c3c;
            text-align: center;
            margin: 15pt 0;
            text-indent: 0;
        }}
        
        blockquote {{ 
            background-color: #f8f9fa; 
            border-left: 4pt solid #e74c3c; 
            margin: 12pt 0; 
            padding: 10pt 12pt; 
            font-style: italic; 
            font-weight: bold;
            font-size: 11pt;
            border-radius: 0 3pt 3pt 0;
        }}
        
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}
        
        @media print {{
            body {{
                background-color: white;
            }}
            .book-container {{
                box-shadow: none;
                margin: 0;
                width: 100%;
                min-height: 28.5cm;
            }}
            .page-break {{
                page-break-before: always;
            }}
        }}
        
        @media screen {{
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px 0;
            }}
            .page-break {{
                border-top: 3px dashed #e74c3c;
                margin: 40px 0;
                padding: 15px 0;
                text-align: center;
                color: #e74c3c;
                font-size: 12pt;
                font-weight: bold;
                background-color: rgba(231, 76, 60, 0.1);
            }}
            .page-break::before {{
                content: "📄 分页 - 28.5cm 📄";
            }}
        }}
    </style>
</head>
<body>
    <div class="book-container">
{processed_text}
    </div>
</body>
</html>"""
    
    return html_content

def main():
    print("=" * 60)
    print("大卫排版应用程序")
    print("=" * 60)
    
    # 创建输出目录
    if not os.path.exists('output'):
        os.makedirs('output')
    
    print("请选择操作:")
    print("1. 处理你的文本文件")
    print("2. 处理示例文本")
    print("3. 退出")
    
    try:
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == '1':
            # 处理用户文本文件
            file_path = r"C:\Users\rudyh\Desktop\新建24文件夹(2024年公司资料）\从普通到卓越主播的技术_20250905143210 (1).txt"
            
            if os.path.exists(file_path):
                print(f"正在处理文件: {file_path}")
                text = read_file_with_encoding(file_path)
                if text:
                    process_and_save(text, "从普通到卓越主播的技术_完整版")
                else:
                    print("无法读取文件")
            else:
                print("文件不存在，请检查路径")
        
        elif choice == '2':
            # 处理示例文本
            if os.path.exists('user_content.txt'):
                with open('user_content.txt', 'r', encoding='utf-8') as f:
                    text = f.read()
                process_and_save(text, "示例文本排版")
            else:
                print("示例文件不存在")
        
        elif choice == '3':
            print("退出程序")
            return
        
        else:
            print("无效选择")
    
    except Exception as e:
        print(f"程序出错: {e}")
    
    input("\n按任意键退出...")

def process_and_save(text, name):
    """处理并保存文本"""
    try:
        print("正在处理文本...")
        html_result = process_text(text)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.html"
        filepath = os.path.join('output', filename)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_result)
        
        print(f"✓ 处理完成！")
        print(f"✓ 输出文件: {filepath}")
        
        # 打开文件
        webbrowser.open(f'file:///{os.path.abspath(filepath)}')
        print("✓ 已在浏览器中打开")
        
    except Exception as e:
        print(f"✗ 处理失败: {e}")

if __name__ == "__main__":
    main()


