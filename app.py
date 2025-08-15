#!/usr/bin/env python3
"""
MySQL表结构比较工具 - PyQt6版本启动文件
"""

import sys
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 检查是否在PyInstaller打包环境中
if getattr(sys, 'frozen', False):
    # 打包环境
    base_path = sys._MEIPASS
    # 添加打包环境中的路径
    sys.path.insert(0, base_path)
    # 如果src目录存在，也添加到路径中
    src_path = os.path.join(base_path, 'src')
    if os.path.exists(src_path):
        sys.path.insert(0, src_path)
else:
    # 开发环境
    # 添加src目录到Python路径
    src_path = os.path.join(current_dir, 'src')
    if os.path.exists(src_path):
        sys.path.insert(0, src_path)

# 尝试导入main模块
try:
    from main import main as pyqt_main
except ImportError:
    try:
        # 尝试从src.main导入
        from src.main import main as pyqt_main
    except ImportError:
        try:
            # 尝试从当前目录的main导入
            sys.path.insert(0, current_dir)
            from main import main as pyqt_main
        except ImportError as e:
            print(f"无法导入main模块: {e}")
            print(f"当前目录: {current_dir}")
            print(f"Python路径: {sys.path}")
            if getattr(sys, 'frozen', False):
                print(f"打包环境路径: {sys._MEIPASS}")
            sys.exit(1)

def main():
    """主函数入口"""
    pyqt_main()

if __name__ == "__main__":
    main() 