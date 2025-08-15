#!/usr/bin/env python3
"""
MySQL表结构比较工具 - PyQt6版本启动文件
"""

import sys
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 添加src目录到Python路径
src_path = os.path.join(current_dir, 'src')
if os.path.exists(src_path):
    sys.path.insert(0, src_path)
else:
    # 如果src目录不存在，可能是打包后的环境，尝试直接导入
    # 在打包环境中，所有模块都应该在同一层级
    pass

try:
    from main import main as pyqt_main
except ImportError:
    # 如果直接导入失败，尝试从src.main导入
    try:
        from src.main import main as pyqt_main
    except ImportError:
        # 如果还是失败，尝试从当前目录的main导入
        try:
            sys.path.insert(0, current_dir)
            from main import main as pyqt_main
        except ImportError as e:
            print(f"无法导入main模块: {e}")
            print(f"当前目录: {current_dir}")
            print(f"Python路径: {sys.path}")
            sys.exit(1)

def main():
    """主函数入口"""
    pyqt_main()

if __name__ == "__main__":
    main() 