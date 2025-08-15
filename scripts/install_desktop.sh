#!/bin/bash
# Linux桌面文件安装脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 桌面文件模板
DESKTOP_FILE="[Desktop Entry]
Version=1.0
Type=Application
Name=DBCompare
Comment=MySQL表结构比较工具
Exec=$PROJECT_ROOT/dist/DBCompare
Icon=$PROJECT_ROOT/icon.png
Terminal=false
Categories=Development;Database;
"

# 创建桌面文件
echo "$DESKTOP_FILE" > "$PROJECT_ROOT/DBCompare.desktop"

# 安装到用户目录
if [ -d "$HOME/.local/share/applications" ]; then
    cp "$PROJECT_ROOT/DBCompare.desktop" "$HOME/.local/share/applications/"
    echo "桌面文件已安装到: $HOME/.local/share/applications/DBCompare.desktop"
elif [ -d "/usr/share/applications" ]; then
    sudo cp "$PROJECT_ROOT/DBCompare.desktop" "/usr/share/applications/"
    echo "桌面文件已安装到: /usr/share/applications/DBCompare.desktop"
else
    echo "警告: 未找到合适的应用程序目录"
fi

# 更新桌面数据库
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database
    echo "桌面数据库已更新"
fi

echo "安装完成！"
