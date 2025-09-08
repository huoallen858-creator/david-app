#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 简化Web版
"""

import os
import re
import webbrowser
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver

class SimpleHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大卫排版应用程序</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        textarea { width: 100%; height: 300px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>大卫排版应用程序</h1>
        <form method="post">
            <textarea name="text" placeholder="请输入要排版的文本内容..."></textarea>
            <br><br>
            <button type="submit">开始排版</button>
        </form>
        <div class="result">
            <h3>功能特点：</h3>
            <ul>
                <li>自动识别标题格式</li>
                <li>清理特殊符号</li>
                <li>智能分页</li>
                <li>专业排版输出</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
            
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 解析表单数据
        text = post_data.decode('utf-8').split('text=')[1].replace('+', ' ').replace('%0A', '\n')
        
        if text.strip():
            try:
                # 处理文本
                processed = self.process_text(text)
                html_result = self.create_html(processed)
                
                # 保存文件
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"大卫排版结果_{timestamp}.html"
                filepath = os.path.join('output', filename)
                
                os.makedirs('output', exist_ok=True)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_result)
                
                # 返回结果页面
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                result_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>排版完成</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        .success {{ color: #28a745; font-size: 18px; text-align: center; }}
        .file-info {{ background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        button {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success">✅ 排版完成！</div>
        <div class="file-info">
            <strong>文件已保存：</strong><br>
            {filename}<br>
            <br>
            <button onclick="window.open('output/{filename}', '_blank')">打开文件</button>
            <button onclick="window.location.href='/'">返回</button>
        </div>
    </div>
</body>
</html>"""
                
                self.wfile.write(result_html.encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                error_html = f"<html><body><h1>错误</h1><p>{str(e)}</p></body></html>"
                self.wfile.write(error_html.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_html = "<html><body><h1>错误</h1><p>请输入文本内容</p></body></html>"
            self.wfile.write(error_html.encode('utf-8'))
    
    def process_text(self, text):
        # 清理符号
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'#+', '', text)
        text = re.sub(r'[□■▪▫▬▭▮▯]', '', text)
        text = re.sub(r'[•·◦‣⁃]', '', text)
        
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
                processed.append(f'<p style="text-indent: 2em;">{paragraph}</p>')
        
        return '\n\n'.join(processed)
    
    def create_html(self, content):
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
        p {{ font-size: 12pt; margin: 8pt 0; }}
        li {{ font-size: 12pt; margin: 4pt 0; list-style: none; }}
    </style>
</head>
<body>
    <div class="book-container">
        {content}
    </div>
</body>
</html>"""

def main():
    print("启动简化Web服务器...")
    print("访问地址: http://localhost:8080")
    
    os.makedirs('output', exist_ok=True)
    
    with socketserver.TCPServer(("", 8080), SimpleHandler) as httpd:
        print("服务器已启动，按 Ctrl+C 停止")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    main()

