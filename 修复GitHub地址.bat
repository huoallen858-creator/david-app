@echo off
chcp 65001 >nul
echo ============================================================
echo 修复GitHub地址
echo Fix GitHub Address
echo ============================================================
echo.

echo 你的GitHub地址可能有问题，让我重新设置...
echo.

REM 删除旧的远程仓库
& "C:\Program Files\Git\bin\git.exe" remote remove origin

echo 请确认你的GitHub用户名和仓库名：
echo.
echo 当前地址: https://github.com/huoallen858-creator/david-app.git
echo.
echo 如果地址正确，请按回车继续
echo 如果地址错误，请输入正确的地址
echo.

set /p new_url="请输入正确的GitHub地址 (或按回车使用当前地址): "

if "%new_url%"=="" (
    set new_url=https://github.com/huoallen858-creator/david-app.git
)

echo.
echo 正在设置新的远程仓库地址: %new_url%
& "C:\Program Files\Git\bin\git.exe" remote add origin %new_url%

echo.
echo 正在尝试上传...
& "C:\Program Files\Git\bin\git.exe" push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ 上传成功！
    echo 访问: %new_url%
    echo 点击 Actions 标签查看构建状态
) else (
    echo.
    echo ❌ 上传失败
    echo 请检查：
    echo 1. GitHub仓库是否存在
    echo 2. 用户名是否正确
    echo 3. 仓库名是否正确
    echo 4. 是否有推送权限
)

pause

