#!/usr/bin/env python3
"""
DBCompare 构建脚本入口
重构后的构建脚本统一入口
"""

import sys
import os
from pathlib import Path

# 添加scripts目录到Python路径
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

def main():
    """主函数"""
    # 导入并运行构建脚本
    from build.build import main as build_main
    build_main()

if __name__ == "__main__":
    main()
