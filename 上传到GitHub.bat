@echo off
chcp 65001 >nul
echo ============================================================
echo 上传到GitHub并构建APK
echo Upload to GitHub and Build APK
echo ============================================================
echo.

echo 正在初始化Git仓库...
git init
git add .
git commit -m "Initial commit: 大卫排版应用程序"

echo.
echo 请按以下步骤操作：
echo.
echo 1. 访问 https://github.com
echo 2. 点击右上角 "+" 号，选择 "New repository"
echo 3. 仓库名称输入: david-app
echo 4. 选择 "Public" 或 "Private"
echo 5. 点击 "Create repository"
echo.
echo 6. 复制仓库的HTTPS地址（类似：https://github.com/用户名/david-app.git）
echo 7. 在下面输入框中粘贴地址并按回车
echo.

set /p repo_url="请输入GitHub仓库地址: "https://github.com/huoallen858-creator/david-app.git


if "%repo_url%"=="" (
    echo ❌ 未输入仓库地址
    pause
    exit /b 1
)

echo.
echo 正在上传到GitHub...
git remote add origin %repo_url%
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ 上传成功！
    echo.
    echo 下一步：
    echo 1. 访问你的GitHub仓库页面
    echo 2. 点击 "Actions" 标签
    echo 3. 等待构建完成（约5-10分钟）
    echo 4. 点击构建任务，下载APK文件
    echo.
    echo 或者直接访问：
    echo %repo_url%/actions
) else (
    echo ❌ 上传失败，请检查网络连接和仓库地址
)

pause
