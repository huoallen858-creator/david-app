#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import webbrowser
from datetime import datetime

def process_text(text):
    """处理文本"""
    # 先去掉Markdown格式的*符号
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    # 按段落分割
    paragraphs = text.split('\n\n')
    processed_paragraphs = []
    
    # 页面行数计算（28.5cm页面，每行约0.6cm，大约47行）
    current_line_count = 0
    max_lines_per_page = 47
    
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        # 估算段落行数
        estimated_lines = max(1, len(paragraph) // 80 + 1)  # 每行约80字符
        
        # 检查是否需要分页（除了第一页）
        if current_line_count > 0 and (current_line_count + estimated_lines) > max_lines_per_page:
            processed_paragraphs.append('<div class="page-break"></div>')
            current_line_count = 0
        
        # 处理标题（从普通到卓越主播的技术）
        if paragraph == "从普通到卓越主播的技术":
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3  # 标题占3行
        # 处理前言标题
        elif paragraph.startswith("前言："):
            # 前言开始新页
            if current_line_count > 0:
                processed_paragraphs.append('<div class="page-break"></div>')
                current_line_count = 0
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        # 处理其他可能的标题
        elif re.match(r'^第[一二三四五六七八九十\d]+章[:：]', paragraph):
            # 章节开始新页
            if current_line_count > 0:
                processed_paragraphs.append('<div class="page-break"></div>')
                current_line_count = 0
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        # 处理二级标题
        elif paragraph in ["迅速增加许多观众的直播技术、迅速增加直播业绩的方法", 
                          "直播卖货就是消费心理学的技术", 
                          "哈佛大学、沃顿商学院的商业圣经"]:
            processed_paragraphs.append(f"<h2>{paragraph}</h2>")
            current_line_count += 2  # 二级标题占2行
        # 处理引用或重点
        elif '【' in paragraph and '】' in paragraph:
            quote_match = re.search(r'【([^】]+)】', paragraph)
            if quote_match:
                processed_paragraphs.append(f'<blockquote>{quote_match.group(1)}</blockquote>')
                current_line_count += 2
            else:
                processed_paragraphs.append(f'<p>{paragraph}</p>')
                current_line_count += estimated_lines
        # 处理问句
        elif paragraph.endswith('？') or paragraph == "为什么？":
            processed_paragraphs.append(f'<p class="question">{paragraph}</p>')
            current_line_count += 1
        # 处理普通段落
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
            size: 184mm 285mm; /* 16开宽度 × 28.5cm高度 */
            margin: 25mm 25mm 20mm 25mm; /* 上25mm，右25mm，下20mm，左25mm */
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
            width: 18.4cm; /* 16开宽度：184mm */
            min-height: 28.5cm; /* 28.5cm高度 */
            margin: 1cm auto;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 25mm 25mm 20mm 25mm; /* 上25mm，右25mm，下20mm，左25mm */
            box-sizing: border-box;
        }}
        
        h1 {{ 
            font-size: 20pt; /* 16开标题1：加大2号 */
            font-weight: bold; 
            color: #2c3e50; 
            margin: 30pt 0 15pt 0;
            text-align: center; 
            border-bottom: 2pt solid #2c3e50; 
            padding-bottom: 8pt; 
            line-height: 1.3;
        }}
        
        h2 {{ 
            font-size: 16pt; /* 16开标题2：加大2号 */
            font-weight: bold; 
            color: #34495e; 
            margin: 20pt 0 12pt 0; 
            border-left: 3pt solid #3498db;
            padding-left: 10pt;
            line-height: 1.4;
        }}
        
        p {{ 
            font-size: 12pt; /* 16开正文：加大2号 */
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
            font-size: 11pt; /* 16开引用：加大2号 */
            border-radius: 0 3pt 3pt 0;
        }}
        
        li {{ 
            font-size: 12pt; /* 16开列表：加大2号 */
            margin: 3pt 0; 
            line-height: 1.5;
        }}
        
        ul, ol {{ 
            margin: 8pt 0; 
            padding-left: 18pt; 
        }}
        
        /* 分页样式 */
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}
        
        /* 打印样式 */
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
        
        /* 屏幕预览样式 */
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
                content: "📄 第 " counter(page) " 页结束 - 28.5cm 分页 📄";
                counter-increment: page;
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
    print("大卫排版应用程序 - 修复分页版本")
    print("=" * 60)
    
    # 创建输出目录
    if not os.path.exists('output'):
        os.makedirs('output')
        print("✓ 创建目录: output")
    
    try:
        # 读取用户文本
        with open('user_content.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        print("✓ 成功读取用户文本")
        print("正在处理文本（修复分页逻辑）...")
        
        html_result = process_text(text)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"从普通到卓越主播的技术_分页修复_{timestamp}.html"
        filepath = os.path.join('output', filename)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_result)
        
        print(f"✓ 处理完成！")
        print(f"✓ 输出文件: {filepath}")
        print("✓ 分页逻辑已修复：")
        print("  - 按28.5cm页面高度计算分页")
        print("  - 只有前言和章节标题强制分页")
        print("  - 其他内容按页面容量自动分页")
        
        # 打开文件
        webbrowser.open(f'file:///{os.path.abspath(filepath)}')
        print("✓ 已在浏览器中打开")
        
    except Exception as e:
        print(f"✗ 处理失败: {e}")
    
    input("\n按任意键退出...")

if __name__ == "__main__":
    main()

