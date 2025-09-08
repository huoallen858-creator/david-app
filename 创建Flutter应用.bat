@echo off
chcp 65001 >nul
echo ============================================================
echo 大卫排版应用程序 - Flutter版创建
echo David Text Formatting Application - Flutter Version
echo ============================================================
echo.

echo 正在创建Flutter应用...
echo.

echo 步骤1: 检查Flutter环境
flutter --version
if %errorlevel% neq 0 (
    echo 错误: Flutter未安装或未添加到PATH
    echo 请先安装Flutter: https://flutter.dev/docs/get-started/install
    pause
    exit /b 1
)

echo.
echo 步骤2: 创建Flutter项目
flutter create david_formatter_app
if %errorlevel% neq 0 (
    echo 错误: 创建Flutter项目失败
    pause
    exit /b 1
)

echo.
echo 步骤3: 复制应用文件
copy "lib\main.dart" "david_formatter_app\lib\main.dart"
copy "pubspec.yaml" "david_formatter_app\pubspec.yaml"
copy "android\app\src\main\AndroidManifest.xml" "david_formatter_app\android\app\src\main\AndroidManifest.xml"

echo.
echo 步骤4: 安装依赖
cd david_formatter_app
flutter pub get

echo.
echo 步骤5: 构建APK
flutter build apk --release

echo.
echo ✅ Flutter应用创建完成！
echo.
echo APK文件位置: david_formatter_app\build\app\outputs\flutter-apk\app-release.apk
echo.
echo 使用方法:
echo 1. 将APK文件传输到手机
echo 2. 在手机上安装APK
echo 3. 打开应用开始使用
echo.
pause
