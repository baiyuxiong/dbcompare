#!/usr/bin/env python3
"""
MySQL表结构比较工具 - PyQt6版本启动文件
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main as pyqt_main

def main():
    """主函数入口"""
    pyqt_main()

if __name__ == "__main__":
    main() 