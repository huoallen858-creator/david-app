#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 移动Web版
David Text Formatting Application - Mobile Web Version
专为手机浏览器优化的Web应用
"""

import os
import re
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json

class MobileWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = self.get_mobile_html()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/process':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            text = data.get('text', [''])[0]
            
            if not text.strip():
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': '请输入文本内容'}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            try:
                # 处理文本
                processed_text = self.process_text_with_pagination(text)
                html_result = self.create_html_template(processed_text)
                
                # 保存文件
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"大卫排版结果_{timestamp}.html"
                filepath = os.path.join('output', filename)
                
                os.makedirs('output', exist_ok=True)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_result)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'success': True,
                    'message': '排版完成！',
                    'filename': filename,
                    'filepath': filepath
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': f'处理失败: {str(e)}'}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_mobile_html(self):
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大卫排版应用程序 - 移动版</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px 20px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
        }
        
        .form-group textarea {
            width: 100%;
            min-height: 200px;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .features {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .features h3 {
            margin-bottom: 15px;
            color: #333;
        }
        
        .features ul {
            list-style: none;
            padding: 0;
        }
        
        .features li {
            padding: 8px 0;
            color: #666;
        }
        
        .features li:before {
            content: "✓ ";
            color: #28a745;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>大卫排版应用程序</h1>
            <p>David Text Formatting Application - Mobile Version</p>
        </div>
        
        <div class="content">
            <form id="form">
                <div class="form-group">
                    <label for="text">输入要排版的文本内容：</label>
                    <textarea id="text" name="text" placeholder="在此输入要排版的文本内容..."></textarea>
                </div>
                
                <button type="submit" class="btn" id="submitBtn">开始排版</button>
            </form>
            
            <div id="status" class="status" style="display: none;"></div>
            
            <div class="features">
                <h3>功能特点</h3>
                <ul>
                    <li>自动识别标题格式</li>
                    <li>清理特殊符号</li>
                    <li>智能分页</li>
                    <li>专业排版输出</li>
                    <li>大16开尺寸 (210mm × 285mm)</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const text = document.getElementById('text').value.trim();
            const submitBtn = document.getElementById('submitBtn');
            const status = document.getElementById('status');
            
            if (!text) {
                showStatus('请输入文本内容', 'error');
                return;
            }
            
            submitBtn.disabled = true;
            submitBtn.textContent = '正在处理...';
            showStatus('正在处理文本，请稍候...', 'info');
            
            try {
                const formData = new FormData();
                formData.append('text', text);
                
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showStatus(`排版完成！文件已保存为: ${result.filename}`, 'success');
                } else {
                    showStatus(result.error || '处理失败', 'error');
                }
            } catch (error) {
                showStatus('网络错误，请重试', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = '开始排版';
            }
        });
        
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = `status ${type}`;
            status.style.display = 'block';
        }
    </script>
</body>
</html>"""
    
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

def main():
    print("=" * 60)
    print("大卫排版应用程序 - 移动Web版")
    print("David Text Formatting Application - Mobile Web Version")
    print("=" * 60)
    print()
    print("正在启动Web服务器...")
    print("服务器地址: http://localhost:8080")
    print("手机访问: http://你的电脑IP:8080")
    print()
    print("按 Ctrl+C 停止服务器")
    print()
    
    # 创建输出目录
    os.makedirs('output', exist_ok=True)
    
    # 启动服务器
    server = HTTPServer(('0.0.0.0', 8080), MobileWebHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.shutdown()

if __name__ == "__main__":
    main()

