@echo off
chcp 65001 >nul
echo ============================================================
echo 安装Android开发环境
echo Install Android Development Environment
echo ============================================================
echo.

echo 正在下载Android Studio...
echo Downloading Android Studio...

REM 创建下载目录
if not exist "C:\Android" mkdir "C:\Android"

REM 下载Android Studio
echo 请手动下载Android Studio:
echo 1. 访问: https://developer.android.com/studio
echo 2. 下载Windows版本
echo 3. 安装到默认位置
echo.

echo 或者使用命令行下载:
powershell -Command "& {Invoke-WebRequest -Uri 'https://redirector.gvt1.com/edgedl/android/studio/install/2023.3.1.18/android-studio-2023.3.1.18-windows.exe' -OutFile 'C:\Android\android-studio.exe'}"

echo.
echo ============================================================
echo 安装步骤:
echo 1. 运行下载的android-studio.exe
echo 2. 选择"Standard"安装
echo 3. 安装完成后启动Android Studio
echo 4. 在欢迎界面选择"More Actions" -> "SDK Manager"
echo 5. 安装Android SDK (API 33或更高版本)
echo 6. 设置ANDROID_HOME环境变量
echo ============================================================
pause

