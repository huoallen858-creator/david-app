@echo off
chcp 65001 >nul
echo ============================================================
echo 如何找到 "Run workflow" 按钮
echo How to Find "Run workflow" Button
echo ============================================================
echo.

echo 📍 "Run workflow" 按钮位置说明：
echo.

echo 1. 访问: https://github.com/huoallen858-creator/david-app/actions
echo.

echo 2. 在Actions页面中，找到 "Build APK" 工作流
echo    - 它应该在页面顶部或左侧列表中
echo.

echo 3. 点击 "Build APK" 工作流名称
echo    - 这会进入该工作流的详细页面
echo.

echo 4. 在详细页面中，查找：
echo    - 页面右上角有一个蓝色的 "Run workflow" 按钮
echo    - 或者在工作流名称旁边有一个下拉箭头，点击后选择 "Run workflow"
echo.

echo 5. 如果仍然找不到，可能是因为：
echo    - 工作流还没有被触发过
echo    - 需要先有至少一次运行记录
echo.

echo 🔧 解决方案：
echo 1. 先检查是否有任何构建任务在运行
echo 2. 如果没有，我们可以手动触发一次
echo 3. 或者直接使用Web版本（推荐）
echo.

echo 正在打开Actions页面...
start https://github.com/huoallen858-creator/david-app/actions

echo.
echo 请按照上述步骤查找按钮，如果还是找不到，请告诉我你看到了什么
pause
