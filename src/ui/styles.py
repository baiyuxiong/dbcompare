"""
UI样式配置文件
定义所有UI组件的样式和主题
"""

import tkinter as tk
from tkinter import ttk
import platform
import sys
from .font_manager import FontManager

class StyleManager:
    """样式管理器"""
    
    @staticmethod
    def get_system_fonts():
        """获取系统字体配置"""
        try:
            # 使用字体管理器获取最优字体
            return FontManager.get_optimal_fonts()
        except Exception as e:
            print(f"字体管理器初始化失败: {e}")
            # 使用备用字体配置
            return FontManager.get_fallback_fonts()
    
    @staticmethod
    def setup_styles():
        """设置所有样式"""
        style = ttk.Style()
        
        # 尝试使用现代主题
        try:
            style.theme_use('clam')
        except:
            pass  # 如果主题不可用，使用默认主题
        
        # 颜色方案
        colors = {
            'primary': '#3498db',      # 主色调 - 蓝色
            'success': '#27ae60',      # 成功色 - 绿色
            'warning': '#f39c12',      # 警告色 - 橙色
            'danger': '#e74c3c',       # 危险色 - 红色
            'info': '#17a2b8',         # 信息色 - 青色
            'dark': '#2c3e50',         # 深色
            'light': '#ecf0f1',        # 浅色
            'white': '#ffffff',        # 白色
            'gray': '#95a5a6',         # 灰色
            'light_gray': '#bdc3c7'    # 浅灰色
        }
        
        # 获取系统字体配置
        fonts = StyleManager.get_system_fonts()
        
        # 主标题样式
        style.configure('Title.TLabel', 
                       font=fonts['title'],
                       foreground=colors['dark'],
                       background=colors['light'],
                       padding=10)
        
        # 副标题样式
        style.configure('Subtitle.TLabel',
                       font=fonts['subtitle'],
                       foreground=colors['dark'],
                       background=colors['light'],
                       padding=8)
        
        # 按钮样式
        style.configure('Primary.TButton',
                       font=fonts['body'],
                       background=colors['primary'],
                       foreground=colors['white'],
                       padding=(15, 8))
        
        style.configure('Success.TButton',
                       font=fonts['body'],
                       background=colors['success'],
                       foreground=colors['white'],
                       padding=(15, 8))
        
        style.configure('Warning.TButton',
                       font=fonts['body'],
                       background=colors['warning'],
                       foreground=colors['white'],
                       padding=(15, 8))
        
        style.configure('Danger.TButton',
                       font=fonts['body'],
                       background=colors['danger'],
                       foreground=colors['white'],
                       padding=(15, 8))
        
        style.configure('Info.TButton',
                       font=fonts['body'],
                       background=colors['info'],
                       foreground=colors['white'],
                       padding=(15, 8))
        
        # 框架样式
        style.configure('Card.TFrame',
                       background=colors['white'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Light.TFrame',
                       background=colors['light'])
        
        # 标签框架样式
        style.configure('Title.TLabelframe',
                       font=fonts['heading'],
                       foreground=colors['dark'],
                       background=colors['light'])
        
        style.configure('Title.TLabelframe.Label',
                       font=fonts['heading'],
                       foreground=colors['dark'],
                       background=colors['light'])
        
        # 树形视图样式
        style.configure('Treeview',
                       font=fonts['small'],
                       rowheight=25,
                       background=colors['white'],
                       foreground=colors['dark'],
                       fieldbackground=colors['white'])
        
        style.configure('Treeview.Heading',
                       font=fonts['body'],
                       background=colors['dark'],
                       foreground=colors['white'])
        
        # 组合框样式
        style.configure('TCombobox',
                       font=fonts['small'],
                       padding=5)
        
        # 复选框样式
        style.configure('TCheckbutton',
                       font=fonts['small'])
        
        # 单选按钮样式
        style.configure('TRadiobutton',
                       font=fonts['body'])
        
        # 标签样式
        style.configure('TLabel',
                       font=fonts['body'])
        
        # 输入框样式
        style.configure('TEntry',
                       font=fonts['small'],
                       padding=5)
        
        # 进度条样式
        style.configure('TProgressbar',
                       background=colors['primary'],
                       troughcolor=colors['light_gray'])
        
        # 滚动条样式
        style.configure('Vertical.TScrollbar',
                       background=colors['gray'],
                       troughcolor=colors['light_gray'])
        
        style.configure('Horizontal.TScrollbar',
                       background=colors['gray'],
                       troughcolor=colors['light_gray'])
        
        return colors, fonts
    
    @staticmethod
    def configure_tree_tags(tree, colors):
        """配置树形视图的标签样式"""
        try:
            fonts = StyleManager.get_system_fonts()
            
            tree.tag_configure("table_header", 
                              font=fonts['heading'], 
                              background=colors['dark'], 
                              foreground=colors['white'])
            
            tree.tag_configure("header", 
                              font=fonts['body'], 
                              background=colors['light'], 
                              foreground=colors['dark'])
            
            tree.tag_configure("different", 
                              foreground=colors['danger'], 
                              font=fonts['small'])
            
            tree.tag_configure("missing", 
                              foreground=colors['primary'], 
                              font=fonts['small'])
            
            tree.tag_configure("added", 
                              foreground=colors['success'], 
                              font=fonts['small'])
            
            tree.tag_configure("modified", 
                              foreground=colors['warning'], 
                              font=fonts['small'])
        except Exception as e:
            print(f"配置树形视图标签失败: {e}")
            # 使用默认配置
            tree.tag_configure("table_header", 
                              background=colors['dark'], 
                              foreground=colors['white'])
            
            tree.tag_configure("header", 
                              background=colors['light'], 
                              foreground=colors['dark'])
            
            tree.tag_configure("different", 
                              foreground=colors['danger'])
            
            tree.tag_configure("missing", 
                              foreground=colors['primary'])
            
            tree.tag_configure("added", 
                              foreground=colors['success'])
            
            tree.tag_configure("modified", 
                              foreground=colors['warning'])
    
    @staticmethod
    def get_icon_text(icon_type):
        """获取图标文本"""
        icons = {
            'connect': '连接',
            'file': '文件',
            'compare': '比较',
            'generate': '生成',
            'sync': '同步',
            'hide': '隐藏',
            'missing': '缺失',
            'test': '测试',
            'save': '保存',
            'delete': '删除',
            'add': '新建',
            'select': '选择',
            'cancel': '取消',
            'database': '数据库',
            'settings': '设置',
            'list': '列表',
            'target': '目标',
            'sql': 'SQL',
            'arrow_right': '→',
            'arrow_left': '←',
            'chart': '图表'
        }
        return icons.get(icon_type, '') 