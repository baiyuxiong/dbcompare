#!/bin/bash

echo "========================================"
echo "   DBCompare Linux 打包脚本"
echo "========================================"

# 检查 Python 环境
echo "正在检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请确保已安装 Python3"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch Linux: sudo pacman -S python python-pip"
    exit 1
fi

python3 --version

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "警告: 建议在虚拟环境中运行此脚本"
    echo "可以使用以下命令创建虚拟环境:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo ""
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查系统依赖
echo ""
echo "正在检查系统依赖..."
if ! command -v tkinter &> /dev/null; then
    echo "警告: 可能需要安装 tkinter"
    echo "Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "CentOS/RHEL: sudo yum install tkinter"
    echo "Arch Linux: sudo pacman -S tk"
fi

# 安装依赖包
echo ""
echo "正在安装依赖包..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 安装依赖包失败"
    exit 1
fi

# 安装 PyInstaller
echo ""
echo "正在安装 PyInstaller..."
python3 -m pip install pyinstaller
if [ $? -ne 0 ]; then
    echo "错误: 安装 PyInstaller 失败"
    exit 1
fi

# 清理旧的构建文件
echo ""
echo "正在清理旧的构建文件..."
rm -rf build dist __pycache__ *.spec

# 构建应用程序
echo ""
echo "开始构建 Linux 应用程序..."
pyinstaller \
    --onefile \
    --console \
    --name=DBCompare \
    --add-data=connections.db:. \
    --hidden-import=tkinter \
    --hidden-import=tkinter.ttk \
    --hidden-import=tkinter.filedialog \
    --hidden-import=tkinter.scrolledtext \
    --hidden-import=tkinter.messagebox \
    --hidden-import=sqlite3 \
    --hidden-import=mysql.connector \
    --hidden-import=sqlparse \
    --hidden-import=threading \
    --hidden-import=datetime \
    main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 构建失败！"
    exit 1
fi

# 设置可执行权限
chmod +x dist/DBCompare

echo ""
echo "✅ 构建完成！"
echo "可执行文件位置: dist/DBCompare"
echo ""
echo "运行方式:"
echo "1. 在终端中运行: ./dist/DBCompare"
echo "2. 或双击文件管理器中的 DBCompare 文件"
echo ""
echo "如果遇到权限问题，请运行: chmod +x dist/DBCompare" 