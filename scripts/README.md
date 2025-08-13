# 构建脚本说明

本目录包含DBCompare项目的构建和部署脚本。

## 目录结构

```
scripts/
├── build/              # 构建脚本
│   ├── build.py           # Python构建脚本
│   ├── build_with_spec.py # 使用spec文件的构建脚本
│   ├── build_macos.sh     # macOS构建脚本
│   ├── build_linux.sh     # Linux构建脚本
│   └── build_windows.bat  # Windows构建脚本
├── deploy/             # 部署脚本
│   └── run_mac.sh         # macOS运行脚本
└── README.md           # 本文件
```

## 使用方法

### 快速构建

```bash
# 使用Python脚本构建（推荐）
python3 build.py

# 或使用根目录的入口脚本
python3 ../build.py
```

### 平台特定构建

```bash
# macOS
bash scripts/build/build_macos.sh

# Linux
bash scripts/build/build_linux.sh

# Windows
scripts/build/build_windows.bat
```

### 高级构建选项

```bash
# 使用spec文件构建（更多控制选项）
python3 scripts/build/build_with_spec.py --help
```

### 运行应用程序

```bash
# macOS
bash scripts/deploy/run_mac.sh
```

## 构建要求

- Python 3.7+
- PyInstaller
- 项目依赖包（见requirements.txt）

## 注意事项

1. 建议在虚拟环境中运行构建脚本
2. 构建前会自动清理旧的构建文件
3. 构建完成后，可执行文件位于 `dist/` 目录
4. 不同平台的构建产物格式不同：
   - Windows: `dist/DBCompare.exe`
   - macOS: `dist/DBCompare.app` 或 `dist/DBCompare/DBCompare`
   - Linux: `dist/DBCompare`
