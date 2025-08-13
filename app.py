#!/usr/bin/env python3
"""
DBCompare - MySQL表结构比较工具
重构后的应用程序入口
"""

import tkinter as tk
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import SQLCompareApp

def main():
    """主函数"""
    root = tk.Tk()
    app = SQLCompareApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
