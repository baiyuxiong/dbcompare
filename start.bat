@echo off
chcp 65001 >nul

echo 🚀 启动 DBCompare - MySQL表结构比较工具

REM 检查Node.js版本
for /f "tokens=1,2,3 delims=." %%a in ('node --version') do set NODE_VERSION=%%a
set NODE_VERSION=%NODE_VERSION:~1%

if %NODE_VERSION% LSS 18 (
    echo ❌ 错误: Node.js版本过低，需要18.0.0或更高版本
    echo 当前版本: 
    node --version
    echo 请访问 https://nodejs.org 下载最新版本
    pause
    exit /b 1
)

echo ✅ Node.js版本检查通过:
node --version

REM 检查依赖是否已安装
if not exist "node_modules" (
    echo 📦 正在安装依赖...
    npm install
    if errorlevel 1 (
        echo ❌ 依赖安装失败，尝试使用国内镜像...
        npm install --registry=https://registry.npmmirror.com
        if errorlevel 1 (
            echo ❌ 依赖安装失败，请检查网络连接
            pause
            exit /b 1
        )
    )
)

echo ✅ 依赖检查完成

REM 启动应用
echo 🎯 启动应用...
npm run dev

pause 