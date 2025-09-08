#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 直接处理版
David Text Formatting Application - Direct Processing Version
直接处理指定的文件，无需用户输入
"""

import os
import re
import webbrowser
from datetime import datetime

def read_text_file(file_path):
    """读取文本文件，尝试多种编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"✓ 成功读取文件，编码: {encoding}")
            return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"✗ 读取文件失败 ({encoding}): {e}")
            continue
    
    raise Exception("无法读取文件，尝试了所有编码格式")

def process_text_with_pagination(text):
    """处理文本并添加分页"""
    # 清理Markdown符号和特殊符号
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # 移除 **text**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # 移除 *text*
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)  # 移除行首的 # 符号
    text = re.sub(r'#+', '', text)  # 移除所有的 # 符号
    text = re.sub(r'[□■▪▫▬▭▮▯]', '', text)  # 移除小方形符号
    text = re.sub(r'[•·◦‣⁃]', '', text)  # 移除项目符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    text = re.sub(r'[▪▫▬▭▮▯]', '', text)  # 移除更多方形符号
    
    # 按段落分割
    paragraphs = text.split('\n\n')
    processed_paragraphs = []
    
    # 页面行数计算（285mm页面高度，减去上下边距45mm，实际内容区域240mm）
    # 12pt字体，1.6倍行距，每行约6.4mm，240mm可容纳约37行
    current_line_count = 0
    max_lines_per_page = 37
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # 估算段落行数
        lines_in_paragraph = max(1, len(paragraph) // 50)  # 粗略估算
        
        # 检查是否需要分页
        if current_line_count + lines_in_paragraph > max_lines_per_page:
            processed_paragraphs.append('<div class="page-break"></div>')
            current_line_count = 0
        
        # 处理标题
        if re.match(r'^第[一二三四五六七八九十\d]+天：', paragraph):
            processed_paragraphs.append(f'<h1>{paragraph}</h1>')
            current_line_count += 3  # 标题占用3行
        elif re.match(r'^分钟 \d+-\d+：', paragraph):
            processed_paragraphs.append(f'<h2>{paragraph}</h2>')
            current_line_count += 2  # 副标题占用2行
        elif re.match(r'^深度技术解析：', paragraph):
            processed_paragraphs.append(f'<h2>{paragraph}</h2>')
            current_line_count += 2
        elif paragraph.startswith('- '):
            # 列表项
            processed_paragraphs.append(f'<li>{paragraph[2:]}</li>')
            current_line_count += 1
        elif re.match(r'^\d+\.', paragraph):
            # 数字列表
            processed_paragraphs.append(f'<li>{paragraph}</li>')
            current_line_count += 1
        else:
            # 普通段落
            processed_paragraphs.append(f'<p class="normal-text">{paragraph}</p>')
            current_line_count += lines_in_paragraph
    
    return '\n\n'.join(processed_paragraphs)

def create_html_template(content):
    """创建HTML模板"""
    html_start = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>大卫排版结果</title>
    <style>
        @page { 
            size: 210mm 285mm; 
            margin: 25mm 25mm 20mm 25mm; 
        }
        
        body { 
            font-family: "Microsoft YaHei", "SimSun", serif; 
            line-height: 1.6; 
            margin: 0;
            padding: 0;
            background-color: #f8f8f8;
            color: #333;
        }
        
        .book-container {
            width: 21cm;
            min-height: 28.5cm;
            margin: 1cm auto;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 25mm 25mm 20mm 25mm;
            box-sizing: border-box;
        }
        
        h1 { 
            font-size: 20pt;
            font-weight: bold; 
            color: #2c3e50; 
            margin: 20pt 0 15pt 0;
            page-break-before: always;
        }
        
        h2 { 
            font-size: 16pt;
            font-weight: bold; 
            color: #34495e; 
            margin: 15pt 0 10pt 0;
        }
        
        p { 
            font-size: 12pt; 
            margin: 8pt 0; 
            text-indent: 2em;
            line-height: 1.6;
        }
        
        p.normal-text {
            text-indent: 2em !important;
            padding-left: 0;
        }
        
        li { 
            font-size: 12pt; 
            margin: 4pt 0; 
            list-style: none;
            padding-left: 0;
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
<body>
    <div class="book-container">
"""
    
    html_end = """
    </div>
</body>
</html>"""
    
    return html_start + content + html_end

def main():
    print("=" * 60)
    print("大卫排版应用程序 - 直接处理版")
    print("David Text Formatting Application - Direct Processing Version")
    print("=" * 60)
    print()
    
    # 创建输出目录
    os.makedirs('output', exist_ok=True)
    
    # 直接处理你的文件
    file_path = r"C:\Users\rudyh\Desktop\新建24文件夹(2024年公司资料）\从普通到卓越主播的技术_20250905143210 (1).txt"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        print("请检查文件路径是否正确")
        input("按任意键退出...")
        return
        
    try:
        print(f"正在读取文件: {file_path}")
        text = read_text_file(file_path)
        print(f"✓ 文件读取成功，字符数: {len(text)}")
        
        print("正在处理文本...")
        processed_text = process_text_with_pagination(text)
        
        # 生成HTML
        html_result = create_html_template(processed_text)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"从普通到卓越主播的技术_排版结果_{timestamp}.html"
        filepath = os.path.join('output', filename)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_result)
        
        print(f"✓ 处理完成！")
        print(f"✓ 输出文件: {filepath}")
        print(f"✓ 分页逻辑: 按28.5cm页面高度智能分页")
        print(f"✓ 纸张尺寸: 210mm × 285mm (大16开)")
        
        # 打开文件
        webbrowser.open(f'file:///{os.path.abspath(filepath)}')
        print("✓ 已在浏览器中打开")
        
    except Exception as e:
        print(f"✗ 处理失败: {e}")
    
    print("\n程序执行完成！")
    input("按任意键退出...")

if __name__ == "__main__":
    main()
