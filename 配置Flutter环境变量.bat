@echo off
chcp 65001 >nul
echo ============================================================
echo 配置Flutter环境变量
echo Configure Flutter Environment Variables
echo ============================================================
echo.

REM 检查Flutter是否已安装
if not exist "C:\flutter\flutter\bin\flutter.bat" (
    echo ❌ Flutter未正确安装
    echo 请先下载并解压Flutter SDK到 C:\flutter\flutter
    pause
    exit /b 1
)

echo ✓ Flutter SDK已找到: C:\flutter\flutter
echo.

REM 添加Flutter到用户PATH环境变量
echo 正在配置环境变量...
setx PATH "%PATH%;C:\flutter\flutter\bin" /M

if %errorlevel% equ 0 (
    echo ✓ 环境变量配置成功
) else (
    echo ⚠ 尝试以管理员权限配置环境变量...
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 配置完成！请按以下步骤操作：
echo 1. 关闭所有PowerShell和CMD窗口
echo 2. 重新打开一个新的PowerShell窗口
echo 3. 运行命令: flutter --version
echo ============================================================
pause
