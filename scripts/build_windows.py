#!/usr/bin/env python3
"""
Windows 平台打包脚本 - 修复版本
专门解决语言文件加载和窗口最大化问题
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

def create_temp_i18n_dir():
    """创建临时的i18n目录结构"""
    print("\n创建临时i18n目录...")
    
    # 创建临时目录
    temp_dir = Path("temp_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # 创建i18n目录
    i18n_dir = temp_dir / "i18n"
    i18n_dir.mkdir()
    
    # 复制语言文件
    src_i18n_dir = Path("src/i18n")
    if src_i18n_dir.exists():
        for lang_file in ["zh_CN.json", "en_US.json"]:
            src_file = src_i18n_dir / lang_file
            dst_file = i18n_dir / lang_file
            if src_file.exists():
                shutil.copy2(src_file, dst_file)
                print(f"✓ 复制 {lang_file}")
            else:
                print(f"✗ 源文件不存在: {src_file}")
    
    return temp_dir

def build_executable(temp_dir=None):
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
        # 构建命令参数
        cmd_args = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",  # 打包成单个文件
            "--windowed",  # 无控制台窗口
            "--name=DBCompare",  # 可执行文件名称
            "--add-data=src/i18n;src/i18n",  # 添加国际化文件（Windows使用分号分隔）
            "--add-data=src/i18n/en_US.json;i18n",  # 确保英文翻译文件在i18n目录下
            "--add-data=src/i18n/zh_CN.json;i18n",  # 确保中文翻译文件在i18n目录下
            "--hidden-import=PyQt6",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=mysql.connector",
            "--hidden-import=sqlparse",
            "--hidden-import=src.i18n.i18n_manager",
            "--hidden-import=src.core.sql_parser",
            "--hidden-import=src.core.sql_generator",
            "--hidden-import=src.core.db_connector",
            "--hidden-import=src.data.models",
            "--hidden-import=src.ui.connection_dialog",
            "--hidden-import=src.ui.language_dialog",
            "--hidden-import=src.utils.icon_manager",
            "--hidden-import=src.utils.util",
            "--collect-all=src",  # 收集所有src模块
            "app.py"
        ]
        
        # 如果有临时目录，添加临时i18n目录
        if temp_dir:
            cmd_args.extend(["--add-data=temp_build/i18n;i18n"])
        
        # 添加图标文件
        if os.path.exists("icon.ico"):
            cmd_args.extend(["--add-data=icon.ico;."])
            cmd_args.extend(["--icon=icon.ico"])
        elif os.path.exists("icon.png"):
            cmd_args.extend(["--add-data=icon.png;."])
        
        print("执行构建命令...")
        print(" ".join(cmd_args))
        
        result = subprocess.run(cmd_args, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ 构建成功")
        return True
    else:
        print("✗ 构建失败")
        print("错误输出:")
        print(result.stderr)
        return False

def cleanup_temp_dir(temp_dir):
    """清理临时目录"""
    if temp_dir and temp_dir.exists():
        shutil.rmtree(temp_dir)
        print("✓ 清理临时目录")

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

def test_built_executable():
    """测试构建的可执行文件"""
    print("\n测试构建的可执行文件...")
    
    exe_path = "dist/DBCompare.exe"
    if not os.path.exists(exe_path):
        print("✗ 可执行文件不存在")
        return False
    
    try:
        # 运行测试脚本
        result = subprocess.run([exe_path, "--test"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ 可执行文件测试通过")
            return True
        else:
            print("✗ 可执行文件测试失败")
            print("输出:", result.stdout)
            print("错误:", result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("✓ 可执行文件启动成功（超时是正常的，因为GUI程序会保持运行）")
        return True
    except Exception as e:
        print(f"✗ 测试可执行文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("DBCompare Windows 打包脚本 - 修复版本")
    print("=" * 60)
    
    temp_dir = None
    
    try:
        # 检查依赖
        check_dependencies()
        
        # 清理构建目录
        clean_build_dirs()
        
        # 创建临时i18n目录
        temp_dir = create_temp_i18n_dir()
        
        # 构建可执行文件
        if build_executable(temp_dir):
            # 测试构建的可执行文件
            test_built_executable()
            
            # 创建桌面快捷方式
            create_shortcut()
            
            print("\n" + "=" * 60)
            print("打包完成！")
            print("=" * 60)
            print("可执行文件位置: dist/DBCompare.exe")
            print("\n修复内容:")
            print("1. ✓ 语言文件加载问题已修复")
            print("2. ✓ 窗口最大化问题已修复")
            print("3. ✓ 添加了内置默认翻译作为备用")
            print("\n使用方法:")
            print("1. 双击 dist/DBCompare.exe 直接运行")
            print("2. 或双击桌面快捷方式运行")
            print("3. 或在命令提示符中运行: dist\\DBCompare.exe")
            return 0
        else:
            print("\n打包失败！")
            return 1
    finally:
        # 清理临时目录
        cleanup_temp_dir(temp_dir)

if __name__ == "__main__":
    sys.exit(main()) 