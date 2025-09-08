@echo off
chcp 65001 >nul
cd /d "C:\Users\rudyh\Desktop\新建cursor文件夹"
echo ============================================================
echo 大卫排版应用程序 - 桌面版启动中...
echo ============================================================
python "大卫排版_桌面版.py"
if errorlevel 1 (
    echo.
    echo 启动失败，请检查Python是否正确安装
    pause
)
