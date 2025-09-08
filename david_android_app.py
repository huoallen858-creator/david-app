#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - Android版
David Text Formatting Application - Android Version
使用Kivy框架创建的移动应用
"""

import os
import re
import webbrowser
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

class DavidApp(App):
    def build(self):
        # 设置窗口大小（手机屏幕尺寸）
        Window.size = (360, 640)
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='大卫排版应用程序\nDavid Text Formatting App',
            size_hint_y=None,
            height=80,
            font_size=20,
            halign='center'
        )
        main_layout.add_widget(title)
        
        # 文件选择区域
        file_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        self.file_input = TextInput(
            hint_text='请输入文件路径或选择文件',
            multiline=False,
            size_hint_x=0.7
        )
        
        select_btn = Button(
            text='选择文件',
            size_hint_x=0.3,
            on_press=self.show_file_chooser
        )
        
        file_layout.add_widget(self.file_input)
        file_layout.add_widget(select_btn)
        main_layout.add_widget(file_layout)
        
        # 文本输入区域
        text_label = Label(
            text='或者直接输入文本内容：',
            size_hint_y=None,
            height=30
        )
        main_layout.add_widget(text_label)
        
        self.text_input = TextInput(
            hint_text='在此输入要排版的文本内容...',
            multiline=True,
            size_hint_y=0.4
        )
        main_layout.add_widget(self.text_input)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        process_btn = Button(
            text='开始排版',
            on_press=self.process_text
        )
        
        clear_btn = Button(
            text='清空',
            on_press=self.clear_inputs
        )
        
        button_layout.add_widget(process_btn)
        button_layout.add_widget(clear_btn)
        main_layout.add_widget(button_layout)
        
        # 进度条
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=20
        )
        main_layout.add_widget(self.progress)
        
        # 状态标签
        self.status_label = Label(
            text='准备就绪',
            size_hint_y=None,
            height=30
        )
        main_layout.add_widget(self.status_label)
        
        return main_layout
    
    def show_file_chooser(self, instance):
        """显示文件选择器"""
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.txt', '*.md']
        )
        
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        select_btn = Button(text='选择', on_press=lambda x: self.select_file(filechooser.path, filechooser.selection))
        cancel_btn = Button(text='取消', on_press=lambda x: self.popup.dismiss())
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(filechooser)
        content.add_widget(btn_layout)
        
        self.popup = Popup(
            title='选择文件',
            content=content,
            size_hint=(0.9, 0.9)
        )
        self.popup.open()
    
    def select_file(self, path, selection):
        """选择文件"""
        if selection:
            file_path = selection[0]
            self.file_input.text = file_path
        self.popup.dismiss()
    
    def clear_inputs(self, instance):
        """清空输入"""
        self.file_input.text = ''
        self.text_input.text = ''
        self.status_label.text = '已清空'
    
    def process_text(self, instance):
        """处理文本"""
        self.status_label.text = '正在处理...'
        self.progress.value = 10
        
        # 获取文本内容
        text = ''
        if self.file_input.text and os.path.exists(self.file_input.text):
            # 从文件读取
            try:
                text = self.read_text_file(self.file_input.text)
                self.progress.value = 30
            except Exception as e:
                self.show_error(f"读取文件失败: {e}")
                return
        elif self.text_input.text.strip():
            # 从输入框读取
            text = self.text_input.text
            self.progress.value = 30
        else:
            self.show_error("请选择文件或输入文本内容")
            return
        
        if not text.strip():
            self.show_error("文本内容为空")
            return
        
        # 处理文本
        try:
            self.progress.value = 50
            processed_text = self.process_text_with_pagination(text)
            self.progress.value = 70
            
            # 生成HTML
            html_result = self.create_html_template(processed_text)
            self.progress.value = 80
            
            # 保存文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"大卫排版结果_{timestamp}.html"
            filepath = os.path.join(os.path.expanduser('~'), 'Downloads', filename)
            
            # 确保下载目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_result)
            
            self.progress.value = 100
            self.status_label.text = f'处理完成！文件已保存到: {filepath}'
            
            # 显示成功消息
            self.show_success(f"排版完成！\n文件已保存到:\n{filepath}")
            
        except Exception as e:
            self.show_error(f"处理失败: {e}")
    
    def read_text_file(self, file_path):
        """读取文本文件，尝试多种编码"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                continue
        
        raise Exception("无法读取文件，尝试了所有编码格式")
    
    def process_text_with_pagination(self, text):
        """处理文本并添加分页"""
        # 清理Markdown符号和特殊符号
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # 移除 **text**
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # 移除 *text*
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)  # 移除行首的 # 符号
        text = re.sub(r'#+', '', text)  # 移除所有的 # 符号
        text = re.sub(r'[□■▪▫▬▭▮▯]', '', text)  # 移除小方形符号
        text = re.sub(r'[•·◦‣⁃]', '', text)  # 移除项目符号
        
        # 多次清理确保彻底
        for _ in range(10):
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
    
    def create_html_template(self, content):
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
    
    def show_error(self, message):
        """显示错误消息"""
        popup = Popup(
            title='错误',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()
        self.status_label.text = '处理失败'
        self.progress.value = 0
    
    def show_success(self, message):
        """显示成功消息"""
        popup = Popup(
            title='成功',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == '__main__':
    DavidApp().run()

