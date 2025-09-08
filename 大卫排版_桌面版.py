#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 桌面版
David Text Formatting Application - Desktop Version
"""

import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser
import threading

class DavidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 大卫排版应用程序")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')
        
        # 创建输出目录
        if not os.path.exists('output'):
            os.makedirs('output')
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="📚 大卫排版应用程序", 
                               font=("Microsoft YaHei", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="📁 选择文本文件", 
                  command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="未选择文件", 
                                   foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=tk.W)
        
        # 文本输入区域
        text_frame = ttk.LabelFrame(main_frame, text="文本内容", padding="10")
        text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.text_input = scrolledtext.ScrolledText(text_frame, height=15, width=70,
                                                   font=("Microsoft YaHei", 10))
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="🚀 开始排版", 
                  command=self.process_text).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="💾 保存结果", 
                  command=self.save_result).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(button_frame, text="👁️ 预览结果", 
                  command=self.preview_result).grid(row=0, column=2)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # 存储处理结果
        self.processed_html = ""
        
    def select_file(self):
        """选择文件"""
        file_path = filedialog.askopenfilename(
            title="选择文本文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(1.0, content)
                self.file_label.config(text=f"已选择: {os.path.basename(file_path)}", 
                                      foreground="green")
                self.status_var.set("文件加载成功")
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {e}")
                self.status_var.set("文件读取失败")
    
    def process_text(self):
        """处理文本"""
        text = self.text_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "请输入要排版的文本内容！")
            return
        
        self.status_var.set("正在处理文本...")
        self.root.update()
        
        try:
            # 在新线程中处理，避免界面卡顿
            thread = threading.Thread(target=self._process_text_thread, args=(text,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            messagebox.showerror("错误", f"处理失败: {e}")
            self.status_var.set("处理失败")
    
    def _process_text_thread(self, text):
        """处理文本的线程函数"""
        try:
            self.processed_html = self.process_text_content(text)
            self.root.after(0, self._process_complete)
        except Exception as e:
            self.root.after(0, lambda: self._process_error(str(e)))
    
    def _process_complete(self):
        """处理完成"""
        self.status_var.set("文本处理完成！")
        messagebox.showinfo("成功", "文本处理完成！\n可以预览或保存结果。")
    
    def _process_error(self, error_msg):
        """处理错误"""
        self.status_var.set("处理失败")
        messagebox.showerror("错误", f"处理失败: {error_msg}")
    
    def process_text_content(self, text):
        """处理文本内容"""
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
        
        # 创建HTML模板
        html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>从普通到卓越主播的技术 - 28.5cm版本</title>
    <style>
        @page { size: 184mm 285mm; margin: 25mm 25mm 20mm 25mm; }
        body { font-family: "Microsoft YaHei", "SimSun", serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f8f8f8; color: #333; }
        .book-container { width: 18.4cm; min-height: 28.5cm; margin: 1cm auto; background-color: white; box-shadow: 0 0 20px rgba(0,0,0,0.1); padding: 25mm 25mm 20mm 25mm; box-sizing: border-box; }
        h1 { font-size: 20pt; font-weight: bold; color: #2c3e50; margin: 30pt 0 15pt 0; text-align: center; border-bottom: 2pt solid #2c3e50; padding-bottom: 8pt; line-height: 1.3; }
        h2 { font-size: 16pt; font-weight: bold; color: #34495e; margin: 20pt 0 12pt 0; border-left: 3pt solid #3498db; padding-left: 10pt; line-height: 1.4; }
        p { font-size: 12pt; text-indent: 2em; margin: 6pt 0; line-height: 1.6; text-align: justify; }
        blockquote { background-color: #f8f9fa; border-left: 4pt solid #e74c3c; margin: 12pt 0; padding: 10pt 12pt; font-style: italic; font-weight: bold; font-size: 11pt; border-radius: 0 3pt 3pt 0; }
        li { font-size: 12pt; margin: 3pt 0; line-height: 1.5; }
        ul, ol { margin: 8pt 0; padding-left: 18pt; }
        .page-break { page-break-before: always; break-before: page; }
        @media print { body { background-color: white; } .book-container { box-shadow: none; margin: 0; width: 100%; min-height: 100vh; } .page-break { page-break-before: always; } }
        @media screen { body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px 0; } .page-break { border-top: 2px dashed #ccc; margin: 30px 0; padding: 10px 0; text-align: center; color: #666; font-size: 10pt; } .page-break::before { content: "--- 分页 (28.5cm) ---"; } }
    </style>
</head>
<body>
    <div class="book-container">
{content}
    </div>
</body>
</html>"""
        
        return html_template.format(content=processed_text)
    
    def save_result(self):
        """保存结果"""
        if not self.processed_html:
            messagebox.showwarning("警告", "请先处理文本！")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存HTML文件",
            defaultextension=".html",
            filetypes=[("HTML文件", "*.html"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.processed_html)
                messagebox.showinfo("成功", f"文件已保存到:\n{file_path}")
                self.status_var.set("文件保存成功")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
                self.status_var.set("保存失败")
    
    def preview_result(self):
        """预览结果"""
        if not self.processed_html:
            messagebox.showwarning("警告", "请先处理文本！")
            return
        
        # 保存临时文件
        temp_file = os.path.join('output', 'preview.html')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(self.processed_html)
            
            # 在浏览器中打开
            webbrowser.open(f'file:///{os.path.abspath(temp_file)}')
            self.status_var.set("预览已打开")
        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {e}")
            self.status_var.set("预览失败")

def main():
    root = tk.Tk()
    app = DavidApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

