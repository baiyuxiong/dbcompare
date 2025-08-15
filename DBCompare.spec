# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/baiyuxiong/code/dbcompare/app.py'],
    pathex=[],
    binaries=[],
    datas=[('connections.db', '.'), ('src', 'src')],
    hiddenimports=['main', 'src.main', 'src.core', 'src.core.sql_parser', 'src.core.sql_generator', 'src.core.db_connector', 'src.data', 'src.data.models', 'src.ui', 'src.ui.connection_dialog', 'src.ui.language_dialog', 'src.i18n', 'src.i18n.i18n_manager', 'src.utils', 'src.utils.util', 'PyQt6', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui', 'sqlite3', 'mysql.connector', 'mysql.connector.plugins.mysql_native_password', 'sqlparse', 'threading', 'datetime'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DBCompare',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DBCompare',
)
app = BUNDLE(
    coll,
    name='DBCompare.app',
    icon=None,
    bundle_identifier=None,
)
