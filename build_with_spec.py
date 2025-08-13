#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 spec 文件的 PyInstaller 打包脚本
提供更高级的打包选项和更好的控制
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
from pathlib import Path

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='DBCompare 打包脚本')
    parser.add_argument('--platform', choices=['win', 'mac', 'linux', 'auto'], 
                       default='auto', help='目标平台')
    parser.add_argument('--console', action='store_true', 
                       help='显示控制台窗口')
    parser.add_argument('--debug', action='store_true', 
                       help='启用调试模式')
    parser.add_argument('--clean', action='store_true', 
                       help='清理构建文件')
    parser.add_argument('--icon', type=str, 
                       help='自定义图标文件路径')
    parser.add_argument('--name', type=str, default='DBCompare',
                       help='可执行文件名称')
    return parser.parse_args()

def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
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
    
    # 清理 .spec 文件（除了我们的主spec文件）
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec") and f != "DBCompare.spec"]
    for spec_file in spec_files:
        print(f"删除文件: {spec_file}")
        os.remove(spec_file)

def install_requirements():
    """安装依赖"""
    print("安装依赖包...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    print("安装 PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def update_spec_file(args, platform_name):
    """更新 spec 文件配置"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 获取当前目录
current_dir = Path(__file__).parent

# 定义数据文件
datas = [
    ('connections.db', '.'),
]

# 定义隐藏导入
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.scrolledtext',
    'tkinter.messagebox',
    'sqlite3',
    'mysql.connector',
    'sqlparse',
    'threading',
    'datetime',
    'sql_parser',
    'sql_generator',
    'connection_dialog',
    'models',
    'db_connector',
    'util',
]

# 定义排除的模块
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'cv2',
    'torch',
    'tensorflow',
]

# 分析配置
a = Analysis(
    ['main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# 清理分析结果
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 可执行文件配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{name}',
    debug={debug},
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{icon}' if os.path.exists('{icon}') else None,
)
"""
    
    # 替换配置参数
    icon_path = args.icon if args.icon else 'icon.ico'
    spec_content = spec_content.format(
        name=args.name,
        debug=str(args.debug),
        console=str(args.console),
        icon=icon_path
    )
    
    # 写入临时 spec 文件
    temp_spec = f"{args.name}.spec"
    with open(temp_spec, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    return temp_spec

def build_app(spec_file, platform_name):
    """构建应用程序"""
    print(f"开始为 {platform_name} 平台构建应用...")
    
    # 基础 PyInstaller 命令
    cmd = ["pyinstaller", spec_file]
    
    # 平台特定配置
    if platform_name == "mac":
        cmd.extend(["--target-architecture=universal2"])
    
    print(f"执行命令: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    """主函数"""
    args = parse_arguments()
    
    try:
        # 获取平台信息
        platform_name = args.platform
        if platform_name == 'auto':
            platform_name = get_platform_info()
        print(f"目标平台: {platform_name}")
        
        # 清理构建目录
        if args.clean:
            clean_build_dirs()
        
        # 安装依赖
        install_requirements()
        
        # 更新 spec 文件
        spec_file = update_spec_file(args, platform_name)
        
        # 构建应用
        build_app(spec_file, platform_name)
        
        # 设置可执行权限（Linux/Mac）
        if platform_name in ["linux", "mac"]:
            exe_name = f"dist/{args.name}"
            if os.path.exists(exe_name):
                os.chmod(exe_name, 0o755)
        
        print(f"\n✅ 构建完成!")
        exe_ext = ".exe" if platform_name == "win" else ""
        print(f"可执行文件位置: dist/{args.name}{exe_ext}")
        
        if platform_name == "win":
            print(f"Windows 用户: 运行 dist/{args.name}.exe")
        elif platform_name == "mac":
            print(f"macOS 用户: 运行 dist/{args.name}")
        else:
            print(f"Linux 用户: 运行 ./dist/{args.name}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)
    finally:
        # 清理临时 spec 文件
        if 'spec_file' in locals() and os.path.exists(spec_file):
            os.remove(spec_file)

if __name__ == "__main__":
    main() 