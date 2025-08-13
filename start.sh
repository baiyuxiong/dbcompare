#!/bin/bash

# DBCompare 快速启动脚本

echo "🚀 启动 DBCompare - MySQL表结构比较工具"

# 检查Node.js版本
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ 错误: Node.js版本过低，需要18.0.0或更高版本"
    echo "当前版本: $(node --version)"
    echo "请访问 https://nodejs.org 下载最新版本"
    exit 1
fi

echo "✅ Node.js版本检查通过: $(node --version)"

# 检查依赖是否已安装
if [ ! -d "node_modules" ]; then
    echo "📦 正在安装依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，尝试使用国内镜像..."
        npm install --registry=https://registry.npmmirror.com
        if [ $? -ne 0 ]; then
            echo "❌ 依赖安装失败，请检查网络连接"
            exit 1
        fi
    fi
fi

echo "✅ 依赖检查完成"

# 启动应用
echo "🎯 启动应用..."
npm run dev 