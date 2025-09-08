#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序启动脚本
David Text Formatting Application Launcher
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖包是否已安装"""
    try:
        import psutil
        import requests
        print("✓ 核心依赖包已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("✗ Python版本过低，需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    else:
        print(f"✓ Python版本: {sys.version.split()[0]}")
        return True

def create_directories():
    """创建必要的目录"""
    directories = ['logs', 'output', 'temp', 'config']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def main():
    """主函数"""
    print("=" * 60)
    print("大卫排版应用程序启动器")
    print("David Text Formatting Application Launcher")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查依赖包
    if not check_dependencies():
        sys.exit(1)
    
    # 创建必要目录
    create_directories()
    
    # 启动主程序
    print("\n启动主程序...")
    print("-" * 40)
    
    try:
        from main import main as main_app
        main_app()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

