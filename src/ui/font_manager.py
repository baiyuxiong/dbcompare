"""
智能字体管理器
自动检测系统支持的字体并选择最适合的字体来显示中文
"""

import tkinter as tk
from tkinter import font
import platform
import subprocess
import os
from typing import Dict, List, Tuple

class FontManager:
    """字体管理器"""
    
    # 字体优先级列表 - 按优先级排序
    FONT_PRIORITIES = {
        'Windows': [
            'Microsoft YaHei UI',
            'Microsoft YaHei',
            'SimHei',
            'SimSun',
            'Arial Unicode MS',
            'Arial'
        ],
        'Linux': [
            'WenQuanYi Micro Hei',
            'WenQuanYi Zen Hei',
            'Noto Sans CJK SC',
            'Noto Sans CJK TC',
            'Noto Sans CJK JP',
            'Droid Sans Fallback',
            'DejaVu Sans',
            'Liberation Sans',
            'Ubuntu',
            'Arial'
        ],
        'Darwin': [  # macOS
            'PingFang SC',
            'PingFang TC',
            'Hiragino Sans GB',
            'STHeiti',
            'Arial Unicode MS',
            'Arial'
        ]
    }
    
    # 等宽字体优先级列表
    MONO_FONT_PRIORITIES = {
        'Windows': [
            'Consolas',
            'Courier New',
            'Monaco'
        ],
        'Linux': [
            'DejaVu Sans Mono',
            'Liberation Mono',
            'Ubuntu Mono',
            'Monaco'
        ],
        'Darwin': [
            'SF Mono',
            'Monaco',
            'Menlo',
            'Courier New'
        ]
    }
    
    @staticmethod
    def get_system_fonts() -> List[str]:
        """获取系统可用字体列表"""
        try:
            # 首先尝试使用tkinter获取字体
            root = tk.Tk()
            root.withdraw()  # 隐藏窗口
            
            # 获取所有可用字体
            fonts = list(font.families())
            root.destroy()
            
            if fonts:
                return fonts
        except Exception as e:
            print(f"tkinter字体检测失败: {e}")
        
        # 如果tkinter方法失败，尝试使用系统命令
        try:
            system = platform.system()
            if system == "Linux":
                # 在Linux上使用fc-list命令
                result = subprocess.run(['fc-list', ':family'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    fonts = []
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            # 移除引号
                            font_name = line.strip().strip('"')
                            if font_name and font_name not in fonts:
                                fonts.append(font_name)
                    return fonts
            elif system == "Windows":
                # 在Windows上可以尝试其他方法
                pass
            elif system == "Darwin":  # macOS
                # 在macOS上可以尝试其他方法
                pass
        except Exception as e:
            print(f"系统命令字体检测失败: {e}")
        
        # 返回一些常见的字体作为备用
        return [
            'Arial', 'Helvetica', 'Times New Roman', 'Times',
            'DejaVu Sans', 'DejaVu Serif', 'DejaVu Sans Mono',
            'Liberation Sans', 'Liberation Serif', 'Liberation Mono',
            'Ubuntu', 'Ubuntu Mono', 'TkDefaultFont', 'TkFixedFont'
        ]
    
    @staticmethod
    def find_best_font(font_list: List[str], system: str) -> str:
        """从字体列表中找出最适合的字体"""
        available_fonts = FontManager.get_system_fonts()
        
        # 按优先级查找可用字体
        for font_name in font_list:
            if font_name in available_fonts:
                return font_name
        
        # 如果没有找到，尝试模糊匹配
        for font_name in font_list:
            for available_font in available_fonts:
                if font_name.lower() in available_font.lower() or available_font.lower() in font_name.lower():
                    return available_font
        
        # 如果还是没有找到，返回系统默认字体
        return 'TkDefaultFont'
    
    @staticmethod
    def get_optimal_fonts() -> Dict[str, Tuple[str, int, str]]:
        """获取最优字体配置"""
        system = platform.system()
        
        # 获取最适合的普通字体
        normal_font = FontManager.find_best_font(
            FontManager.FONT_PRIORITIES.get(system, FontManager.FONT_PRIORITIES['Linux']),
            system
        )
        
        # 获取最适合的等宽字体
        mono_font = FontManager.find_best_font(
            FontManager.MONO_FONT_PRIORITIES.get(system, FontManager.MONO_FONT_PRIORITIES['Linux']),
            system
        )
        
        print(f"系统: {system}")
        print(f"选择的普通字体: {normal_font}")
        print(f"选择的等宽字体: {mono_font}")
        
        return {
            'title': (normal_font, 14, 'bold'),
            'subtitle': (normal_font, 12, 'bold'),
            'heading': (normal_font, 11, 'bold'),
            'body': (normal_font, 10, 'normal'),
            'small': (normal_font, 9, 'normal'),
            'code': (mono_font, 10, 'normal')
        }
    
    @staticmethod
    def test_chinese_display(font_name: str) -> bool:
        """测试字体是否能正确显示中文"""
        try:
            root = tk.Tk()
            root.withdraw()
            
            # 创建测试标签
            test_label = tk.Label(root, text="中文测试", font=(font_name, 12))
            test_label.pack()
            
            # 更新窗口以获取实际尺寸
            root.update()
            
            # 获取文本的实际显示宽度
            width = test_label.winfo_reqwidth()
            
            root.destroy()
            
            # 如果宽度太小，说明字体可能不支持中文
            return width > 50
        except Exception as e:
            print(f"测试字体 {font_name} 失败: {e}")
            return False
    
    @staticmethod
    def get_fallback_fonts() -> Dict[str, Tuple[str, int, str]]:
        """获取备用字体配置"""
        return {
            'title': ('TkDefaultFont', 14, 'bold'),
            'subtitle': ('TkDefaultFont', 12, 'bold'),
            'heading': ('TkDefaultFont', 11, 'bold'),
            'body': ('TkDefaultFont', 10, 'normal'),
            'small': ('TkDefaultFont', 9, 'normal'),
            'code': ('TkFixedFont', 10, 'normal')
        } 