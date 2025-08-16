#!/usr/bin/env python3
"""
跨平台 spec 文件生成器
根据当前平台自动生成相应的 PyInstaller spec 文件
"""

import os
import sys
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

def get_platform_config(platform_name):
    """获取平台特定配置"""
    configs = {
        "windows": {
            "onefile": True,
            "console": False,
            "add_data_separator": ";",
            "exe_name": "DBCompare.exe",
            "bundle_name": "DBCompare.exe"
        },
        "macos": {
            "onefile": False,
            "console": False,
            "add_data_separator": ":",
            "exe_name": "DBCompare",
            "bundle_name": "DBCompare.app"
        },
        "linux": {
            "onefile": True,
            "console": False,
            "add_data_separator": ":",
            "exe_name": "DBCompare",
            "bundle_name": "DBCompare"
        }
    }
    return configs.get(platform_name, configs["linux"])

def generate_spec_content(platform_name):
    """生成 spec 文件内容"""
    config = get_platform_config(platform_name)
    project_root = Path.cwd()
    
    # 数据文件
    datas = [
        # 图标文件 - 根据平台选择
        ('icon.ico', '.') if platform_name == "windows" and os.path.exists('icon.ico') else ('icon.png', '.'),
        # 国际化文件 - 确保在i18n目录下
        ('src/i18n/en_US.json', 'i18n'),
        ('src/i18n/zh_CN.json', 'i18n'),
        # 其他资源文件
        ('README.md', '.'),
    ]
    
    # 隐藏导入
    hiddenimports = [
        # PyQt6 相关
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        # 数据库相关
        'mysql.connector',
        'mysql.connector.plugins.mysql_native_password',
        'sqlparse',
        'sqlite3',
        # 项目模块
        'main',
        'src.main',
        'core',
        'src.core',
        'src.core.sql_parser',
        'src.core.sql_generator', 
        'src.core.db_connector',
        'data',
        'src.data',
        'src.data.models',
        'ui',
        'src.ui',
        'src.ui.connection_dialog',
        'src.ui.language_dialog',
        'i18n',
        'src.i18n',
        'src.i18n.i18n_manager',
        'utils',
        'src.utils',
        'src.utils.util',
        'src.utils.icon_manager',
        # 标准库
        'threading',
        'datetime',
        'json',
        'pathlib',
    ]
    
    # 排除的模块
    excludes = [
        'matplotlib',
        'numpy', 
        'pandas',
        'scipy',
        'tkinter',
        'test',
        'unittest',
    ]
    
    # 生成 spec 内容
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = Path.cwd()

# 数据文件
datas = {datas}

# 隐藏导入 - 包含所有项目模块
hiddenimports = {hiddenimports}

# 排除的模块
excludes = {excludes}

a = Analysis(
    ['app.py'],
    pathex=[str(project_root), str(project_root / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{config["exe_name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={config["console"]},  # 设置为False以隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else ('icon.png' if os.path.exists('icon.png') else None),
)
'''
    
    # 如果是 macOS，添加 BUNDLE 配置
    if platform_name == "macos":
        spec_content += f'''

# macOS .app 包配置
app = BUNDLE(
    exe,
    name='{config["bundle_name"]}',
    icon='icon.ico' if os.path.exists('icon.ico') else ('icon.png' if os.path.exists('icon.png') else None),
    bundle_identifier='com.dbcompare.app',
    info_plist={{
        'CFBundleName': 'DBCompare',
        'CFBundleDisplayName': 'DBCompare',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    }},
)
'''
    
    return spec_content

def main():
    """主函数"""
    print("DBCompare 跨平台 spec 文件生成器")
    print("=" * 50)
    
    # 检测平台
    platform_name = detect_platform()
    print(f"检测到平台: {platform_name}")
    
    if platform_name == "unknown":
        print("⚠ 未知平台，使用 Linux 配置")
        platform_name = "linux"
    
    # 生成 spec 内容
    spec_content = generate_spec_content(platform_name)
    
    # 写入 spec 文件
    spec_file = "DBCompare.spec"
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print(f"✓ spec 文件已生成: {spec_file}")
    print(f"✓ 平台配置: {platform_name}")
    
    # 显示配置信息
    config = get_platform_config(platform_name)
    print(f"\n平台配置详情:")
    print(f"  可执行文件: {config['exe_name']}")
    print(f"  图标文件: {'icon.ico' if platform_name == 'windows' and os.path.exists('icon.ico') else 'icon.png'}")
    print(f"  单文件模式: {config['onefile']}")
    print(f"  控制台窗口: {config['console']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 