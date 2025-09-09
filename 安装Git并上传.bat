@echo off
chcp 65001 >nul
echo ============================================================
echo 安装Git并上传到GitHub
echo Install Git and Upload to GitHub
echo ============================================================
echo.

echo 正在下载并安装Git...
echo Downloading and installing Git...

REM 下载Git
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile 'C:\temp\Git-installer.exe'}"

if exist "C:\temp\Git-installer.exe" (
    echo 正在安装Git...
    C:\temp\Git-installer.exe /SILENT /NORESTART
    echo Git安装完成
) else (
    echo 下载失败，请手动安装Git
    echo 访问: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo.
echo 正在设置Git环境变量...
set PATH=%PATH%;C:\Program Files\Git\bin

echo 正在初始化Git仓库...
git init
git config user.name "David App"
git config user.email "david@example.com"
git add .
git commit -m "Initial commit: 大卫排版应用程序"

echo.
echo 正在上传到GitHub...
git remote add origin https://github.com/huoallen858-creator/david-app.git
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ 上传成功！
    echo.
    echo 下一步：
    echo 1. 访问: https://github.com/huoallen858-creator/david-app
    echo 2. 点击 "Actions" 标签
    echo 3. 等待构建完成（约5-10分钟）
    echo 4. 点击构建任务，下载APK文件
    echo.
    echo 或者直接访问：
    echo https://github.com/huoallen858-creator/david-app/actions
) else (
    echo ❌ 上传失败，请检查网络连接
    echo 可能需要输入GitHub用户名和密码
)

pause

