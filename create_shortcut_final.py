#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建桌面快捷方式 - 最终版
"""

import os
import sys

def create_shortcut():
    try:
        import win32com.client
        
        # 创建快捷方式
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "大卫排版工具.lnk")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        
        # 设置目标为批处理文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        batch_file = os.path.join(current_dir, "启动大卫排版.bat")
        
        shortcut.TargetPath = batch_file
        shortcut.WorkingDirectory = current_dir
        shortcut.Description = "大卫排版应用程序 - 交互式版本"
        shortcut.IconLocation = "python.exe,0"
        
        shortcut.Save()
        
        print(f"✓ 桌面快捷方式创建成功: {shortcut_path}")
        print(f"✓ 目标文件: {batch_file}")
        return True
        
    except ImportError:
        print("✗ 需要安装 pywin32: pip install pywin32")
        return False
    except Exception as e:
        print(f"✗ 创建快捷方式失败: {e}")
        return False

if __name__ == "__main__":
    create_shortcut()


