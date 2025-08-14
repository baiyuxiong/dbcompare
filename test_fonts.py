#!/usr/bin/env python3
"""
字体显示测试脚本
用于验证不同系统下的字体显示效果
"""

import tkinter as tk
from tkinter import ttk
import platform

def test_fonts():
    """测试字体显示"""
    root = tk.Tk()
    root.title("字体显示测试")
    root.geometry("600x400")
    
    # 获取系统信息
    system = platform.system()
    print(f"当前系统: {system}")
    
    # 创建测试框架
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    title_label = ttk.Label(frame, text="字体显示测试", font=('TkDefaultFont', 16, 'bold'))
    title_label.pack(pady=(0, 20))
    
    # 系统信息
    system_label = ttk.Label(frame, text=f"系统: {system}", font=('TkDefaultFont', 12))
    system_label.pack(pady=5)
    
    # 测试不同字体
    test_texts = [
        ("默认字体", "TkDefaultFont"),
        ("固定字体", "TkFixedFont"),
        ("系统字体", "System"),
        ("中文测试", "中文显示测试"),
        ("English Test", "English Display Test"),
    ]
    
    for label_text, font_name in test_texts:
        if font_name in ["TkDefaultFont", "TkFixedFont", "System"]:
            test_label = ttk.Label(frame, text=f"{label_text}: {font_name}", font=(font_name, 10))
        else:
            test_label = ttk.Label(frame, text=f"{label_text}: {font_name}", font=('TkDefaultFont', 10))
        test_label.pack(pady=2)
    
    # 按钮测试
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=20)
    
    ttk.Button(btn_frame, text="测试按钮", font=('TkDefaultFont', 10)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Test Button", font=('TkDefaultFont', 10)).pack(side=tk.LEFT, padx=5)
    
    # 输入框测试
    entry_frame = ttk.Frame(frame)
    entry_frame.pack(pady=10)
    
    ttk.Label(entry_frame, text="输入测试:", font=('TkDefaultFont', 10)).pack(side=tk.LEFT)
    entry = ttk.Entry(entry_frame, font=('TkDefaultFont', 10))
    entry.pack(side=tk.LEFT, padx=5)
    entry.insert(0, "中文输入测试")
    
    root.mainloop()

if __name__ == "__main__":
    test_fonts() 