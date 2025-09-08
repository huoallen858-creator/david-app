#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序 - 修复版
David Text Formatting Application - Fixed Version
"""

import os
import re
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import threading
import time

class DavidWebHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_index_html().encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/process':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                result = self.process_text(data['text'])
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'html': result}).encode('utf-8'))
            except Exception as e:
                print(f"处理错误: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_index_html(self):
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>大卫排版应用程序</title>
    <style>
        body { font-family: "Microsoft YaHei", sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .upload-area { border: 2px dashed #3498db; padding: 40px; text-align: center; margin-bottom: 20px; border-radius: 10px; cursor: pointer; }
        .upload-area:hover { background-color: #f8f9fa; }
        .btn { background: #3498db; color: white; border: none; padding: 15px 30px; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px; }
        .btn:hover { background: #2980b9; }
        .text-area { width: 100%; height: 300px; border: 1px solid #ddd; padding: 15px; font-size: 14px; margin-bottom: 20px; border-radius: 5px; }
        .status { padding: 15px; margin: 20px 0; border-radius: 5px; display: none; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .file-input { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 大卫排版应用程序</h1>
        
        <div class="upload-area" onclick="document.getElementById('fileInput').click()">
            <div style="font-size: 48px; color: #3498db; margin-bottom: 20px;">📁</div>
            <div>点击选择文件或拖拽文件到此处</div>
            <input type="file" id="fileInput" class="file-input" accept=".txt">
        </div>
        
        <div class="status" id="status"></div>
        
        <textarea id="textInput" class="text-area" placeholder="请在此处输入或粘贴要排版的文本内容..."></textarea>
        
        <div style="text-align: center;">
            <button class="btn" onclick="processText()">🚀 开始排版</button>
            <button class="btn" onclick="downloadResult()" id="downloadBtn" style="display: none;">💾 下载结果</button>
        </div>
    </div>
    
    <script>
        let processedHtml = '';
        
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('textInput').value = e.target.result;
                    showStatus('文件读取成功！', 'success');
                };
                reader.readAsText(file, 'utf-8');
            }
        });
        
        async function processText() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                showStatus('请输入要排版的文本内容！', 'error');
                return;
            }
            
            showStatus('正在处理文本...', 'success');
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    processedHtml = result.html;
                    showStatus('文本处理完成！', 'success');
                    document.getElementById('downloadBtn').style.display = 'inline-block';
                } else {
                    showStatus('处理失败: ' + result.message, 'error');
                }
            } catch (error) {
                showStatus('处理失败: ' + error.message, 'error');
            }
        }
        
        function downloadResult() {
            if (!processedHtml) return;
            
            const blob = new Blob([processedHtml], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '大卫排版结果.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
        
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
            
            setTimeout(() => {
                status.style.display = 'none';
            }, 3000);
        }
    </script>
</body>
</html>"""
    
    def process_text(self, text):
        # 先去掉Markdown格式的*符号
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        
        # 按段落分割，而不是按行分割
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
            # 处理列表项（以•、-、数字开头）
            elif re.match(r'^[•\-\d]+\.', paragraph) or paragraph.startswith('•'):
                # 处理列表项，保持原有格式
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
                # 将段落内的换行符替换为空格，保持段落完整性
                paragraph = paragraph.replace('\n', ' ')
                processed_paragraphs.append(f'<p>{paragraph}</p>')
        
        processed_text = '\n'.join(processed_paragraphs)
        
        # 创建HTML模板
        html_start = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>从普通到卓越主播的技术 - 28.5cm版本</title>\n    <style>\n        @page { size: 184mm 285mm; margin: 25mm 25mm 20mm 25mm; }\n        body { font-family: "Microsoft YaHei", "SimSun", serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f8f8f8; color: #333; }\n        .book-container { width: 18.4cm; min-height: 28.5cm; margin: 1cm auto; background-color: white; box-shadow: 0 0 20px rgba(0,0,0,0.1); padding: 25mm 25mm 20mm 25mm; box-sizing: border-box; }\n        h1 { font-size: 20pt; font-weight: bold; color: #2c3e50; margin: 30pt 0 15pt 0; text-align: center; border-bottom: 2pt solid #2c3e50; padding-bottom: 8pt; line-height: 1.3; }\n        h2 { font-size: 16pt; font-weight: bold; color: #34495e; margin: 20pt 0 12pt 0; border-left: 3pt solid #3498db; padding-left: 10pt; line-height: 1.4; }\n        p { font-size: 12pt; text-indent: 2em; margin: 6pt 0; line-height: 1.6; text-align: justify; }\n        blockquote { background-color: #f8f9fa; border-left: 4pt solid #e74c3c; margin: 12pt 0; padding: 10pt 12pt; font-style: italic; font-weight: bold; font-size: 11pt; border-radius: 0 3pt 3pt 0; }\n        li { font-size: 12pt; margin: 3pt 0; line-height: 1.5; }\n        ul, ol { margin: 8pt 0; padding-left: 18pt; }\n        .page-break { page-break-before: always; break-before: page; }\n        @media print { body { background-color: white; } .book-container { box-shadow: none; margin: 0; width: 100%; min-height: 100vh; } .page-break { page-break-before: always; } }\n        @media screen { body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px 0; } .page-break { border-top: 2px dashed #ccc; margin: 30px 0; padding: 10px 0; text-align: center; color: #666; font-size: 10pt; } .page-break::before { content: "--- 分页 (28.5cm) ---"; } }\n    </style>\n</head>\n<body>\n    <div class="book-container">\n'
        
        html_end = '\n    </div>\n</body>\n</html>'
        
        return html_start + processed_text + html_end

def open_browser_delayed(url, delay=2):
    """延迟打开浏览器"""
    def open_browser():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"无法自动打开浏览器: {e}")
            print(f"请手动访问: {url}")
    
    thread = threading.Thread(target=open_browser)
    thread.daemon = True
    thread.start()

def main():
    print("=" * 60)
    print("大卫排版应用程序 - 修复版")
    print("=" * 60)
    
    # 创建输出目录
    if not os.path.exists('output'):
        os.makedirs('output')
        print("✓ 创建目录: output")
    
    # 启动服务器
    port = 8080
    server_address = ('', port)
    
    try:
        httpd = HTTPServer(server_address, DavidWebHandler)
        print(f"✓ 服务器启动成功！")
        print(f"✓ 访问地址: http://localhost:{port}")
        print(f"✓ 按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        # 延迟打开浏览器
        open_browser_delayed(f'http://localhost:{port}')
        
        httpd.serve_forever()
        
    except OSError as e:
        if e.errno == 10048:  # 端口被占用
            print(f"✗ 端口 {port} 被占用，尝试使用端口 8081...")
            try:
                port = 8081
                server_address = ('', port)
                httpd = HTTPServer(server_address, DavidWebHandler)
                print(f"✓ 服务器启动成功！")
                print(f"✓ 访问地址: http://localhost:{port}")
                print(f"✓ 按 Ctrl+C 停止服务器")
                print("=" * 60)
                
                open_browser_delayed(f'http://localhost:{port}')
                httpd.serve_forever()
            except Exception as e2:
                print(f"✗ 启动失败: {e2}")
                input("按任意键继续...")
        else:
            print(f"✗ 启动失败: {e}")
            input("按任意键继续...")
    except KeyboardInterrupt:
        print("\n✓ 服务器已停止")
        httpd.shutdown()
    except Exception as e:
        print(f"✗ 发生错误: {e}")
        input("按任意键继续...")

if __name__ == "__main__":
    main()

