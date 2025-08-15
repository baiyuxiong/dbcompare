#!/usr/bin/env python3
"""
macOS 平台打包脚本
生成可直接双击运行的 .app 文件
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
            "--onedir",  # macOS通常使用目录模式
            "--windowed",  # 无控制台窗口
            "--name=DBCompare",  # 可执行文件名称
            "--add-data=src/i18n:src/i18n",  # 添加国际化文件（macOS使用冒号分隔）
            "--add-data=icon.png:." if os.path.exists("icon.png") else "",
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

def create_app_bundle():
    """创建 .app 包"""
    print("\n创建 .app 包...")
    
    try:
        # 检查是否已经生成了 .app 文件
        app_path = "dist/DBCompare.app"
        if os.path.exists(app_path):
            print(f"✓ .app 包已存在: {app_path}")
            return True
        
        # 如果没有 .app 文件，尝试创建
        print("尝试创建 .app 包...")
        
        # 创建基本的 .app 结构
        app_contents = "dist/DBCompare.app/Contents"
        os.makedirs(f"{app_contents}/MacOS", exist_ok=True)
        os.makedirs(f"{app_contents}/Resources", exist_ok=True)
        
        # 复制可执行文件
        if os.path.exists("dist/DBCompare"):
            shutil.copy("dist/DBCompare", f"{app_contents}/MacOS/DBCompare")
            os.chmod(f"{app_contents}/MacOS/DBCompare", 0o755)
        
        # 创建 Info.plist
        info_plist = f"""[CFBundle]
CFBundleExecutable = DBCompare
CFBundleIdentifier = com.dbcompare.app
CFBundleName = DBCompare
CFBundleDisplayName = DBCompare
CFBundleVersion = 1.0.0
CFBundleShortVersionString = 1.0.0
CFBundlePackageType = APPL
CFBundleSignature = ????"""
        
        with open(f"{app_contents}/Info.plist", "w") as f:
            f.write(info_plist)
        
        print(f"✓ .app 包已创建: {app_path}")
        return True
        
    except Exception as e:
        print(f"⚠ 创建 .app 包失败: {e}")
        print("  可执行文件位置: dist/DBCompare")
        return False

def create_desktop_file():
    """创建桌面文件"""
    print("\n创建桌面文件...")
    
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=DBCompare
Comment=MySQL表结构比较工具
Exec={exec_path}
Icon={icon_path}
Terminal=false
Categories=Development;Database;
"""
    
    # 获取可执行文件路径
    app_path = os.path.abspath("dist/DBCompare.app")
    exec_path = f"{app_path}/Contents/MacOS/DBCompare"
    icon_path = os.path.abspath("icon.png") if os.path.exists("icon.png") else ""
    
    # 创建桌面文件
    desktop_file = "DBCompare.desktop"
    with open(desktop_file, "w", encoding="utf-8") as f:
        f.write(desktop_content.format(
            exec_path=exec_path,
            icon_path=icon_path
        ))
    
    # 设置可执行权限
    os.chmod(desktop_file, 0o755)
    
    print(f"✓ 桌面文件已创建: {desktop_file}")

def main():
    """主函数"""
    print("DBCompare macOS 打包脚本")
    print("=" * 50)
    
    # 检查依赖
    check_dependencies()
    
    # 清理构建目录
    clean_build_dirs()
    
    # 构建可执行文件
    if build_executable():
        # 创建 .app 包
        create_app_bundle()
        
        # 创建桌面文件
        create_desktop_file()
        
        print("\n" + "=" * 50)
        print("打包完成！")
        print("=" * 50)
        print("可执行文件位置: dist/DBCompare")
        print(".app 包位置: dist/DBCompare.app")
        print("桌面文件: DBCompare.desktop")
        print("\n使用方法:")
        print("1. 双击 dist/DBCompare.app 直接运行")
        print("2. 或双击桌面文件运行")
        print("3. 或在终端运行: ./dist/DBCompare")
        print("4. 或运行: open dist/DBCompare.app")
        return 0
    else:
        print("\n打包失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 