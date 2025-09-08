# Flutter安装指南 - 大卫排版应用程序

## 🚀 为什么选择Flutter？

- ✅ **真正的原生应用** - 不是Web应用，性能更好
- ✅ **跨平台支持** - 一套代码，Android和iOS都能用
- ✅ **原生UI** - 使用系统原生组件，体验更好
- ✅ **离线使用** - 无需网络连接
- ✅ **文件管理** - 可以直接读取和保存文件
- ✅ **分享功能** - 内置分享到其他应用

## 📦 安装步骤

### 步骤1：下载Flutter SDK

1. **访问Flutter官网**：https://flutter.dev/docs/get-started/install/windows
2. **下载Flutter SDK**：选择Windows版本
3. **解压到合适位置**：建议解压到 `C:\flutter`

### 步骤2：配置环境变量

1. **打开系统属性**：
   - 右键"此电脑" → "属性"
   - 点击"高级系统设置"
   - 点击"环境变量"

2. **添加Flutter到PATH**：
   - 在"系统变量"中找到"Path"
   - 点击"编辑"
   - 点击"新建"
   - 添加：`C:\flutter\bin`
   - 点击"确定"保存

### 步骤3：安装Android Studio

1. **下载Android Studio**：https://developer.android.com/studio
2. **安装Android Studio**：按照默认设置安装
3. **启动Android Studio**：完成初始设置
4. **安装Android SDK**：在SDK Manager中安装最新版本

### 步骤4：验证安装

打开命令提示符，运行：
```bash
flutter doctor
```

如果看到绿色勾号，说明安装成功！

### 步骤5：创建Flutter应用

```bash
# 创建项目
flutter create david_formatter_app

# 进入项目目录
cd david_formatter_app

# 安装依赖
flutter pub get

# 构建APK
flutter build apk --release
```

## 📱 应用特点

- **原生性能** - 比Web应用快很多
- **文件选择** - 可以直接选择手机上的文件
- **离线使用** - 完全不需要网络
- **分享功能** - 排版完成后直接分享到微信、QQ等
- **专业排版** - 大16开尺寸，智能分页
- **符号清理** - 自动清理所有特殊符号

## 🔧 故障排除

### 常见问题：
1. **Flutter命令不识别** - 检查PATH环境变量
2. **Android SDK未找到** - 安装Android Studio
3. **构建失败** - 运行 `flutter doctor` 检查问题

### 解决方案：
- 重新配置环境变量
- 重启命令提示符
- 运行 `flutter doctor --android-licenses` 接受许可

---

**Flutter版本提供最佳的手机应用体验！** 🎉

