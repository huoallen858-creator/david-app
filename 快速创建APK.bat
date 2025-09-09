@echo off
chcp 65001 >nul
echo ============================================================
echo 快速创建Android APK
echo Quick Android APK Creation
echo ============================================================
echo.

REM 检查Flutter
C:\flutter\flutter\bin\flutter.bat --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flutter未安装
    pause
    exit /b 1
)

echo ✓ Flutter已安装

REM 检查Android SDK
if not exist "C:\Users\%USERNAME%\AppData\Local\Android\Sdk" (
    echo ❌ Android SDK未安装
    echo 请先运行: 安装Android开发环境.bat
    pause
    exit /b 1
)

echo ✓ Android SDK已找到

REM 设置环境变量
set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
set PATH=%PATH%;%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools

echo 正在创建APK...
cd david_app
C:\flutter\flutter\bin\flutter.bat build apk --release

if %errorlevel% equ 0 (
    echo.
    echo ✅ APK创建成功！
    echo 文件位置: david_app\build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo 安装到手机:
    echo 1. 将APK文件传输到手机
    echo 2. 在手机上允许安装未知来源应用
    echo 3. 点击APK文件安装
) else (
    echo ❌ APK创建失败
)

pause

