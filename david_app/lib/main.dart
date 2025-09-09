import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

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
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
        fontFamily: 'Microsoft YaHei',
      ),
      home: const DavidHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class DavidHomePage extends StatefulWidget {
  const DavidHomePage({super.key});

  @override
  State<DavidHomePage> createState() => _DavidHomePageState();
}

class _DavidHomePageState extends State<DavidHomePage> with TickerProviderStateMixin {
  final TextEditingController _textController = TextEditingController();
  String _formattedText = '';
  bool _isProcessing = false;
  int _currentTabIndex = 0;
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _tabController.addListener(() {
      setState(() {
        _currentTabIndex = _tabController.index;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    // 强制竖屏
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);

    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        backgroundColor: Colors.deepPurple[600],
        foregroundColor: Colors.white,
        elevation: 0,
        title: const Text(
          '📚 大卫排版',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.white,
          indicatorWeight: 3,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.white70,
          tabs: const [
            Tab(
              icon: Icon(Icons.edit, size: 20),
              text: '输入文本',
            ),
            Tab(
              icon: Icon(Icons.preview, size: 20),
              text: '预览结果',
            ),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildInputTab(),
          _buildPreviewTab(),
        ],
      ),
      floatingActionButton: _currentTabIndex == 0
          ? FloatingActionButton.extended(
              onPressed: _isProcessing ? null : _formatText,
              backgroundColor: Colors.deepPurple[600],
              foregroundColor: Colors.white,
              icon: _isProcessing
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : const Icon(Icons.rocket_launch),
              label: Text(_isProcessing ? '处理中...' : '开始排版'),
            )
          : null,
    );
  }

  Widget _buildInputTab() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          // 功能说明卡片
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.deepPurple[50]!, Colors.purple[50]!],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.deepPurple[200]!),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.deepPurple[600], size: 20),
                    const SizedBox(width: 8),
                    Text(
                      '支持格式',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.deepPurple[700],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                const Text(
                  '• CH1 章标题 → 自动加粗分页\n• CH1-S1 小节标题 → 自动加粗\n• 【重要内容】 → 自动加框\n• 普通段落 → 自动首行缩进',
                  style: TextStyle(fontSize: 14, height: 1.5),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          // 文本输入区域
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.1),
                    spreadRadius: 1,
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '输入要排版的文本：',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.grey[700],
                      ),
                    ),
                    const SizedBox(height: 12),
                    Expanded(
                      child: TextField(
                        controller: _textController,
                        maxLines: null,
                        expands: true,
                        textAlignVertical: TextAlignVertical.top,
                        style: const TextStyle(fontSize: 16, height: 1.5),
                        decoration: InputDecoration(
                          hintText: '在此输入要排版的文本内容...\n\n例如：\nCH1 第一章标题\n这是第一章的内容...\n\nCH1-S1 第一个小节\n这是小节内容...\n\n【重要观点】这是重要内容',
                          hintStyle: TextStyle(
                            color: Colors.grey[400],
                            fontSize: 14,
                            height: 1.5,
                          ),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                            borderSide: BorderSide(color: Colors.grey[300]!),
                          ),
                          enabledBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                            borderSide: BorderSide(color: Colors.grey[300]!),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                            borderSide: BorderSide(color: Colors.deepPurple[400]!, width: 2),
                          ),
                          contentPadding: const EdgeInsets.all(16),
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
    );
  }

  Widget _buildPreviewTab() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          // 预览说明
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.blue[50],
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.blue[200]!),
            ),
            child: Row(
              children: [
                Icon(Icons.preview, color: Colors.blue[600], size: 18),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _formattedText.isEmpty 
                        ? '请先在"输入文本"页面输入内容并点击排版'
                        : '排版完成！以下是预览效果',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.blue[700],
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          // 预览内容
          Expanded(
            child: Container(
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.1),
                    spreadRadius: 1,
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: _formattedText.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.text_fields,
                            size: 64,
                            color: Colors.grey[300],
                          ),
                          const SizedBox(height: 16),
                          Text(
                            '暂无预览内容',
                            style: TextStyle(
                              fontSize: 16,
                              color: Colors.grey[500],
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            '请先输入文本并排版',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey[400],
                            ),
                          ),
                        ],
                      ),
                    )
                  : SingleChildScrollView(
                      padding: const EdgeInsets.all(16),
                      child: Text(
                        _formattedText,
                        style: const TextStyle(
                          fontSize: 16,
                          height: 1.8,
                          letterSpacing: 0.5,
                        ),
                      ),
                    ),
            ),
          ),
        ],
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