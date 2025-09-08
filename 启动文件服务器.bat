@echo off
chcp 65001 >nul
echo ============================================================
echo 文件传输服务器
echo File Transfer Server
echo ============================================================
echo.
echo 正在启动文件服务器...
echo.

python 文件服务器.py

echo.
echo 服务器已停止
pause

