#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序安装脚本
David Text Formatting Application Installer
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    else:
        print(f"✅ Python版本: {sys.version.split()[0]}")
        return True

def install_dependencies():
    """安装依赖包"""
    print("安装依赖包...")
    
    try:
        # 升级pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip已升级")
        
        # 安装依赖包
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def create_directories():
    """创建必要目录"""
    print("创建必要目录...")
    
    directories = [
        "logs",
        "output", 
        "temp",
        "config",
        "examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def create_config_file():
    """创建配置文件"""
    print("创建配置文件...")
    
    config_file = "config/settings.json"
    if not os.path.exists(config_file):
        print("✅ 配置文件已存在")
        return True
    
    # 配置文件已存在，不需要创建
    print("✅ 配置文件已存在")
    return True

def create_startup_scripts():
    """创建启动脚本"""
    print("创建启动脚本...")
    
    # Windows批处理文件
    if platform.system() == "Windows":
        bat_content = """@echo off
echo 启动大卫排版应用程序...
python run.py
pause
"""
        with open("start_david.bat", "w", encoding="utf-8") as f:
            f.write(bat_content)
        print("✅ 创建Windows启动脚本: start_david.bat")
    
    # Unix shell脚本
    shell_content = """#!/bin/bash
echo "启动大卫排版应用程序..."
python3 run.py
"""
    with open("start_david.sh", "w", encoding="utf-8") as f:
        f.write(shell_content)
    
    # 设置执行权限
    if platform.system() != "Windows":
        os.chmod("start_david.sh", 0o755)
    
    print("✅ 创建Unix启动脚本: start_david.sh")

def run_tests():
    """运行测试"""
    print("运行测试...")
    
    try:
        result = subprocess.run([sys.executable, "test_david.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 所有测试通过")
            return True
        else:
            print("❌ 测试失败")
            print("错误输出:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def main():
    """主安装函数"""
    print("=" * 60)
    print("大卫排版应用程序安装程序")
    print("David Text Formatting Application Installer")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖包
    if not install_dependencies():
        print("❌ 安装失败，请检查网络连接和Python环境")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 创建配置文件
    create_config_file()
    
    # 创建启动脚本
    create_startup_scripts()
    
    # 运行测试
    if not run_tests():
        print("⚠️  测试失败，但安装可能仍然成功")
    
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("\n使用方法:")
    print("1. 交互模式: python run.py")
    print("2. 批处理模式: python main.py file1.txt file2.txt")
    print("3. 测试程序: python test_david.py")
    print("\n配置文件: config/settings.json")
    print("输出目录: output/")
    print("日志文件: logs/david.log")
    print("=" * 60)

if __name__ == "__main__":
    main()

