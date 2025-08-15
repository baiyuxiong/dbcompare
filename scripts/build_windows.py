#!/usr/bin/env python3
"""
Windows 平台打包脚本
生成可直接双击运行的 .exe 文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """检查必要的依赖"""
    print("检查依赖...")
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("✗ PyInstaller 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 检查其他依赖
    required_packages = [
        "PyQt6",
        "mysql-connector-python", 
        "sqlparse"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装，正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def clean_build_dirs():
    """清理构建目录"""
    print("\n清理构建目录...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 清理 {dir_name}")
    
    # 清理 .pyc 文件
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
    
    print("✓ 清理完成")

def build_executable():
    """构建可执行文件"""
    print("\n开始构建可执行文件...")
    
    # 使用 spec 文件构建
    spec_file = "DBCompare.spec"
    if os.path.exists(spec_file):
        print(f"使用 {spec_file} 配置文件构建...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--clean",  # 清理缓存
            spec_file
        ], capture_output=True, text=True)
    else:
        print("使用默认配置构建...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--onefile",  # 打包成单个文件
            "--windowed",  # 无控制台窗口
            "--name=DBCompare",  # 可执行文件名称
            "--icon=icon.ico" if os.path.exists("icon.ico") else "",
            "--add-data=src/i18n;src/i18n",  # 添加国际化文件（Windows使用分号分隔）
            "--add-data=icon.png;." if os.path.exists("icon.png") else "",
            "--hidden-import=PyQt6",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=mysql.connector",
            "--hidden-import=sqlparse",
            "app.py"
        ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ 构建成功")
        return True
    else:
        print("✗ 构建失败")
        print("错误输出:")
        print(result.stderr)
        return False

def create_shortcut():
    """创建桌面快捷方式"""
    print("\n创建桌面快捷方式...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        # 获取桌面路径
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "DBCompare.lnk")
        
        # 获取可执行文件路径
        exe_path = os.path.abspath("dist/DBCompare.exe")
        
        # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = exe_path
        shortcut.save()
        
        print(f"✓ 桌面快捷方式已创建: {shortcut_path}")
        return True
    except ImportError:
        print("⚠ 无法创建桌面快捷方式（需要 pywin32 和 winshell）")
        print("  可执行文件位置: dist/DBCompare.exe")
        return False
    except Exception as e:
        print(f"⚠ 创建快捷方式失败: {e}")
        return False

def main():
    """主函数"""
    print("DBCompare Windows 打包脚本")
    print("=" * 50)
    
    # 检查依赖
    check_dependencies()
    
    # 清理构建目录
    clean_build_dirs()
    
    # 构建可执行文件
    if build_executable():
        # 创建桌面快捷方式
        create_shortcut()
        
        print("\n" + "=" * 50)
        print("打包完成！")
        print("=" * 50)
        print("可执行文件位置: dist/DBCompare.exe")
        print("\n使用方法:")
        print("1. 双击 dist/DBCompare.exe 直接运行")
        print("2. 或双击桌面快捷方式运行")
        print("3. 或在命令提示符中运行: dist\\DBCompare.exe")
        return 0
    else:
        print("\n打包失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 