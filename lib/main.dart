import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';
import 'dart:io';
import 'dart:convert';

void main() {
  runApp(const DavidFormatterApp());
}

class DavidFormatterApp extends StatelessWidget {
  const DavidFormatterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '大卫排版应用程序',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _textController = TextEditingController();
  bool _isProcessing = false;
  String _statusMessage = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('大卫排版应用程序'),
        backgroundColor: Colors.blue[600],
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Colors.blue[400]!, Colors.purple[600]!],
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                Card(
                  elevation: 8,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '输入要排版的文本内容：',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: Colors.grey[800],
                          ),
                        ),
                        const SizedBox(height: 12),
                        TextField(
                          controller: _textController,
                          maxLines: 8,
                          decoration: InputDecoration(
                            hintText: '在此输入要排版的文本内容...',
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide: BorderSide(color: Colors.grey[300]!),
                            ),
                            focusedBorder: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide: BorderSide(color: Colors.blue[400]!),
                            ),
                            contentPadding: const EdgeInsets.all(16),
                          ),
                        ),
                        const SizedBox(height: 20),
                        Row(
                          children: [
                            Expanded(
                              child: ElevatedButton.icon(
                                onPressed: _isProcessing ? null : _processText,
                                icon: _isProcessing
                                    ? const SizedBox(
                                        width: 20,
                                        height: 20,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                        ),
                                      )
                                    : const Icon(Icons.format_align_left),
                                label: Text(_isProcessing ? '处理中...' : '开始排版'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.blue[600],
                                  foregroundColor: Colors.white,
                                  padding: const EdgeInsets.symmetric(vertical: 16),
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(width: 12),
                            ElevatedButton.icon(
                              onPressed: _isProcessing ? null : _pickFile,
                              icon: const Icon(Icons.folder_open),
                              label: const Text('选择文件'),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.green[600],
                                foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(vertical: 16),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                ),
                              ),
                            ),
                          ],
                        ),
                        if (_statusMessage.isNotEmpty) ...[
                          const SizedBox(height: 16),
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: _statusMessage.contains('成功') || _statusMessage.contains('完成')
                                  ? Colors.green[50]
                                  : Colors.red[50],
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                color: _statusMessage.contains('成功') || _statusMessage.contains('完成')
                                    ? Colors.green[200]!
                                    : Colors.red[200]!,
                              ),
                            ),
                            child: Text(
                              _statusMessage,
                              style: TextStyle(
                                color: _statusMessage.contains('成功') || _statusMessage.contains('完成')
                                    ? Colors.green[800]
                                    : Colors.red[800],
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                Card(
                  elevation: 8,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '功能特点',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.grey[800],
                          ),
                        ),
                        const SizedBox(height: 12),
                        ..._buildFeatureList(),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  List<Widget> _buildFeatureList() {
    final features = [
      '自动识别标题格式',
      '清理特殊符号',
      '智能分页',
      '专业排版输出',
      '大16开尺寸 (210mm × 285mm)',
    ];

    return features.map((feature) => Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(
            Icons.check_circle,
            color: Colors.green[600],
            size: 20,
          ),
          const SizedBox(width: 8),
          Text(
            feature,
            style: TextStyle(
              color: Colors.grey[700],
              fontSize: 14,
            ),
          ),
        ],
      ),
    )).toList();
  }

  Future<void> _processText() async {
    if (_textController.text.trim().isEmpty) {
      setState(() {
        _statusMessage = '请输入文本内容';
      });
      return;
    }

    setState(() {
      _isProcessing = true;
      _statusMessage = '正在处理文本...';
    });

    try {
      final processedText = _processTextContent(_textController.text);
      final htmlResult = _createHTML(processedText);
      
      // 保存文件
      final directory = await getApplicationDocumentsDirectory();
      final timestamp = DateTime.now().millisecondsSinceEpoch;
      final filename = '大卫排版结果_$timestamp.html';
      final file = File('${directory.path}/$filename');
      
      await file.writeAsString(htmlResult, encoding: utf8);
      
      // 分享文件
      await Share.shareXFiles([XFile(file.path)], text: '大卫排版结果');
      
      setState(() {
        _statusMessage = '排版完成！文件已保存并分享';
      });
    } catch (e) {
      setState(() {
        _statusMessage = '处理失败: $e';
      });
    } finally {
      setState(() {
        _isProcessing = false;
      });
    }
  }

  Future<void> _pickFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['txt', 'md'],
      );

      if (result != null) {
        final file = File(result.files.single.path!);
        final content = await file.readAsString(encoding: utf8);
        _textController.text = content;
        setState(() {
          _statusMessage = '文件读取成功';
        });
      }
    } catch (e) {
      setState(() {
        _statusMessage = '文件读取失败: $e';
      });
    }
  }

  String _processTextContent(String text) {
    // 清理Markdown符号和特殊符号
    text = text.replaceAll(RegExp(r'\*\*([^*]+)\*\*'), r'$1');
    text = text.replaceAll(RegExp(r'\*([^*]+)\*'), r'$1');
    text = text.replaceAll(RegExp(r'^#+\s*', multiLine: true), '');
    text = text.replaceAll(RegExp(r'#+'), '');
    text = text.replaceAll(RegExp(r'[□■▪▫▬▭▮▯]'), '');
    text = text.replaceAll(RegExp(r'[•·◦‣⁃]'), '');
    
    // 多次清理
    for (int i = 0; i < 10; i++) {
      text = text.replaceAll(RegExp(r'[▪▫▬▭▮▯]'), '');
    }
    
    // 处理段落
    final paragraphs = text.split('\n\n');
    final processed = <String>[];
    
    for (final paragraph in paragraphs) {
      final trimmed = paragraph.trim();
      if (trimmed.isEmpty) continue;
      
      if (RegExp(r'^第[一二三四五六七八九十\d]+天：').hasMatch(trimmed)) {
        processed.add('<h1>$trimmed</h1>');
      } else if (RegExp(r'^分钟 \d+-\d+：').hasMatch(trimmed)) {
        processed.add('<h2>$trimmed</h2>');
      } else if (RegExp(r'^深度技术解析：').hasMatch(trimmed)) {
        processed.add('<h2>$trimmed</h2>');
      } else if (trimmed.startsWith('- ')) {
        processed.add('<li>${trimmed.substring(2)}</li>');
      } else if (RegExp(r'^\d+\.').hasMatch(trimmed)) {
        processed.add('<li>$trimmed</li>');
      } else {
        processed.add('<p class="normal-text">$trimmed</p>');
      }
    }
    
    return processed.join('\n\n');
  }

  String _createHTML(String content) {
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>大卫排版结果</title>
    <style>
        @page { size: 210mm 285mm; margin: 25mm; }
        body { font-family: "Microsoft YaHei", serif; line-height: 1.6; margin: 0; padding: 20px; }
        .book-container { max-width: 21cm; margin: 0 auto; background: white; padding: 25mm; }
        h1 { font-size: 20pt; font-weight: bold; color: #2c3e50; margin: 20pt 0 15pt 0; }
        h2 { font-size: 16pt; font-weight: bold; color: #34495e; margin: 15pt 0 10pt 0; }
        p { font-size: 12pt; margin: 8pt 0; text-indent: 2em; }
        p.normal-text { text-indent: 2em !important; }
        li { font-size: 12pt; margin: 4pt 0; list-style: none; }
    </style>
</head>
<body>
    <div class="book-container">
        $content
    </div>
</body>
</html>''';
  }
}

