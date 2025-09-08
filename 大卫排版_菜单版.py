#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 菜单版
David Text Formatting Application - Menu Version
"""

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
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        # 处理主要章节标题（第X天：）
        if re.match(r'^第[一二三四五六七八九十\d]+天：', paragraph):
            processed_paragraphs.append('<div class="page-break"></div>')
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
        # 处理分钟标题（分钟 XX-XX：标题）
        elif re.match(r'^分钟 \d+-\d+：', paragraph):
            processed_paragraphs.append(f"<h2>{paragraph}</h2>")
        # 处理技术解析标题
        elif re.match(r'^深度技术解析：', paragraph):
            processed_paragraphs.append(f"<h2>{paragraph}</h2>")
        # 处理列表项
        elif re.match(r'^[•\-\d]+\.', paragraph) or paragraph.startswith('•'):
            lines = paragraph.split('\n')
            list_items = []
            for line in lines:
                line = line.strip()
                if line:
                    if line.startswith('•'):
                        list_items.append(f'<li>{line[1:].strip()}</li>')
                    elif re.match(r'^\d+\.', line):
                        list_items.append(f'<li>{line}</li>')
                    elif line.startswith('- '):
                        list_items.append(f'<li>{line[2:]}</li>')
                    else:
                        list_items.append(f'<li>{line}</li>')
            
            if list_items:
                processed_paragraphs.append('<ul>')
                processed_paragraphs.extend(list_items)
                processed_paragraphs.append('</ul>')
        # 处理引用或重点
        elif '【' in paragraph and '】' in paragraph:
            quote_match = re.search(r'【([^】]+)】', paragraph)
            if quote_match:
                processed_paragraphs.append(f'<blockquote>{quote_match.group(1)}</blockquote>')
            else:
                processed_paragraphs.append(f'<p>{paragraph}</p>')
        # 处理普通段落
        else:
            paragraph = paragraph.replace('\n', ' ')
            processed_paragraphs.append(f'<p>{paragraph}</p>')
    
    processed_text = '\n'.join(processed_paragraphs)
    
    # 创建简单的HTML模板
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>从普通到卓越主播的技术 - 28.5cm版本</title>
    <style>
        body {{ 
            font-family: "Microsoft YaHei", "SimSun", serif; 
            line-height: 1.6; 
            margin: 0; 
            padding: 20px; 
            background-color: #f8f8f8; 
            color: #333; 
        }}
        .book-container {{ 
            max-width: 800px; 
            margin: 0 auto; 
            background-color: white; 
            box-shadow: 0 0 20px rgba(0,0,0,0.1); 
            padding: 40px; 
            border-radius: 10px; 
        }}
        h1 {{ 
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50; 
            margin: 30px 0 20px 0; 
            text-align: center; 
            border-bottom: 2px solid #2c3e50; 
            padding-bottom: 10px; 
        }}
        h2 {{ 
            font-size: 20px; 
            font-weight: bold; 
            color: #34495e; 
            margin: 25px 0 15px 0; 
            border-left: 4px solid #3498db; 
            padding-left: 15px; 
        }}
        p {{ 
            font-size: 16px; 
            text-indent: 2em; 
            margin: 10px 0; 
            line-height: 1.8; 
            text-align: justify; 
        }}
        blockquote {{ 
            background-color: #f8f9fa; 
            border-left: 4px solid #e74c3c; 
            margin: 20px 0; 
            padding: 15px 20px; 
            font-style: italic; 
            font-weight: bold; 
            border-radius: 0 5px 5px 0; 
        }}
        li {{ 
            font-size: 16px; 
            margin: 8px 0; 
            line-height: 1.6; 
        }}
        ul, ol {{ 
            margin: 15px 0; 
            padding-left: 30px; 
        }}
        .page-break {{ 
            border-top: 2px dashed #ccc; 
            margin: 40px 0; 
            padding: 20px 0; 
            text-align: center; 
            color: #666; 
            font-size: 12px; 
        }}
        .page-break::before {{ 
            content: "--- 分页 (28.5cm) ---"; 
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
    print("大卫排版应用程序 - 菜单版")
    print("=" * 60)
    
    # 创建输出目录
    if not os.path.exists('output'):
        os.makedirs('output')
        print("✓ 创建目录: output")
    
    print("\n请选择操作:")
    print("1. 输入文本进行排版")
    print("2. 选择文件进行排版")
    print("3. 使用示例文本")
    print("4. 退出程序")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == '1':
        print("\n请输入要排版的文本内容 (输入完成后按两次回车结束):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        
        text = '\n'.join(lines[:-1])  # 去掉最后的空行
        if text.strip():
            process_and_save(text)
        else:
            print("✗ 没有输入任何内容")
    
    elif choice == '2':
        file_path = input("\n请输入文件路径: ").strip()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                process_and_save(text)
            except Exception as e:
                print(f"✗ 读取文件失败: {e}")
        else:
            print("✗ 文件不存在")
    
    elif choice == '3':
        # 使用示例文本
        sample_text = """第1天：基础准备

分钟 1-5：了解直播行业

直播行业是一个快速发展的新兴产业，具有以下特点：
• 实时互动性强
• 内容形式多样
• 受众群体广泛
• 变现方式灵活

【重点提示】成功的直播需要专业的技术支持和持续的内容创新。

分钟 6-10：设备准备

深度技术解析：直播设备配置

直播设备是成功直播的基础，需要以下核心设备：
1. 摄像头：推荐使用1080p以上分辨率
2. 麦克风：建议使用专业麦克风
3. 灯光：确保画面清晰明亮
4. 网络：稳定的网络连接至关重要

第2天：内容策划

分钟 1-5：内容定位

内容定位是直播成功的关键因素：
• 明确目标受众
• 确定内容主题
• 制定内容计划
• 保持内容一致性

【核心要点】好的内容定位能够吸引精准的粉丝群体，提高直播效果。"""
        
        process_and_save(sample_text)
    
    elif choice == '4':
        print("\n✓ 感谢使用大卫排版应用程序！")
        return
    
    else:
        print("✗ 无效选择，请重新输入")

def process_and_save(text):
    """处理并保存文本"""
    try:
        print("\n正在处理文本...")
        html_result = process_text(text)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"大卫排版结果_{timestamp}.html"
        filepath = os.path.join('output', filename)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_result)
        
        print(f"✓ 处理完成！")
        print(f"✓ 输出文件: {filepath}")
        
        # 询问是否打开文件
        open_file = input("\n是否在浏览器中打开结果？(y/n): ").strip().lower()
        if open_file in ['y', 'yes', '是']:
            try:
                webbrowser.open(f'file:///{os.path.abspath(filepath)}')
                print("✓ 已在浏览器中打开")
            except Exception as e:
                print(f"✗ 打开失败: {e}")
        
    except Exception as e:
        print(f"✗ 处理失败: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ 程序已退出")
    except Exception as e:
        print(f"\n✗ 程序出错: {e}")
        input("按任意键继续...")

