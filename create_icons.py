#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建应用图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    # 创建图像
    img = Image.new('RGBA', (size, size), (102, 126, 234, 255))
    draw = ImageDraw.Draw(img)
    
    # 绘制圆形背景
    draw.ellipse([10, 10, size-10, size-10], fill=(118, 75, 162, 255))
    
    # 绘制文字
    try:
        font_size = size // 4
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "大卫"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # 保存图标
    img.save(filename, 'PNG')
    print(f"✓ 创建图标: {filename}")

def main():
    print("正在创建应用图标...")
    
    # 创建不同尺寸的图标
    create_icon(192, 'icon-192.png')
    create_icon(512, 'icon-512.png')
    
    print("✓ 图标创建完成！")

if __name__ == "__main__":
    main()


