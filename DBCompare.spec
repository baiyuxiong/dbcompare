# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = Path.cwd()

# 数据文件
datas = [('icon.png', '.'), ('src/i18n/en_US.json', 'i18n'), ('src/i18n/zh_CN.json', 'i18n'), ('README.md', '.')]

# 隐藏导入 - 包含所有项目模块
hiddenimports = ['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'mysql.connector', 'mysql.connector.plugins.mysql_native_password', 'sqlparse', 'sqlite3', 'main', 'src.main', 'core', 'src.core', 'src.core.sql_parser', 'src.core.sql_generator', 'src.core.db_connector', 'data', 'src.data', 'src.data.models', 'ui', 'src.ui', 'src.ui.connection_dialog', 'src.ui.language_dialog', 'i18n', 'src.i18n', 'src.i18n.i18n_manager', 'utils', 'src.utils', 'src.utils.util', 'threading', 'datetime', 'json', 'pathlib']

# 排除的模块
excludes = ['matplotlib', 'numpy', 'pandas', 'scipy', 'tkinter', 'test', 'unittest']

a = Analysis(
    ['app.py'],
    pathex=[str(project_root), str(project_root / "src")],
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

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DBCompare',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False以隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.png' if os.path.exists('icon.png') else None,
)
