#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包脚本
支持 Windows、Mac 和 Linux 平台
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "win"
    elif system == "darwin":
        return "mac"
    elif system == "linux":
        return "linux"
    else:
        raise ValueError(f"不支持的操作系统: {system}")

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理 .spec 文件
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    for spec_file in spec_files:
        print(f"删除文件: {spec_file}")
        os.remove(spec_file)

def install_requirements():
    """安装依赖"""
    print("安装依赖包...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # 安装 PyInstaller
    print("安装 PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def build_app(platform_name):
    """构建应用程序"""
    print(f"开始为 {platform_name} 平台构建应用...")
    
    # 基础 PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 不显示控制台窗口 (Windows/Mac)
        "--name=DBCompare",  # 应用名称
        "--icon=icon.ico" if platform_name == "win" else "",  # Windows 图标
        "--add-data=connections.db;." if platform_name == "win" else "--add-data=connections.db:.",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.scrolledtext",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=sqlite3",
        "--hidden-import=mysql.connector",
        "--hidden-import=sqlparse",
        "--hidden-import=threading",
        "--hidden-import=datetime",
        "main.py"
    ]
    
    # 移除空字符串
    cmd = [arg for arg in cmd if arg]
    
    # 平台特定配置
    if platform_name == "win":
        cmd.extend([
            "--console",  # Windows 下保留控制台以便调试
        ])
    elif platform_name == "mac":
        cmd.extend([
            "--target-architecture=universal2",  # 支持 Intel 和 Apple Silicon
        ])
    elif platform_name == "linux":
        cmd.extend([
            "--console",  # Linux 下保留控制台
        ])
    
    print(f"执行命令: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def create_icon():
    """创建应用图标（如果不存在）"""
    if not os.path.exists("icon.ico"):
        print("创建默认图标...")
        # 这里可以添加创建默认图标的代码
        # 或者提示用户提供图标文件
        print("提示: 可以添加 icon.ico 文件作为应用图标")

def main():
    """主函数"""
    try:
        # 获取平台信息
        platform_name = get_platform_info()
        print(f"检测到平台: {platform_name}")
        
        # 清理构建目录
        clean_build_dirs()
        
        # 安装依赖
        install_requirements()
        
        # 创建图标
        create_icon()
        
        # 构建应用
        build_app(platform_name)
        
        print(f"\n✅ 构建完成!")
        print(f"可执行文件位置: dist/DBCompare{'exe' if platform_name == 'win' else ''}")
        
        if platform_name == "win":
            print("Windows 用户: 运行 dist/DBCompare.exe")
        elif platform_name == "mac":
            print("macOS 用户: 运行 dist/DBCompare")
        else:
            print("Linux 用户: 运行 ./dist/DBCompare")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 