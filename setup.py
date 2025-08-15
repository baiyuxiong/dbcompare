#!/usr/bin/env python3
"""
DBCompare - MySQL表结构比较工具
安装配置文件
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dbcompare",
    version="1.0.0",
    author="DBCompare Team",
    author_email="baiyuxiong@gmail.com",
    description="MySQL表结构比较工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/dbcompare",
    project_urls={
        "Homepage": "https://github.com/your-username/dbcompare",
        "Repository": "https://github.com/your-username/dbcompare",
        "Issues": "https://github.com/your-username/dbcompare/issues",
        "Documentation": "https://github.com/your-username/dbcompare#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dbcompare=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.py", "*.json", "*.png"],
    },
    keywords=["mysql", "database", "compare", "schema", "gui", "pyqt6"],
)
