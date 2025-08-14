# DBCompare 打包指南

本文档介绍如何使用 PyInstaller 将 DBCompare 应用程序打包成可执行文件，支持 Windows、macOS 和 Linux 平台。

## 📋 前置要求

### 通用要求
- Python 3.7 或更高版本
- pip 包管理器
- 网络连接（用于下载依赖包）

### 平台特定要求

#### Windows
- Windows 10 或更高版本
- 建议使用虚拟环境

#### macOS
- macOS 10.14 或更高版本
- 建议使用虚拟环境
- 如果遇到安全警告，需要在系统偏好设置中允许运行

#### Linux
- Ubuntu 18.04+ / CentOS 7+ / Arch Linux
- 需要安装 PyQt6 相关依赖：
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-pyqt6
  
  # CentOS/RHEL
  sudo yum install python3-qt6
  
  # Arch Linux
  sudo pacman -S python-pyqt6
  ```

## 🚀 快速开始

### 方法一：使用通用 Python 脚本（推荐）

```bash
# 运行通用打包脚本
python build.py
```

### 方法二：使用平台特定脚本

#### Windows
```cmd
# 双击运行或在命令行中执行
build_windows.bat
```

#### macOS
```bash
# 给脚本执行权限
chmod +x build_macos.sh

# 运行脚本
./build_macos.sh
```

#### Linux
```bash
# 给脚本执行权限
chmod +x build_linux.sh

# 运行脚本
./build_linux.sh
```

### 方法三：使用高级打包脚本

```bash
# 基本打包
python build_with_spec.py

# 显示控制台窗口（用于调试）
python build_with_spec.py --console

# 启用调试模式
python build_with_spec.py --debug

# 清理构建文件
python build_with_spec.py --clean

# 自定义应用名称
python build_with_spec.py --name MyApp

# 自定义图标
python build_with_spec.py --icon path/to/icon.ico

# 指定目标平台
python build_with_spec.py --platform win
```

## 📁 输出文件

打包完成后，可执行文件将位于 `dist/` 目录中：

- **Windows**: `dist/DBCompare.exe`
- **macOS**: `dist/DBCompare`
- **Linux**: `dist/DBCompare`

## 🔧 高级配置

### 使用 spec 文件

项目包含一个预配置的 `DBCompare.spec` 文件，可以直接使用：

```bash
pyinstaller DBCompare.spec
```

### 自定义配置

您可以修改 `DBCompare.spec` 文件来自定义打包配置：

```python
# 修改应用名称
name='MyCustomApp'

# 启用控制台窗口
console=True

# 添加自定义图标
icon='path/to/icon.ico'

# 添加额外的数据文件
datas = [
    ('connections.db', '.'),
    ('config.ini', '.'),
]
```

### 优化打包大小

为了减小打包后的文件大小，可以：

1. 排除不需要的模块：
```python
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
```

2. 使用 UPX 压缩（如果已安装）：
```bash
pip install upx
```

## 🐛 常见问题

### 1. 打包失败

**问题**: 打包过程中出现错误
**解决方案**:
- 确保所有依赖包已正确安装
- 检查 Python 版本兼容性
- 尝试在虚拟环境中运行

### 2. 运行时缺少模块

**问题**: 运行打包后的程序时提示缺少模块
**解决方案**:
- 在 spec 文件的 `hiddenimports` 中添加缺失的模块
- 重新打包

### 3. 文件大小过大

**问题**: 打包后的文件过大
**解决方案**:
- 检查并排除不需要的模块
- 使用 `--onefile` 选项打包成单个文件
- 考虑使用 `--onedir` 选项打包成目录

### 4. macOS 安全警告

**问题**: 在 macOS 上运行时出现安全警告
**解决方案**:
- 在系统偏好设置 > 安全性与隐私中允许运行
- 或使用 `--console` 选项显示控制台窗口

### 5. Linux 权限问题

**问题**: 在 Linux 上无法运行打包后的程序
**解决方案**:
```bash
chmod +x dist/DBCompare
```

## 📦 分发说明

### Windows
- 将 `dist/DBCompare.exe` 分发给用户
- 用户可以直接双击运行

### macOS
- 将 `dist/DBCompare` 分发给用户
- 可以创建 `.app` 包进行分发

### Linux
- 将 `dist/DBCompare` 分发给用户
- 确保用户有执行权限

## 🔍 调试技巧

### 启用控制台窗口
```bash
python build_with_spec.py --console
```

### 启用调试模式
```bash
python build_with_spec.py --debug
```

### 查看详细日志
```bash
pyinstaller --log-level DEBUG DBCompare.spec
```

## 📝 注意事项

1. **数据库文件**: 确保 `connections.db` 文件存在于项目根目录
2. **图标文件**: 如果需要自定义图标，请准备 `.ico` 文件（Windows）或 `.icns` 文件（macOS）
3. **依赖管理**: 建议使用虚拟环境来避免依赖冲突
4. **测试**: 打包完成后请在不同环境下测试应用程序功能

## 🤝 贡献

如果您在使用过程中遇到问题或有改进建议，请：

1. 检查本文档的常见问题部分
2. 在项目仓库中提交 Issue
3. 提供详细的错误信息和环境信息

---

**祝您打包顺利！** 🎉 