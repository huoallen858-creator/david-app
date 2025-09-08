#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 简化Android版
David Text Formatting Application - Simple Android Version
"""

import os
import re
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window

class DavidSimpleApp(App):
    def build(self):
        Window.size = (360, 640)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='大卫排版应用程序',
            size_hint_y=None,
            height=60,
            font_size=24,
            halign='center'
        )
        layout.add_widget(title)
        
        # 文本输入
        text_label = Label(
            text='输入要排版的文本：',
            size_hint_y=None,
            height=30
        )
        layout.add_widget(text_label)
        
        self.text_input = TextInput(
            hint_text='在此输入文本内容...',
            multiline=True,
            size_hint_y=0.6
        )
        layout.add_widget(self.text_input)
        
        # 按钮
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        process_btn = Button(
            text='开始排版',
            on_press=self.process_text
        )
        
        clear_btn = Button(
            text='清空',
            on_press=self.clear_text
        )
        
        button_layout.add_widget(process_btn)
        button_layout.add_widget(clear_btn)
        layout.add_widget(button_layout)
        
        # 状态标签
        self.status_label = Label(
            text='准备就绪',
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.status_label)
        
        return layout
    
    def clear_text(self, instance):
        self.text_input.text = ''
        self.status_label.text = '已清空'
    
    def process_text(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self.show_popup('错误', '请输入文本内容')
            return
        
        try:
            self.status_label.text = '正在处理...'
            
            # 处理文本
            processed_text = self.process_text_simple(text)
            
            # 生成HTML
            html_result = self.create_html_simple(processed_text)
            
            # 保存文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"大卫排版结果_{timestamp}.html"
            filepath = os.path.join(os.path.expanduser('~'), 'Downloads', filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_result)
            
            self.status_label.text = '处理完成！'
            self.show_popup('成功', f'排版完成！\n文件已保存到:\n{filepath}')
            
        except Exception as e:
            self.show_popup('错误', f'处理失败: {e}')
            self.status_label.text = '处理失败'
    
    def process_text_simple(self, text):
        # 清理符号
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'#+', '', text)
        text = re.sub(r'[□■▪▫▬▭▮▯]', '', text)
        text = re.sub(r'[•·◦‣⁃]', '', text)
        
        # 多次清理
        for _ in range(10):
            text = re.sub(r'[▪▫▬▭▮▯]', '', text)
        
        # 处理段落
        paragraphs = text.split('\n\n')
        processed = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            if re.match(r'^第[一二三四五六七八九十\d]+天：', paragraph):
                processed.append(f'<h1>{paragraph}</h1>')
            elif re.match(r'^分钟 \d+-\d+：', paragraph):
                processed.append(f'<h2>{paragraph}</h2>')
            elif re.match(r'^深度技术解析：', paragraph):
                processed.append(f'<h2>{paragraph}</h2>')
            elif paragraph.startswith('- '):
                processed.append(f'<li>{paragraph[2:]}</li>')
            elif re.match(r'^\d+\.', paragraph):
                processed.append(f'<li>{paragraph}</li>')
            else:
                processed.append(f'<p class="normal-text">{paragraph}</p>')
        
        return '\n\n'.join(processed)
    
    def create_html_simple(self, content):
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>大卫排版结果</title>
    <style>
        @page {{ size: 210mm 285mm; margin: 25mm; }}
        body {{ font-family: "Microsoft YaHei", serif; line-height: 1.6; margin: 0; padding: 20px; }}
        .book-container {{ max-width: 21cm; margin: 0 auto; background: white; padding: 25mm; }}
        h1 {{ font-size: 20pt; font-weight: bold; color: #2c3e50; margin: 20pt 0 15pt 0; }}
        h2 {{ font-size: 16pt; font-weight: bold; color: #34495e; margin: 15pt 0 10pt 0; }}
        p {{ font-size: 12pt; margin: 8pt 0; text-indent: 2em; }}
        p.normal-text {{ text-indent: 2em !important; }}
        li {{ font-size: 12pt; margin: 4pt 0; list-style: none; }}
    </style>
</head>
<body>
    <div class="book-container">
        {content}
    </div>
</body>
</html>"""
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == '__main__':
    DavidSimpleApp().run()

