# 大卫 - 智能长文本排版应用程序

David - Intelligent Long Text Formatting Application

一个专门用于处理长文本文件排版的智能应用程序，能够协调多个大语言模型共同完成排版任务，确保内容完整性和格式规范。

## 主要特性

- 📚 **长文本处理**: 支持32万字以上的长文本文件处理
- 🤖 **多LLM协调**: 智能协调多个大语言模型，确保处理效率和质量
- 📝 **智能排版**: 自动识别和应用排版规则，保持内容完整性
- ✅ **内容验证**: 多层次内容完整性验证，防止内容丢失或错位
- 🔄 **批量处理**: 支持批量处理多个文件
- 🎨 **多种格式**: 支持HTML、Word、纯文本等多种输出格式
- 🛡️ **安全可靠**: 内置内容验证和错误恢复机制

## 排版规则

### 标题层级
- **一级标题**: CHxx 章标题 → 加粗，字号 30
- **二级标题**: CHxx-Sxx 小节标题 → 加粗，字号 26

### 正文格式
- **字号**: 20
- **首行缩进**: 2 个字符
- **行距**: 1.5 倍

### 特殊标记
- **引用或重点**: 用【加框】表示
- **列表**: 用 "- " 或 "1. 2. 3." 表示，禁止用特殊符号

### 分页规则
- 每个大章节（CHxx）单独换页

## 安装说明

### 环境要求
- Python 3.8+
- 操作系统: Windows, macOS, Linux

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/your-repo/david.git
cd david
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置LLM API密钥
编辑 `config/settings.json` 文件，添加你的LLM API密钥：

```json
{
  "llm_configs": [
    {
      "name": "openai_gpt4",
      "api_key": "your-openai-api-key",
      "base_url": "https://api.openai.com/v1",
      "model": "gpt-4",
      "max_tokens": 4000,
      "temperature": 0.7,
      "timeout": 30,
      "priority": 1
    }
  ]
}
```

## 使用方法

### 交互模式
```bash
python main.py
```

### 批处理模式
```bash
python main.py file1.txt file2.txt file3.txt
```

### 命令行参数
- 无参数: 启动交互模式
- 文件路径: 批处理指定文件

## 配置说明

### 主要配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `chunk_size` | 4000 | 文本块大小（字符数） |
| `overlap_size` | 200 | 块间重叠大小（字符数） |
| `max_concurrent_tasks` | 3 | 最大并发任务数 |
| `retry_attempts` | 3 | 重试次数 |
| `min_similarity_threshold` | 0.95 | 最小相似度阈值 |
| `max_content_loss_threshold` | 0.05 | 最大内容丢失阈值 |

### LLM配置

支持多种LLM服务：
- OpenAI GPT-4
- Claude 3
- 其他兼容OpenAI API的服务

## 项目结构

```
david/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明
├── config/                # 配置文件目录
│   ├── settings.py        # 设置管理模块
│   └── settings.json      # 配置文件
├── core/                  # 核心模块
│   ├── text_processor.py  # 文本处理模块
│   ├── llm_coordinator.py # LLM协调器
│   ├── formatting_engine.py # 排版引擎
│   └── content_validator.py # 内容验证器
├── ui/                    # 用户界面
│   └── main_interface.py  # 主界面
├── logs/                  # 日志目录
├── output/                # 输出目录
└── temp/                  # 临时文件目录
```

## 处理流程

1. **文本读取**: 读取输入文件并进行预处理
2. **智能分块**: 将长文本分割成可处理的块
3. **LLM协调**: 使用多个LLM并行处理文本块
4. **排版应用**: 应用排版规则和格式
5. **内容验证**: 验证处理结果的完整性和正确性
6. **结果保存**: 保存格式化后的文本

## 故障排除

### 常见问题

1. **文件读取失败**
   - 检查文件路径是否正确
   - 确保文件编码为UTF-8
   - 检查文件权限

2. **LLM API调用失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 检查API配额和限制

3. **内存不足**
   - 减小 `chunk_size` 配置
   - 减少 `max_concurrent_tasks` 配置
   - 关闭其他占用内存的程序

4. **处理速度慢**
   - 增加 `max_concurrent_tasks` 配置
   - 使用更快的LLM服务
   - 检查网络延迟

### 日志查看

日志文件位置: `logs/david.log`

```bash
# 查看最新日志
tail -f logs/david.log

# 查看错误日志
grep "ERROR" logs/david.log
```

## 开发说明

### 添加新的LLM服务

1. 在 `core/llm_coordinator.py` 中添加新的API调用方法
2. 在 `config/settings.json` 中添加配置
3. 更新文档说明

### 自定义排版规则

1. 在 `core/formatting_engine.py` 中添加新规则
2. 更新规则优先级
3. 测试规则效果

### 扩展输出格式

1. 在 `core/formatting_engine.py` 中添加新格式方法
2. 更新设置配置
3. 更新用户界面

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

MIT License

## 联系方式

- 项目地址: https://github.com/your-repo/david
- 问题反馈: https://github.com/your-repo/david/issues
- 邮箱: your-email@example.com

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基本的长文本排版功能
- 多LLM协调处理
- 内容完整性验证
- 用户友好的交互界面

