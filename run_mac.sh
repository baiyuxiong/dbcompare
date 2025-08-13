#!/bin/bash

# 运行 DBCompare 应用程序
# 使用方法: ./run_mac.sh

# 检查应用程序是否存在
if [ -f "./dist/DBCompare/DBCompare" ]; then
    echo "启动 DBCompare 应用程序..."
    ./dist/DBCompare/DBCompare
elif [ -d "./dist/DBCompare.app" ]; then
    echo "启动 DBCompare.app..."
    open ./dist/DBCompare.app
else
    echo "错误: 找不到 DBCompare 应用程序"
    echo "请先运行 python3 build.py 构建应用程序"
    exit 1
fi
