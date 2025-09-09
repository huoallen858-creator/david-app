@echo off
chcp 65001 >nul
echo ============================================================
echo 大卫排版应用程序 - 构建Android APK
echo David Text Formatting Application - Build Android APK
echo ============================================================
echo.
echo 正在构建Android APK...
echo.

echo 步骤1: 清理之前的构建...
buildozer android clean

echo.
echo 步骤2: 开始构建APK...
buildozer android debug

echo.
echo 构建完成！
echo APK文件位置: bin/davidformatter-1.0-debug.apk
echo.
echo 请按任意键退出...
pause >nul


