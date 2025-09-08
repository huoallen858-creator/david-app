# 大卫排版应用程序 - Flutter版

## 🚀 为什么选择Flutter？

### **优势：**
- ✅ **真正的原生应用**：不是Web应用，性能更好
- ✅ **跨平台支持**：一套代码，Android和iOS都能用
- ✅ **原生UI**：使用系统原生组件，体验更好
- ✅ **离线使用**：无需网络连接
- ✅ **文件管理**：可以直接读取和保存文件
- ✅ **分享功能**：内置分享到其他应用

### **功能特点：**
- 📱 **原生界面**：Material Design风格
- 📝 **文本输入**：支持直接输入或选择文件
- 🔧 **智能排版**：自动识别标题、段落、列表
- 🧹 **符号清理**：清理所有特殊符号
- 📄 **专业输出**：大16开尺寸排版
- 📤 **一键分享**：直接分享到其他应用

## 📦 安装步骤

### **方法1：自动创建（推荐）**
1. 确保已安装Flutter
2. 双击 `创建Flutter应用.bat`
3. 等待自动创建和构建
4. 将生成的APK安装到手机

### **方法2：手动创建**
```bash
# 1. 创建Flutter项目
flutter create david_formatter_app

# 2. 复制文件
# 将 lib/main.dart 复制到 david_formatter_app/lib/
# 将 pubspec.yaml 复制到 david_formatter_app/
# 将 AndroidManifest.xml 复制到 david_formatter_app/android/app/src/main/

# 3. 安装依赖
cd david_formatter_app
flutter pub get

# 4. 构建APK
flutter build apk --release
```

## 📱 使用说明

1. **安装应用**：将APK文件安装到手机
2. **打开应用**：点击桌面图标启动
3. **输入文本**：在文本框中输入内容
4. **选择文件**：点击"选择文件"按钮选择文本文件
5. **开始排版**：点击"开始排版"按钮
6. **分享结果**：排版完成后自动分享HTML文件

## 🔧 技术特点

- **Flutter框架**：Google开发的跨平台UI框架
- **Material Design**：现代化的UI设计
- **文件处理**：支持读取和保存文件
- **分享功能**：内置分享到其他应用
- **响应式设计**：适配不同屏幕尺寸

## 📋 系统要求

- **开发环境**：Flutter SDK 3.0+
- **Android**：API 21+ (Android 5.0+)
- **iOS**：iOS 11.0+ (如果构建iOS版本)

---

**Flutter版本提供更好的用户体验和原生性能！** 🎉

