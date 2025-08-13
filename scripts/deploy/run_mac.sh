#!/bin/bash

# 运行 DBCompare 应用程序
# 使用方法: ./run_mac.sh

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# 切换到项目根目录
cd "$PROJECT_ROOT"

# 检查应用程序是否存在
if [ -f "./dist/DBCompare/DBCompare" ]; then
    echo "启动 DBCompare 应用程序..."
    ./dist/DBCompare/DBCompare
elif [ -d "./dist/DBCompare.app" ]; then
    echo "启动 DBCompare.app..."
    open ./dist/DBCompare.app
else
    echo "错误: 找不到 DBCompare 应用程序"
    echo "请先运行构建脚本构建应用程序"
    echo "可用的构建脚本:"
    echo "  python3 scripts/build/build.py"
    echo "  bash scripts/build/build_macos.sh"
    exit 1
fi
