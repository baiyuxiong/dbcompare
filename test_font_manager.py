#!/usr/bin/env python3
"""
字体管理器测试脚本
用于验证智能字体管理器的工作效果
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.font_manager import FontManager
from ui.styles import StyleManager

def test_font_manager():
    """测试字体管理器"""
    root = tk.Tk()
    root.title("字体管理器测试")
    root.geometry("800x600")
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    title_label = ttk.Label(main_frame, text="智能字体管理器测试", font=('TkDefaultFont', 16, 'bold'))
    title_label.pack(pady=(0, 20))
    
    # 系统信息
    import platform
    system_info = f"系统: {platform.system()} {platform.release()}"
    system_label = ttk.Label(main_frame, text=system_info, font=('TkDefaultFont', 12))
    system_label.pack(pady=5)
    
    # 获取系统字体
    print("正在检测系统字体...")
    system_fonts = FontManager.get_system_fonts()
    print(f"检测到 {len(system_fonts)} 个系统字体")
    
    # 获取最优字体配置
    print("正在选择最优字体...")
    optimal_fonts = FontManager.get_optimal_fonts()
    
    # 显示字体信息
    font_info_frame = ttk.LabelFrame(main_frame, text="字体配置信息", padding="10")
    font_info_frame.pack(fill=tk.X, pady=10)
    
    for font_type, font_config in optimal_fonts.items():
        font_name, size, weight = font_config
        info_text = f"{font_type}: {font_name} {size}pt {weight}"
        info_label = ttk.Label(font_info_frame, text=info_text, font=('TkDefaultFont', 10))
        info_label.pack(anchor=tk.W, pady=2)
    
    # 测试中文显示
    test_frame = ttk.LabelFrame(main_frame, text="中文显示测试", padding="10")
    test_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # 使用不同字体显示中文
    test_texts = [
        ("标题字体", "title"),
        ("副标题字体", "subtitle"),
        ("标题字体", "heading"),
        ("正文字体", "body"),
        ("小字体", "small"),
        ("代码字体", "code")
    ]
    
    for label_text, font_type in test_texts:
        font_config = optimal_fonts[font_type]
        test_label = ttk.Label(test_frame, 
                              text=f"{label_text}: 中文测试 Chinese Test 123", 
                              font=font_config)
        test_label.pack(anchor=tk.W, pady=5)
    
    # 按钮测试
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=20)
    
    # 使用样式管理器
    try:
        colors, fonts = StyleManager.setup_styles()
        
        # 测试按钮
        test_btn1 = ttk.Button(btn_frame, text="测试按钮", style='Primary.TButton')
        test_btn1.pack(side=tk.LEFT, padx=5)
        
        test_btn2 = ttk.Button(btn_frame, text="Test Button", style='Success.TButton')
        test_btn2.pack(side=tk.LEFT, padx=5)
        
        print("样式管理器初始化成功")
    except Exception as e:
        print(f"样式管理器初始化失败: {e}")
    
    # 显示系统字体列表（前20个）
    font_list_frame = ttk.LabelFrame(main_frame, text="系统字体列表（前20个）", padding="10")
    font_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # 创建滚动文本框
    text_widget = tk.Text(font_list_frame, height=8, font=('TkFixedFont', 9))
    scrollbar = ttk.Scrollbar(font_list_frame, orient=tk.VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 插入字体列表
    for i, font in enumerate(system_fonts[:20]):
        text_widget.insert(tk.END, f"{i+1:2d}. {font}\n")
    
    text_widget.config(state=tk.DISABLED)
    
    root.mainloop()

if __name__ == "__main__":
    test_font_manager() 