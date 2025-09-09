#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的文件服务器，用于传输文件到手机
"""

import http.server
import socketserver
import webbrowser
import socket
import os

def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class FileHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    PORT = 8080
    IP = get_local_ip()
    
    print("=" * 60)
    print("文件传输服务器")
    print("=" * 60)
    print(f"服务器地址: http://{IP}:{PORT}")
    print(f"手机访问: http://{IP}:{PORT}")
    print()
    print("可用文件:")
    print("- david_mobile_app.html (手机版应用)")
    print("- manifest.json (应用配置)")
    print("- sw.js (离线缓存)")
    print()
    print("在手机浏览器中访问上述地址即可下载文件")
    print("按 Ctrl+C 停止服务器")
    print()
    
    # 启动服务器
    with socketserver.TCPServer(("", PORT), FileHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    main()


