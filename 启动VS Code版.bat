@echo off
chcp 65001 >nul
echo ============================================================
echo 大卫排版应用程序 - VS Code版
echo David Text Formatting Application - VS Code Version
echo ============================================================
echo.
echo 正在启动VS Code...
echo.

REM 检查Flutter是否安装
flutter --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flutter未安装，请先安装Flutter
    echo 运行: Flutter快速安装.bat
    pause
    exit /b 1
)

REM 检查VS Code是否安装
code --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ VS Code未安装，请先安装VS Code
    echo 下载地址: https://code.visualstudio.com/
    pause
    exit /b 1
)

echo ✓ Flutter环境检查通过
echo ✓ VS Code环境检查通过
echo.

REM 安装VS Code Flutter扩展
echo 正在安装VS Code Flutter扩展...
code --install-extension dart-code.dart-code
code --install-extension dart-code.flutter

echo.
echo 正在打开VS Code项目...
code .

echo.
echo ============================================================
echo 使用说明:
echo 1. 在VS Code中按F5运行应用
echo 2. 或使用Ctrl+Shift+P，输入"Flutter: Run Flutter App"
echo 3. 选择设备后开始运行
echo ============================================================
pause
