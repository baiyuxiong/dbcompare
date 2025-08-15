#!/usr/bin/env python3
"""
构建配置文件
定义构建过程中使用的各种配置参数
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 应用信息
APP_NAME = "DBCompare"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "MySQL表结构比较工具"

# 构建配置
BUILD_CONFIG = {
    "name": APP_NAME,
    "version": APP_VERSION,
    "description": APP_DESCRIPTION,
    "author": "DBCompare Team",
    "hidden_imports": [
        "sqlite3",
        "mysql.connector",
        "mysql.connector.plugins.mysql_native_password",
        "sqlparse",
        "threading",
        "datetime",
    ],
    "data_files": [
        ("connections.db", "."),
    ],
    "exclude_modules": [
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
    ],
}

# 统一图标配置
ICON_CONFIG = {
    "icon_file": "icon.png",  # 统一使用PNG格式
    "icon_path": PROJECT_ROOT / "icon.png",
}

# 平台特定配置
PLATFORM_CONFIG = {
    "win": {
        "onefile": True,
        "console": False,
        "add_data_separator": ";",
    },
    "mac": {
        "onefile": False,
        "console": False,
        "add_data_separator": ":",
    },
    "linux": {
        "onefile": True,
        "console": True,
        "add_data_separator": ":",
    },
}

# 文件路径配置
PATHS = {
    "src": PROJECT_ROOT / "src",
    "tests": PROJECT_ROOT / "tests",
    "docs": PROJECT_ROOT / "docs",
    "scripts": PROJECT_ROOT / "scripts",
    "config": PROJECT_ROOT / "config",
    "requirements": PROJECT_ROOT / "requirements.txt",
    "app_entry": PROJECT_ROOT / "app.py",
    "build_dir": PROJECT_ROOT / "build",
    "dist_dir": PROJECT_ROOT / "dist",
}

# 构建脚本配置
BUILD_SCRIPTS = {
    "python": "scripts/build/build.py",
    "with_spec": "scripts/build/build_with_spec.py",
    "macos": "scripts/build/build_macos.sh",
    "linux": "scripts/build/build_linux.sh",
    "windows": "scripts/build/build_windows.bat",
}

# 部署脚本配置
DEPLOY_SCRIPTS = {
    "macos": "scripts/deploy/run_mac.sh",
}
