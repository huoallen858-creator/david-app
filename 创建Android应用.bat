@echo off
chcp 65001 >nul
echo ============================================================
echo 创建Android应用
echo Create Android App
echo ============================================================
echo.

echo 正在创建Android应用...

REM 进入Flutter项目目录
cd david_app

REM 检查Flutter
C:\flutter\flutter\bin\flutter.bat --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flutter未安装
    pause
    exit /b 1
)

echo ✓ Flutter已安装

REM 获取依赖
echo 正在获取依赖...
C:\flutter\flutter\bin\flutter.bat pub get

REM 创建APK
echo 正在创建APK...
C:\flutter\flutter\bin\flutter.bat build apk --debug

if %errorlevel% equ 0 (
    echo.
    echo ✅ Android应用创建成功！
    echo.
    echo APK文件位置:
    echo david_app\build\app\outputs\flutter-apk\app-debug.apk
    echo.
    echo 安装方法:
    echo 1. 将APK文件复制到手机
    echo 2. 在手机上允许安装未知来源应用
    echo 3. 点击APK文件安装
    echo.
    echo 或者使用ADB安装:
    echo adb install david_app\build\app\outputs\flutter-apk\app-debug.apk
) else (
    echo ❌ 创建失败，可能需要安装Android SDK
    echo 请运行: 安装Android开发环境.bat
)

pause
