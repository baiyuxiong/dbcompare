#!/usr/bin/env python3
"""
DBCompare 构建脚本入口
支持标准Python构建和跨平台可执行文件打包
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def detect_platform():
    """检测当前平台"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def standard_build():
    """标准Python构建"""
    print("DBCompare 标准构建")
    print("=" * 50)
    
    # 检查是否安装了构建工具
    try:
        import setuptools
        print("✓ setuptools 已安装")
    except ImportError:
        print("✗ setuptools 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "setuptools"], check=True)
    
    # 构建项目
    print("\n开始构建项目...")
    try:
        subprocess.run([sys.executable, "setup.py", "build"], check=True)
        print("✓ 构建完成")
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        return 1
    
    # 可选：创建分发包
    print("\n创建分发包...")
    try:
        subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], check=True)
        print("✓ 分发包创建完成")
    except subprocess.CalledProcessError as e:
        print(f"✗ 分发包创建失败: {e}")
        return 1
    
    print("\n构建成功完成！")
    print("可执行文件: python app.py")
    print("安装包: pip install .")
    return 0

def generate_spec():
    """生成跨平台 spec 文件"""
    print("生成跨平台 spec 文件...")
    
    spec_generator = Path(__file__).parent / "scripts" / "generate_spec.py"
    if spec_generator.exists():
        result = subprocess.run([sys.executable, str(spec_generator)])
        return result.returncode == 0
    else:
        print(f"✗ 找不到 spec 生成器: {spec_generator}")
        return False

def platform_executable_build(platform_name):
    """平台特定可执行文件构建"""
    platform_names = {
        "windows": "Windows",
        "macos": "macOS", 
        "linux": "Linux"
    }
    
    print(f"DBCompare {platform_names.get(platform_name, platform_name)} 可执行文件构建")
    print("=" * 50)
    
    # 检查并安装 PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("✗ PyInstaller 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 生成 spec 文件
    if not generate_spec():
        print("✗ spec 文件生成失败")
        return 1
    
    # 运行平台特定打包脚本
    build_script = Path(__file__).parent / "scripts" / f"build_{platform_name}.py"
    if build_script.exists():
        print(f"\n运行 {platform_names.get(platform_name, platform_name)} 打包脚本: {build_script}")
        result = subprocess.run([sys.executable, str(build_script)])
        return result.returncode
    else:
        print(f"✗ 找不到 {platform_names.get(platform_name, platform_name)} 打包脚本: {build_script}")
        return 1

def auto_platform_build():
    """自动检测平台并构建"""
    platform_name = detect_platform()
    print(f"自动检测到平台: {platform_name}")
    
    if platform_name == "unknown":
        print("⚠ 未知平台，使用标准构建")
        return standard_build()
    else:
        return platform_executable_build(platform_name)

def show_help():
    """显示帮助信息"""
    print("DBCompare 构建脚本")
    print("=" * 50)
    print("支持平台: Windows, macOS, Linux")
    print("\n构建类型:")
    print("  standard/package/pip - 标准Python包构建")
    print("  windows              - Windows可执行文件构建")
    print("  macos                - macOS可执行文件构建") 
    print("  linux                - Linux可执行文件构建")
    print("  auto                 - 自动检测平台并构建")
    print("\n使用示例:")
    print("  python build.py standard  # 标准构建")
    print("  python build.py windows   # Windows可执行文件")
    print("  python build.py macos     # macOS可执行文件")
    print("  python build.py linux     # Linux可执行文件")
    print("  python build.py auto      # 自动检测平台")
    print("\n当前平台:", detect_platform())

def main():
    """主函数"""
    if len(sys.argv) > 1:
        build_type = sys.argv[1].lower()
        
        if build_type in ["standard", "package", "pip"]:
            return standard_build()
        elif build_type in ["windows", "win"]:
            return platform_executable_build("windows")
        elif build_type in ["macos", "mac", "osx"]:
            return platform_executable_build("macos")
        elif build_type in ["linux", "unix"]:
            return platform_executable_build("linux")
        elif build_type in ["auto", "detect"]:
            return auto_platform_build()
        elif build_type in ["help", "-h", "--help"]:
            show_help()
            return 0
        else:
            print(f"未知的构建类型: {build_type}")
            show_help()
            return 1
    else:
        # 默认显示帮助
        show_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
