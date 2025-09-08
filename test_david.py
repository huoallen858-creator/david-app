#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大卫排版应用程序测试脚本
David Text Formatting Application Test Script
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_text_processor():
    """测试文本处理模块"""
    print("测试文本处理模块...")
    
    try:
        from core.text_processor import TextProcessor
        from config.settings import Settings
        
        settings = Settings()
        processor = TextProcessor(settings)
        
        # 创建测试文本
        test_text = """CH1 测试章节
        
这是测试内容，包含多个段落。

CH1-S1 测试小节

- 列表项1
- 列表项2

【重要内容】这是一个重要的引用。

CH2 另一个章节

更多测试内容..."""
        
        # 测试文本分析
        analysis = processor.analyze_text_structure(test_text)
        print(f"✓ 文本分析完成: {analysis['chapters']} 个章节, {analysis['sections']} 个小节")
        
        # 测试文本分块
        chunks = processor._chunk_text(test_text)
        print(f"✓ 文本分块完成: {len(chunks)} 个块")
        
        return True
        
    except Exception as e:
        print(f"✗ 文本处理模块测试失败: {e}")
        return False

def test_formatting_engine():
    """测试排版引擎模块"""
    print("测试排版引擎模块...")
    
    try:
        from core.formatting_engine import FormattingEngine
        from config.settings import Settings
        
        settings = Settings()
        engine = FormattingEngine(settings)
        
        # 测试文本
        test_chunks = [
            "**CH1 测试章节**\n\n这是测试内容。",
            "**CH1-S1 测试小节**\n\n- 列表项1\n- 列表项2"
        ]
        
        # 测试格式化
        formatted_text = engine.format_text(test_chunks)
        print(f"✓ 文本格式化完成: {len(formatted_text)} 字符")
        
        # 测试验证
        validation = engine.validate_formatting(formatted_text)
        print(f"✓ 格式化验证完成: {validation}")
        
        return True
        
    except Exception as e:
        print(f"✗ 排版引擎模块测试失败: {e}")
        return False

def test_content_validator():
    """测试内容验证器模块"""
    print("测试内容验证器模块...")
    
    try:
        from core.content_validator import ContentValidator
        from config.settings import Settings
        
        settings = Settings()
        validator = ContentValidator(settings)
        
        # 测试内容
        original_chunks = ["CH1 测试章节\n\n这是测试内容。"]
        processed_chunks = ["CH1 测试章节\n\n这是测试内容。"]
        formatted_text = "<h1>CH1 测试章节</h1><p>这是测试内容。</p>"
        
        # 测试验证
        result = validator.validate_content(original_chunks, processed_chunks, formatted_text)
        print(f"✓ 内容验证完成: 有效性={result.is_valid}, 相似度={result.similarity_score:.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ 内容验证器模块测试失败: {e}")
        return False

def test_settings():
    """测试设置管理模块"""
    print("测试设置管理模块...")
    
    try:
        from config.settings import Settings
        
        # 创建临时设置文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"chunk_size": 2000, "test_setting": "test_value"}')
            temp_config = f.name
        
        try:
            settings = Settings(temp_config)
            
            # 测试设置获取
            chunk_size = settings.get('chunk_size')
            test_setting = settings.get('test_setting')
            
            print(f"✓ 设置管理测试完成: chunk_size={chunk_size}, test_setting={test_setting}")
            
            # 测试设置验证
            errors = settings.validate_settings()
            print(f"✓ 设置验证完成: {len(errors)} 个错误")
            
            return True
            
        finally:
            # 清理临时文件
            os.unlink(temp_config)
        
    except Exception as e:
        print(f"✗ 设置管理模块测试失败: {e}")
        return False

def test_full_workflow():
    """测试完整工作流程"""
    print("测试完整工作流程...")
    
    try:
        from main import DavidApp
        
        # 创建临时测试文件
        test_content = """CH1 测试章节

这是测试内容，包含多个段落。

CH1-S1 测试小节

- 列表项1
- 列表项2

【重要内容】这是一个重要的引用。

CH2 另一个章节

更多测试内容..."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # 创建应用程序实例
            app = DavidApp()
            
            # 测试处理流程（不实际调用LLM）
            print("✓ 应用程序初始化完成")
            
            # 测试文本处理
            text_processor = app.text_processor
            chunks = text_processor.load_and_chunk_text(temp_file)
            print(f"✓ 文本处理完成: {len(chunks)} 个块")
            
            # 测试排版引擎
            formatting_engine = app.formatting_engine
            formatted_text = formatting_engine.format_text(chunks)
            print(f"✓ 排版处理完成: {len(formatted_text)} 字符")
            
            return True
            
        finally:
            # 清理临时文件
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"✗ 完整工作流程测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("大卫排版应用程序测试")
    print("David Text Formatting Application Test")
    print("=" * 60)
    
    tests = [
        ("设置管理模块", test_settings),
        ("文本处理模块", test_text_processor),
        ("排版引擎模块", test_formatting_engine),
        ("内容验证器模块", test_content_validator),
        ("完整工作流程", test_full_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✓ {test_name} 测试通过")
        else:
            print(f"✗ {test_name} 测试失败")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用程序可以正常使用。")
        return True
    else:
        print("❌ 部分测试失败，请检查错误信息。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

