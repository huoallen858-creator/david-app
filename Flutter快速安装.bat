@echo off
chcp 65001 >nul
echo ============================================================
echo Flutter快速安装指南
echo Flutter Quick Installation Guide
echo ============================================================
echo.

echo 步骤1: 检查Flutter是否已安装
flutter --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ Flutter未安装！
    echo.
    echo 请按照以下步骤安装Flutter：
    echo.
    echo 1. 访问: https://flutter.dev/docs/get-started/install/windows
    echo 2. 下载Flutter SDK for Windows
    echo 3. 解压到 C:\flutter
    echo 4. 添加 C:\flutter\bin 到系统PATH环境变量
    echo 5. 重启命令提示符
    echo.
    echo 详细步骤请查看: Flutter安装指南.md
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Flutter已安装！
echo.

echo 步骤2: 检查Flutter环境
flutter doctor
echo.

echo 步骤3: 创建Flutter应用
if not exist "david_formatter_app" (
    echo 正在创建Flutter项目...
    flutter create david_formatter_app
    if %errorlevel% neq 0 (
        echo ❌ 创建项目失败！
        pause
        exit /b 1
    )
    echo ✅ 项目创建成功！
) else (
    echo ✅ 项目已存在！
)

echo.
echo 步骤4: 复制应用文件
if exist "lib\main.dart" (
    copy "lib\main.dart" "david_formatter_app\lib\main.dart" >nul
    echo ✅ 主程序文件已复制
)

if exist "pubspec.yaml" (
    copy "pubspec.yaml" "david_formatter_app\pubspec.yaml" >nul
    echo ✅ 配置文件已复制
)

if exist "android\app\src\main\AndroidManifest.xml" (
    if not exist "david_formatter_app\android\app\src\main\" mkdir "david_formatter_app\android\app\src\main\"
    copy "android\app\src\main\AndroidManifest.xml" "david_formatter_app\android\app\src\main\AndroidManifest.xml" >nul
    echo ✅ Android配置已复制
)

echo.
echo 步骤5: 安装依赖
cd david_formatter_app
flutter pub get
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败！
    pause
    exit /b 1
)
echo ✅ 依赖安装成功！

echo.
echo 步骤6: 构建APK
echo 正在构建Android APK，请稍候...
flutter build apk --release
if %errorlevel% neq 0 (
    echo ❌ APK构建失败！
    echo 请检查Flutter环境配置
    pause
    exit /b 1
)

echo.
echo ✅ Flutter应用创建完成！
echo.
echo 📱 APK文件位置: build\app\outputs\flutter-apk\app-release.apk
echo.
echo 使用方法:
echo 1. 将APK文件传输到手机
echo 2. 在手机上安装APK
echo 3. 打开应用开始使用
echo.
echo 按任意键退出...
pause >nul


