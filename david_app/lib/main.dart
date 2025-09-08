import 'package:flutter/material.dart';

void main() {
  runApp(const DavidApp());
}

class DavidApp extends StatelessWidget {
  const DavidApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '大卫排版应用程序',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
        fontFamily: 'Microsoft YaHei',
      ),
      home: const DavidHomePage(),
    );
  }
}

class DavidHomePage extends StatefulWidget {
  const DavidHomePage({super.key});

  @override
  State<DavidHomePage> createState() => _DavidHomePageState();
}

class _DavidHomePageState extends State<DavidHomePage> {
  final TextEditingController _textController = TextEditingController();
  String _formattedText = '';
  bool _isProcessing = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('📚 大卫排版应用程序'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // 输入区域
            Expanded(
              flex: 1,
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '输入要排版的文本内容：',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Expanded(
                        child: TextField(
                          controller: _textController,
                          maxLines: null,
                          expands: true,
                          decoration: const InputDecoration(
                            hintText: '在此输入要排版的文本内容...\n\n支持格式：\n• CH1 章标题\n• CH1-S1 小节标题\n• 【重要内容】\n• 普通段落会自动首行缩进',
                            border: OutlineInputBorder(),
                            alignLabelWithHint: true,
                          ),
                          textAlignVertical: TextAlignVertical.top,
                        ),
                      ),
                      const SizedBox(height: 16),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: _isProcessing ? null : _formatText,
                          icon: _isProcessing 
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              )
                            : const Icon(Icons.rocket_launch),
                          label: Text(_isProcessing ? '处理中...' : '🚀 开始排版'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            // 输出区域
            Expanded(
              flex: 1,
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '排版结果预览：',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Expanded(
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey.shade300),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: _formattedText.isEmpty
                              ? const Center(
                                  child: Text(
                                    '输入文本后点击"开始排版"按钮查看结果',
                                    style: TextStyle(
                                      color: Colors.grey,
                                      fontSize: 16,
                                    ),
                                  ),
                                )
                              : SingleChildScrollView(
                                  child: Text(
                                    _formattedText,
                                    style: const TextStyle(
                                      fontSize: 14,
                                      height: 1.6,
                                    ),
                                  ),
                                ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _formatText() {
    if (_textController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('请输入要排版的文本内容！')),
      );
      return;
    }

    setState(() {
      _isProcessing = true;
    });

    // 模拟处理延迟
    Future.delayed(const Duration(milliseconds: 500), () {
      final formattedText = _processText(_textController.text);
      setState(() {
        _formattedText = formattedText;
        _isProcessing = false;
      });
    });
  }

  String _processText(String text) {
    // 清理Markdown符号和特殊符号
    text = text.replaceAll(RegExp(r'\*\*([^*]+)\*\*'), r'$1');  // 移除 **text**
    text = text.replaceAll(RegExp(r'\*([^*]+)\*'), r'$1');      // 移除 *text*
    text = text.replaceAll(RegExp(r'^#+\s*', multiLine: true), '');  // 移除行首的 # 符号
    text = text.replaceAll(RegExp(r'#+'), '');                 // 移除所有的 # 符号
    text = text.replaceAll(RegExp(r'[□■▪▫▬▭▮▯•·◦‣⁃]'), '');    // 移除各种符号
    
    // 按段落分割
    final paragraphs = text.split(RegExp(r'\n\s*\n'));
    String result = '';
    int lineCount = 0;
    const int maxLinesPerPage = 35; // 28.5cm约35行
    
    for (final paragraph in paragraphs) {
      final trimmedParagraph = paragraph.trim();
      if (trimmedParagraph.isEmpty) continue;
      
      // 检查是否是标题
      if (RegExp(r'^CH\d+[-\s]').hasMatch(trimmedParagraph)) {
        // 一级标题
        if (lineCount > 0) {
          result += '\n\n📄 分页 - 28.5cm 📄\n\n';
        }
        result += '【章标题】$trimmedParagraph\n\n';
        lineCount += 3;
      } else if (RegExp(r'^CH\d+-S\d+').hasMatch(trimmedParagraph)) {
        // 二级标题
        if (lineCount > maxLinesPerPage - 5) {
          result += '\n\n📄 分页 - 28.5cm 📄\n\n';
          lineCount = 0;
        }
        result += '【小节标题】$trimmedParagraph\n\n';
        lineCount += 2;
      } else if (RegExp(r'^【.*】$').hasMatch(trimmedParagraph)) {
        // 引用内容
        if (lineCount > maxLinesPerPage - 3) {
          result += '\n\n📄 分页 - 28.5cm 📄\n\n';
          lineCount = 0;
        }
        result += '【重要】$trimmedParagraph\n\n';
        lineCount += 2;
      } else {
        // 普通段落
        if (lineCount > maxLinesPerPage - 2) {
          result += '\n\n📄 分页 - 28.5cm 📄\n\n';
          lineCount = 0;
        }
        result += '    $trimmedParagraph\n\n'; // 首行缩进
        lineCount += (trimmedParagraph.length / 50).ceil(); // 估算行数
      }
    }
    
    return result;
  }

  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }
}