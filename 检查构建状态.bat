@echo off
chcp 65001 >nul
echo ============================================================
echo 检查GitHub Actions构建状态
echo Check GitHub Actions Build Status
echo ============================================================
echo.

echo ✅ 修复完成！现在可以检查构建状态了
echo.

echo 请访问以下链接检查构建状态：
echo.
echo 🔗 Actions页面: https://github.com/huoallen858-creator/david-app/actions
echo.

echo 如果看到 "Run workflow" 按钮：
echo 1. 点击 "Run workflow" 按钮
echo 2. 选择 main 分支
echo 3. 点击 "Run workflow" 确认
echo 4. 等待5-10分钟构建完成
echo 5. 在构建完成后下载APK文件
echo.

echo 如果构建失败，请检查错误信息并告诉我
echo.

echo 或者直接使用Web版本（推荐）：
echo 双击 大卫排版_Web版.html
echo.

echo 正在打开浏览器...
start https://github.com/huoallen858-creator/david-app/actions

pause
